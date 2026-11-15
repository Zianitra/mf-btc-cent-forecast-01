#!/usr/bin/env python3
"""make.fun btc-cent-forecast-01 entry — forecasts BTC price 240 minutes ahead.

Model: damped exponentially-weighted level (alpha 0.12) blended 80/20 with a
24h moving average. Deterministic, stdlib only.
"""
import json
import os


def forecast(prices: list[float]) -> float:
    alpha = 0.12
    level = prices[0]
    for x in prices[-800:]:
        level = alpha * x + (1 - alpha) * level
    long_ma = sum(prices[-1440:]) / len(prices[-1440:])
    return 0.8 * level + 0.2 * long_ma


def main() -> None:
    src = "/input" if os.path.isdir("/input") else "input"
    out = "/output" if os.path.isdir("/output") else "output"
    os.makedirs(out, exist_ok=True)
    for name in sorted(os.listdir(src)):
        if not name.endswith(".in"):
            continue
        with open(os.path.join(src, name), encoding="utf-8") as f:
            case = json.load(f)
        prices = case["markets"][0]["prices"]
        guess = forecast(prices)
        case_id = case.get("case") or name[:-3]
        with open(os.path.join(out, case_id + ".out"), "w", encoding="utf-8") as f:
            f.write(f"{guess:.2f}\n")


if __name__ == "__main__":
    main()
