"""Smoke tests for category config wiring."""

from nfl_player_search.config import CATEGORIES, PASSING, RECEIVING, RUSHING


def test_categories_cover_three_offense_groups() -> None:
    assert set(CATEGORIES) == {PASSING.label, RUSHING.label, RECEIVING.label}


def test_rating_weights_match_radar_stats() -> None:
    for cfg in (PASSING, RUSHING, RECEIVING):
        assert set(cfg.rating_weights) == set(cfg.radar_stats)
