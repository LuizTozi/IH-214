"""Deterministic simulation of a single TLOF from request to release."""

import argparse
import json
import sys
from bisect import insort
from collections import Counter
from decimal import Decimal
from pathlib import Path

ZERO = Decimal(0)
SECONDS_PER_HOUR = Decimal(3600)


def seconds(value, field, *, positive=False):
    if type(value) not in (int, Decimal):
        raise ValueError(f"{field} must be a number in seconds")
    value = Decimal(value)
    # Millisecond resolution avoids numerical ambiguity at event ties.
    if (not value.is_finite() or not ZERO <= value <= 10**9
            or value != value.quantize(Decimal("0.001"))
            or (positive and value == ZERO)):
        raise ValueError(f"{field} must be {'positive' if positive else 'nonnegative'},"
                         " at most 10^9 s, with millisecond resolution")
    return value


def load_scenario(path):
    scenario = json.loads(path.read_text(), parse_float=Decimal)
    if scenario["kind"] not in {"synthetic_verification", "literature_scenario_verification"}:
        raise ValueError("unknown verification scenario kind")
    for field in ("scenario_id", "basis"):
        if not isinstance(scenario[field], str) or not scenario[field].strip():
            raise ValueError(f"{field} must be a nonempty string")
    horizon = seconds(scenario["horizon_s"], "horizon_s", positive=True)
    separation = seconds(scenario["separation_s"], "separation_s")
    if not isinstance(scenario["requests"], list):
        raise ValueError("requests must be a list")
    seen = set()
    requests = []
    for row in scenario["requests"]:
        key = row["id"]
        if not isinstance(key, str) or not key.strip() or key in seen:
            raise ValueError("request IDs must be nonempty and unique")
        seen.add(key)
        time = seconds(row["request_s"], f"{key}.request_s")
        if time >= horizon:
            raise ValueError(f"{key}.request_s must be before the horizon")
        duration = seconds(row["occupancy_s"], f"{key}.occupancy_s", positive=True)
        window = row.get("window_s")
        if window is not None:
            earliest, latest = (seconds(t, f"{key}.window_s") for t in window)
            if earliest < time or latest < earliest:
                raise ValueError(f"{key}: invalid touchdown window")
            window = (earliest, latest)
        requests.append((key, time, duration, window))
    return scenario, horizon, separation, sorted(requests, key=lambda row: row[1])


def first_free_time(reservations, earliest, total):
    for start, end in reservations:
        if earliest + total(earliest) <= start:
            break
        earliest = max(earliest, end)
    return earliest


def observed_duration(start, end, horizon):
    return max(ZERO, min(end, horizon) - start)


def allocate(requests, policy, resource_duration):
    """Yield each request and the allocated start, or None on rejection."""
    reservations = []
    next_free = ZERO
    for key, time, duration, window in requests:
        def total(start):
            return resource_duration(key, duration, start)
        if policy == "scheduled":
            if window is None:
                raise ValueError(f"{key}: scheduled policy requires window_s")
            earliest, latest = window
            start = first_free_time(reservations, earliest, total)
            if start > latest:
                yield key, time, duration, None
                continue
            insort(reservations, (start, start + total(start)))
        else:
            start = max(time, next_free)
            next_free = start + total(start)
        yield key, time, duration, start


def simulate(path, policy):
    scenario, horizon, separation, requests = load_scenario(path)
    occupancy = restriction = ZERO
    rows = []
    events = []
    waits = []
    states = Counter({name: 0 for name in (
        "rejected", "waiting", "occupied", "separation", "released"
    )})

    for key, time, duration, touchdown in allocate(
        requests, policy, lambda key, duration, start: duration + separation
    ):
        events.append((time, "request", key))
        if touchdown is None:
            rows.append({"id": key, "state": "rejected"})
            events.append((time, "rejected", key))
            states["rejected"] += 1
            continue
        physical_exit = touchdown + duration
        release = physical_exit + separation

        if touchdown >= horizon:
            state = "waiting"
        elif physical_exit >= horizon:
            state = "occupied"
        elif release >= horizon:
            state = "separation"
        else:
            state = "released"

        states[state] += 1
        occupancy += observed_duration(touchdown, physical_exit, horizon)
        restriction += observed_duration(physical_exit, release, horizon)
        for timestamp, name in ((touchdown, "touchdown"),
                                (physical_exit, "physical_exit"),
                                (release, "release")):
            if timestamp < horizon:
                events.append((timestamp, name, key))
        if touchdown < horizon:
            waits.append(touchdown - time)
        rows.append({"id": key, "state": state, "planned_touchdown_s": touchdown,
                     "planned_exit_s": physical_exit, "planned_release_s": release})

    # Exits and releases precede the next occupation at a tie. The stable sort
    # preserves input order among requests submitted at the same instant.
    order = {name: i for i, name in enumerate(
        ("physical_exit", "release", "request", "rejected", "touchdown")
    )}
    events.sort(key=lambda event: (event[0], order[event[1]]))
    return {
        "scenario_id": scenario["scenario_id"], "kind": scenario["kind"],
        "basis": scenario["basis"], "policy": policy,
        "horizon_s": horizon, "separation_s": separation,
        "inputs": [
            {"id": key, "request_s": time, "occupancy_s": duration, "window_s": window}
            for key, time, duration, window in requests
        ],
        "requests": rows,
        "events": [{"t_s": time, "event": name, "id": key} for time, name, key in events],
        "summary": {
            "requested": len(requests),
            "accepted": len(requests) - states["rejected"],
            "states_at_horizon": dict(states),
            "physical_utilization": occupancy / horizon,
            "post_exit_restriction_fraction": restriction / horizon,
            "release_rate_per_hour": states["released"] * SECONDS_PER_HOUR / horizon,
            "observed_wait_count": len(waits),
            "mean_observed_access_delay_s": sum(waits, ZERO) / len(waits) if waits else None,
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scenario", type=Path)
    parser.add_argument("--policy", choices=("scheduled", "fcfs"), default="scheduled")
    args = parser.parse_args()
    try:
        report = simulate(args.scenario, args.policy)
    except (OSError, ValueError, TypeError, KeyError, ArithmeticError) as error:
        parser.exit(2, f"Phase A input error: {error}\n")
    json.dump(report, sys.stdout, default=float, ensure_ascii=False, indent=2, allow_nan=False)
    print()


if __name__ == "__main__":
    main()
