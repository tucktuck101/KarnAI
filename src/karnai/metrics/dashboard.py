from __future__ import annotations

from typing import Any, Dict


def render_dashboard(summary: Dict[str, Any]) -> str:
    lines = [
        "KarnAI Metrics Dashboard",
        "-----------------------",
        f"Replays:               {summary.get('replays', 0)}",
        f"Total steps:           {summary.get('total_steps', 0)}",
        f"Avg steps / replay:    {summary.get('avg_steps_per_replay', 0.0)}",
        f"Determinism rate:      {summary.get('determinism_rate', 0.0)}",
        f"Unique snapshot hashes:{summary.get('unique_sha', 0)}",
    ]
    return "\n".join(lines)
