"""Tests for headshot CSV contract + missing-image helpers (issue #4)."""

from __future__ import annotations

from unittest.mock import MagicMock

import pandas as pd
import pytest

from nfl_player_search.config import PASSING, RECEIVING, RUSHING
from nfl_player_search.data import load_images, load_stats
from nfl_player_search.ui import (
    IMAGE_MISSING_LABEL,
    _response_looks_like_image,
    _show_missing_image,
)


def test_image_csvs_have_player_and_url_columns() -> None:
    for cfg in (PASSING, RUSHING, RECEIVING):
        imgs = pd.read_csv(cfg.images_csv)
        assert list(imgs.columns)[:2] == ["Player", "Player Image"]
        assert imgs["Player"].notna().all()
        assert imgs["Player"].nunique() == len(imgs)


def test_modern_star_has_headshot_url() -> None:
    """A known modern star should carry a non-empty nflverse/NFL.com URL."""
    qb = pd.read_csv(PASSING.images_csv)
    # Patrick Mahomes / Josh Allen style — at least one of these after refresh
    stars = {"Patrick Mahomes", "Josh Allen", "Joe Burrow", "Lamar Jackson"}
    rows = qb[qb["Player"].isin(stars)]
    assert not rows.empty, "expected at least one modern QB star in image CSV"
    assert (rows["Player Image"].astype(str).str.strip() != "").any()
    assert rows["Player Image"].astype(str).str.contains("nfl.com|espncdn|nflverse", case=False, regex=True).any()


def test_historical_miss_has_empty_url_for_missing_label() -> None:
    """Pre-nflverse careers often lack URLs — UI shows silhouette + Image missing."""
    rb_imgs = pd.read_csv(RUSHING.images_csv)
    stats = load_stats(str(RUSHING.stats_csv), None)
    # Jim Brown is in RB stats; nflverse headshot coverage for 1960s is thin.
    assert (stats["Player"] == "Jim Brown").any()
    hit = rb_imgs.loc[rb_imgs["Player"] == "Jim Brown"]
    assert not hit.empty, "image CSV should list all stats players (URL may be empty)"
    url = str(hit.iloc[0]["Player Image"]).strip()
    assert url == "" or url.lower() == "nan"

    # Brandon Jacobs was a classic old-CSV miss; nflverse may now supply a URL.
    assert (stats["Player"] == "Brandon Jacobs").any()


def test_response_looks_like_image_rejects_html() -> None:
    ok = MagicMock()
    ok.headers = {"Content-Type": "image/png"}
    ok.content = b"\x89PNG" + b"x" * 600
    assert _response_looks_like_image(ok) is True

    html = MagicMock()
    html.headers = {"Content-Type": "text/html"}
    html.content = b"<!DOCTYPE html><html>nope</html>" + b"x" * 600
    assert _response_looks_like_image(html) is False

    disguised = MagicMock()
    disguised.headers = {"Content-Type": "image/jpeg"}
    disguised.content = b"<!DOCTYPE html>" + b"x" * 600
    assert _response_looks_like_image(disguised) is False


def test_show_missing_image_adds_caption(monkeypatch: pytest.MonkeyPatch) -> None:
    col = MagicMock()
    # Force placeholder path missing so we hit col.info + caption
    cfg = MagicMock()
    cfg.placeholder_image.exists.return_value = False
    cfg.placeholder_size = (10, 10)
    _show_missing_image(col, "Brandon Jacobs", cfg)
    col.info.assert_called()
    col.caption.assert_called_with(IMAGE_MISSING_LABEL)


def test_modern_hit_rate_gate() -> None:
    """Merge gate: majority of modern (2021+) players have a non-empty URL."""
    for cfg, key in ((PASSING, "QB"), (RUSHING, "RB"), (RECEIVING, "WR")):
        rename = tuple(cfg.rename_map.items()) if cfg.rename_map else None
        stats = load_stats(str(cfg.stats_csv), rename)
        modern = set(stats.loc[stats["Year"] >= 2021, "Player"].dropna().astype(str))
        imgs = load_images(str(cfg.images_csv))
        url_map = dict(
            zip(
                imgs["Player"].astype(str),
                imgs["Player Image"].fillna("").astype(str).str.strip(),
            )
        )
        with_url = sum(1 for n in modern if url_map.get(n, ""))
        rate = with_url / len(modern) if modern else 0.0
        assert rate >= 0.90, f"{key} modern URL hit-rate {rate:.1%} below 90%"
