"""Verify a round trip through one TLOF, one shared route and one stand."""

import argparse
import json
import sys
from pathlib import Path

from phase_a import allocate, load_scenario, observed_duration, seconds


def simulate(path, policy):
    scenario, horizon, arrival_separation, requests = load_scenario(path)
    stand = seconds(scenario["stand_service_s"], "stand_service_s", positive=True)
    stages = {key: [("stand_service", stand)] for key, *_ in requests}
    return simulate_cycles(scenario, horizon, arrival_separation, requests, policy, stages)


def simulate_cycles(scenario, horizon, arrival_separation, requests, policy, stages, stand_plan=None):
    taxi = seconds(scenario["taxi_s"], "taxi_s", positive=True)
    departure = seconds(scenario["departure_occupancy_s"], "departure_occupancy_s",
                        positive=True)
    departure_separation = seconds(scenario["departure_separation_s"],
                                   "departure_separation_s")

    # An arrival requires the only stand and the only route at admission.
    # If an aircraft is already in the system, its return must clear the TLOF
    # and the departure separation before another arrival can acquire all three.
    def operations(key, entry):
        return stand_plan(key, entry) if stand_plan else stages[key]

    def cycle_duration(key, occupancy, touchdown):
        entry = touchdown + occupancy + taxi
        service = sum(duration for _, duration in operations(key, entry))
        return (occupancy + max(arrival_separation, taxi + service)
                + taxi + departure + departure_separation)

    records = []
    intervals = []
    for key, request, occupancy, touchdown in allocate(
        requests, policy, cycle_duration
    ):
        if touchdown is None:
            records.append({"id": key, "request_s": request, "state": "rejected"})
            continue
        taxi_in = touchdown + occupancy
        arrival_release = taxi_in + arrival_separation
        stand_entry = taxi_in + taxi
        stand_ready = stand_entry
        timeline = []
        for operation, duration in operations(key, stand_entry):
            start = stand_ready
            stand_ready += duration
            timeline.append({"operation": operation, "start_s": start, "end_s": stand_ready})
        taxi_out = max(arrival_release, stand_ready)
        departure_entry = taxi_out + taxi
        departure_exit = departure_entry + departure
        release = departure_exit + departure_separation

        periods = (
            ("tlof", "reserved_for_departure", taxi_out, departure_entry),
            ("tlof", "occupied", touchdown, taxi_in),
            ("tlof", "separation", taxi_in, arrival_release),
            ("tlof", "occupied", departure_entry, departure_exit),
            ("tlof", "separation", departure_exit, release),
            ("taxiway", "reserved", touchdown, taxi_in),
            ("taxiway", "occupied", taxi_in, stand_entry),
            ("taxiway", "occupied", taxi_out, departure_entry),
            ("stand", "reserved", touchdown, stand_entry),
            ("stand", "occupied", stand_entry, taxi_out),
        )
        for stage in timeline:
            if stage["operation"] == "charge":
                periods += (("charger", "occupied", stage["start_s"], stage["end_s"]),)
        for resource, state, start, end in periods:
            duration = observed_duration(start, end, horizon)
            if duration:
                intervals.append({"id": key, "resource": resource, "state": state,
                                  "start_s": start, "end_s": min(end, horizon)})

        if release < horizon:
            state = "completed"
        elif touchdown < horizon:
            state = "in_system"
        else:
            state = "waiting"
        records.append({"id": key, "request_s": request, "state": state,
                        "planned_touchdown_s": touchdown, "planned_taxi_in_s": taxi_in,
                        "planned_stand_entry_s": stand_entry,
                        "planned_stand_ready_s": stand_ready,
                        "planned_taxi_out_s": taxi_out,
                        "planned_departure_entry_s": departure_entry,
                        "planned_departure_exit_s": departure_exit,
                        "planned_tlof_release_s": release,
                        "planned_stand_blocked_s": taxi_out - stand_ready})

        if "stand_service_s" not in scenario:
            records[-1]["planned_stand_stages"] = timeline

    departure_measurements = []
    for row in records:
        if "planned_taxi_out_s" not in row:
            continue
        markers = {}
        for name, field in (("stand_exit", "taxi_out"), ("tlof_entry", "departure_entry"),
                            ("liftoff", "departure_exit"), ("release", "tlof_release")):
            instant = row[f"planned_{field}_s"]
            markers[name] = instant if instant < horizon else None
        durations = {}
        for name, begin, end in (("taxi", "stand_exit", "tlof_entry"),
                                 ("occupancy", "tlof_entry", "liftoff"),
                                 ("separation", "liftoff", "release")):
            durations[name] = (None if markers[end] is None
                               else markers[end] - markers[begin])
        departure_measurements.append({"id": row["id"], "event_s": markers,
                                       "elapsed_s": durations})
    intervals.sort(key=lambda row: row["start_s"])
    return {"scenario": scenario, "policy": policy, "requests": records,
            "observed_resource_intervals": intervals,
            "simulated_departure_measurements": departure_measurements}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scenario", type=Path)
    parser.add_argument("--policy", choices=("scheduled", "fcfs"), default="scheduled")
    args = parser.parse_args()
    try:
        report = simulate(args.scenario, args.policy)
    except (OSError, ValueError, TypeError, KeyError, ArithmeticError) as error:
        parser.exit(2, f"Phase B input error: {error}\n")
    json.dump(report, sys.stdout, default=float, ensure_ascii=False, indent=2, allow_nan=False)
    print()


if __name__ == "__main__":
    main()
