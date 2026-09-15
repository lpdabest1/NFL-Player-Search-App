"""CLI: refresh committed *_Search_Images.csv from nflreadpy headshots."""
from __future__ import annotations

import argparse

from .headshots import run_headshots
from .lookups import latest_completed_season


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--stats-start",
        type=int,
        default=1999,
        help="First season to pull headshot_url overrides from player_stats",
    )
    parser.add_argument(
        "--stats-end",
        type=int,
        default=None,
        help="Last season inclusive (default: latest completed REG)",
    )
    args = parser.parse_args()
    end = args.stats_end if args.stats_end is not None else latest_completed_season()
    print(f"Headshot ETL: stats URL window {args.stats_start}–{end}")
    summary = run_headshots(args.stats_start, end)
    print("Done.")
    for key, info in summary.items():
        print(
            f"  {key}: overall {info['with_url']}/{info['players']} "
            f"({info['overall_pct']:.1f}%), modern {info['modern_with_url']}/"
            f"{info['modern_players']} ({info['modern_pct']:.1f}%)"
        )


if __name__ == "__main__":
    main()
