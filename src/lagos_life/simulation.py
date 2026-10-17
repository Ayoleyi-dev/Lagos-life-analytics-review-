"""Entirely hypothetical player-event simulation, NOT observed Lagos Life telemetry."""
from __future__ import annotations

import random
from collections import defaultdict
from datetime import date, timedelta


def simulate_sessions(n_players: int = 250, seed: int = 42) -> list[dict]:
    if n_players < 1:
        raise ValueError("n_players must be positive")
    rng = random.Random(seed)
    start = date(2026, 10, 1)
    events = []
    for p in range(n_players):
        cohort_offset = rng.randrange(0, 7)
        signup = start + timedelta(days=cohort_offset)
        user_id = f"SIM-{p + 1:04d}"  # Fabricated IDs, not real players
        for day_since in range(14 - cohort_offset):
            if day_since == 0:
                active = True
            elif day_since == 1:
                active = rng.random() < 0.50
            elif day_since == 7:
                active = rng.random() < 0.23
            else:
                active = rng.random() < 0.32
            if active:
                events.append({
                    "synthetic_user_id": user_id,
                    "signup_date": signup.isoformat(),
                    "session_date": (signup + timedelta(days=day_since)).isoformat(),
                    "day_since_signup": day_since,
                    "session_minutes": rng.randint(3, 55),
                    "feature": rng.choice(["work", "social", "housing", "transport", "explore"]),
                    "data_class": "SYNTHETIC_SIMULATION",
                })
    return events


def retention(events: list[dict], day: int) -> dict:
    if day < 0:
        raise ValueError("day must be nonnegative")
    players_by_cohort = defaultdict(set)
    retained_by_cohort = defaultdict(set)
    observation_end = max((date.fromisoformat(r["session_date"]) for r in events), default=None)
    for event in events:
        uid = event["synthetic_user_id"]
        signup = date.fromisoformat(event["signup_date"])
        if observation_end is None or signup + timedelta(days=day) > observation_end:
            continue
        players_by_cohort[signup].add(uid)
        if event["day_since_signup"] == day:
            retained_by_cohort[signup].add(uid)
    eligible = sum(len(ids) for ids in players_by_cohort.values())
    retained = sum(len(retained_by_cohort[c]) for c in players_by_cohort)
    return {
        "day": day,
        "eligible_players": eligible,
        "retained_players": retained,
        "retention_rate": round(retained / eligible, 4) if eligible else None,
        "data_class": "SYNTHETIC_SIMULATION",
    }
