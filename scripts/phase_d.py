"""Couple terminal queues and manifested passengers to the single-stand aircraft cycle."""

import argparse
import json
import sys
from decimal import Decimal
from math import ceil
from pathlib import Path

from phase_a import load_scenario, seconds
from phase_b import simulate_cycles


def terminal(scenario, horizon):
    passengers = {}
    visits = []
    pending = []
    groups = {}
    for flight in scenario["requests"]:
        key = flight["id"]
        cutoff = seconds(flight["manifest_close_s"], "manifest_close_s")
        if cutoff > flight["request_s"] or not 1 <= len(flight["manifest"]) <= 4:
            raise ValueError("close manifest by aircraft request and reserve 1–4 seats")
        groups[key] = []
        for person in flight["manifest"]:
            pid = person["id"]
            if not isinstance(pid, str) or not pid or pid in passengers:
                raise ValueError("passenger IDs must be unique nonempty strings")
            arrival = person["arrival_s"]
            row = {"id": pid, "flight": key, "arrival_s": arrival}
            passengers[pid] = row
            if arrival is None:
                row["state"] = "absent"
                continue
            arrival = seconds(arrival, "arrival_s")
            if arrival > cutoff:
                row["state"] = "late"
                continue
            row["state"] = "accepted"
            groups[key].append(pid)
            pending.append((arrival, pid, person))

    los = {}
    for station in ("counter", "baggage", "security"):
        available = Decimal(0)
        following = []
        waits = []
        censored = 0
        limit = scenario["wait_limits_s"].get(station)
        for entry, pid, person in sorted(pending):
            service = (person["bag_service_s"] if station == "baggage"
                       else scenario["terminal_service_s"][station])
            service = seconds(service, station, positive=True)
            if station == "baggage" and not 30 <= service <= 60:
                raise ValueError("bag_service_s outside PAR-028")
            start = max(entry, available)
            available = start + service
            following.append((available, pid, person))
            if entry < horizon:
                wait = start - entry if start < horizon else None
                visits.append({"id": pid, "station": station, "entry_s": entry,
                               "start_s": start if start < horizon else None,
                               "end_s": available if available < horizon else None,
                               "wait_s": wait})
                if wait is None:
                    censored += 1
                else:
                    waits.append(wait)
        compliant = sum(w <= limit for w in waits) if limit is not None else None
        los[station] = {"complete": len(waits), "censored": censored, "within": compliant,
                        "ratio": compliant / len(waits) if waits and limit is not None else None}
        pending = following
    for ready, pid, _ in pending:
        passengers[pid]["planned_terminal_ready_s"] = ready
    return passengers, groups, visits, los


def simulate(path, policy):
    scenario, horizon, separation, requests = load_scenario(path)
    people, groups, visits, los = terminal(scenario, horizon)
    flights = {row["id"]: row for row in scenario["requests"]}
    durations = {k: seconds(v, k, positive=True) for k, v in scenario["service_s"].items()}
    tolerance = seconds(scenario["punctuality_tolerance_s"], "punctuality_tolerance_s")
    for flight in flights.values():
        minutes = flight["declared_charge_min"]
        if type(minutes) is not int or minutes not in (0, 30, 60):
            raise ValueError("invalid declared charge")
        seconds(flight["target_departure_s"], "target_departure_s")

    def stand_plan(key, entry):
        plan = [(k, durations[k]) for k in ("detach_tug", "deboard", "exit_gate")]
        charge = flights[key]["declared_charge_min"] * 60
        if charge:
            plan.append(("charge", charge))
        available = entry + sum(t for _, t in plan)
        group = sorted(groups[key], key=lambda pid: (people[pid]["planned_terminal_ready_s"], pid))
        for pid in group:
            ready = people[pid]["planned_terminal_ready_s"]
            wait = max(0, ready - available)
            if wait:
                plan.append(("await_passenger", wait))
            for k in ("walk_in", "enter_gate", "board"):
                plan.append((f"{k}/{pid}", durations[k]))
            available += wait + durations["walk_in"] + durations["enter_gate"] + durations["board"]
        plan.append(("attach_tug", durations["attach_tug"]))
        return plan

    active = [r for r in requests if groups[r[0]]]
    report = simulate_cycles(scenario, horizon, separation, active, policy, {}, stand_plan)
    by_id = {r["id"]: r for r in report["requests"]}
    for key, flight in flights.items():
        if not groups[key]:
            by_id[key] = {"id": key, "request_s": flight["request_s"], "state": "cancelled_empty"}
            continue
        trace = by_id[key]
        for pid in groups[key]:
            people[pid]["state"] = "flight_rejected" if trace["state"] == "rejected" else "pending"
        for stage in trace.get("planned_stand_stages", []):
            if stage["operation"].startswith("board/"):
                trace["planned_boarding_complete_s"] = stage["end_s"]
                pid = stage["operation"].split("/", 1)[1]
                if stage["start_s"] < horizon:
                    row = people[pid]
                    row["boarding_start_s"] = stage["start_s"]
                    row["terminal_to_board_s"] = stage["start_s"] - row["arrival_s"]
                    row["boarding_end_s"] = stage["end_s"] if stage["end_s"] < horizon else None
                    row["state"] = "boarded" if stage["end_s"] < horizon else "boarding"
    report["requests"] = [by_id[r[0]] for r in requests]
    departures = [r for r in report["simulated_departure_measurements"]
                  if r["event_s"]["liftoff"] is not None]
    waits = sorted(p["terminal_to_board_s"] for p in people.values() if "terminal_to_board_s" in p)
    punctual = sum(r["event_s"]["liftoff"] <= flights[r["id"]]["target_departure_s"] + tolerance
                   for r in departures)
    intervals = report["observed_resource_intervals"]
    for visit in visits:
        if visit["start_s"] is not None:
            intervals.append({"id": visit["id"], "resource": visit["station"], "state": "occupied",
                              "start_s": visit["start_s"], "end_s": visit["end_s"] or horizon})
    for flight in report["requests"]:
        for stage in flight.get("planned_stand_stages", []):
            name = stage["operation"].split("/")[0]
            if name in {"deboard", "exit_gate", "enter_gate", "board"} and stage["start_s"] < horizon:
                intervals.append({"id": flight["id"], "resource": "gate", "state": "occupied",
                                  "start_s": stage["start_s"], "end_s": min(stage["end_s"], horizon)})
    intervals.sort(key=lambda row: row["start_s"])
    utilization = {resource: sum(i["end_s"] - i["start_s"] for i in intervals
                                 if i["resource"] == resource and i["state"] == "occupied") / horizon
                   for resource in ("tlof", "taxiway", "stand", "charger", "gate",
                                    "counter", "baggage", "security")}
    report.update(utilization=utilization, boarding_wait_sample=len(waits), passengers=list(people.values()), station_visits=visits, station_los=los,
                  departed=len(departures), departures_per_hour=len(departures) * 3600 / horizon,
                  punctual_departures=punctual,
                  terminal_to_board_p95_s=waits[ceil(len(waits)*0.95)-1] if waits else None)
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scenario", type=Path)
    parser.add_argument("--policy", choices=("scheduled", "fcfs"), default="scheduled")
    args = parser.parse_args()
    try:
        report = simulate(args.scenario, args.policy)
    except (ValueError, TypeError, KeyError, OSError, ArithmeticError) as error:
        parser.exit(2, f"Phase D input error: {error}\n")
    json.dump(report, sys.stdout, default=float, indent=2, allow_nan=False)
    print()
