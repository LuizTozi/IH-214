"""Verify a single stand with declared charging and one passenger in each direction."""

import argparse
import json
import sys
from pathlib import Path

from phase_a import load_scenario, seconds
from phase_b import simulate_cycles


def simulate(path, policy):
    scenario, horizon, separation, requests = load_scenario(path)
    durations = scenario["service_s"]

    def service(name):
        return name, seconds(durations[name], name, positive=True)

    stages = {}
    for row in scenario["requests"]:
        minutes = row["declared_charge_min"]
        if type(minutes) is not int or minutes not in (0, 30, 60):
            raise ValueError("declared_charge_min must be 0, 30 or 60")
        stages[row["id"]] = [
            service("detach_tug"), service("deboard"), service("exit_gate"),
            *([("charge", minutes * 60)] if minutes else []),
            service("enter_gate"), service("board"), service("attach_tug"),
        ]
    return simulate_cycles(scenario, horizon, separation, requests, policy, stages)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scenario", type=Path)
    parser.add_argument("--policy", choices=("scheduled", "fcfs"), default="scheduled")
    args = parser.parse_args()
    try:
        result = simulate(args.scenario, args.policy)
    except (OSError, ValueError, TypeError, KeyError, ArithmeticError) as error:
        parser.exit(2, f"Phase C input error: {error}\n")
    json.dump(result, sys.stdout, ensure_ascii=False, default=float, indent=2, allow_nan=False)
    print()
