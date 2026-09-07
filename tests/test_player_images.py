"""Image CSV schema + missing-image UX helpers (issue #4)."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from nfl_player_search.config import PASSING, RECEIVING, RUSHING
from nfl_player_search.data import load_images, load_stats
from nfl_player_search.ui import IMAGE_UNAVAILABLE_LABEL, _render_player_image


@pytest.mark.parametrize("cfg", [PASSING, RUSHING, RECEIVING])
def test_image_csv_schema_player_and_url(cfg) -> None:
    images = load_images(str(cfg.images_csv))
    assert list(images.columns) == ["Player", "Player Image"]
    assert images["Player"].nunique() == len(images)
    assert images["Player Image"].astype(str).str.startswith("http").all()


def test_modern_player_has_headshot_url_path() -> None:
    images = load_images(str(PASSING.images_csv))
    mahomes = images.loc[images["Player"] == "Patrick Mahomes", "Player Image"]
    assert not mahomes.empty
    url = str(mahomes.iloc[0])
    assert "http" in url
    assert "nfl.com" in url or "espncdn.com" in url or "nflverse" in url


def test_known_historical_miss_has_no_image_row() -> None:
    """Johnny Unitas-style gap: in stats, absent from refreshed image CSV."""
    rename = tuple(PASSING.rename_map.items()) if PASSING.rename_map else None
    stats = load_stats(str(PASSING.stats_csv), rename)
    assert "Johnny Unitas" in set(stats["Player"])
    images = load_images(str(PASSING.images_csv))
    assert "Johnny Unitas" not in set(images["Player"])


def test_render_unavailable_shows_label_when_no_url() -> None:
    col = MagicMock()
    images = pd.DataFrame(columns=["Player", "Player Image"])
    with patch("nfl_player_search.ui.Image") as pil:
        pil.open.return_value.resize.return_value = MagicMock(name="img")
        _render_player_image(col, images, "Johnny Unitas", PASSING)
    col.caption.assert_called_with(IMAGE_UNAVAILABLE_LABEL)


def test_render_unavailable_on_fetch_failure() -> None:
    col = MagicMock()
    images = pd.DataFrame(
        [{"Player": "Fake Player", "Player Image": "https://example.invalid/nope.jpg"}]
    )
    with patch("nfl_player_search.ui.requests.get", side_effect=OSError("boom")), patch(
        "nfl_player_search.ui.Image"
    ) as pil:
        pil.open.return_value.resize.return_value = MagicMock(name="img")
        _render_player_image(col, images, "Fake Player", PASSING)
    col.caption.assert_called_with(IMAGE_UNAVAILABLE_LABEL)


def test_render_success_skips_unavailable_label() -> None:
    col = MagicMock()
    images = pd.DataFrame(
        [{"Player": "Patrick Mahomes", "Player Image": "https://example.com/m.jpg"}]
    )
    fake_resp = MagicMock()
    fake_resp.content = b"fake"
    fake_resp.raise_for_status = MagicMock()
    with patch("nfl_player_search.ui.requests.get", return_value=fake_resp), patch(
        "nfl_player_search.ui.Image"
    ) as pil:
        pil.open.return_value.resize.return_value = MagicMock(name="img")
        _render_player_image(col, images, "Patrick Mahomes", PASSING)
    col.image.assert_called()
    col.caption.assert_not_called()
