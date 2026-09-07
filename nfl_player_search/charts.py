"""Radar chart helpers."""

from __future__ import annotations

from typing import Sequence

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def create_radar_chart(
    ax: plt.Axes,
    angles: np.ndarray,
    player_row: np.ndarray,
    stat_labels: Sequence[str],
    color: str = "blue",
) -> plt.Axes:
    """Draw a single-player radar using the trailing percentile-rank values."""
    values = np.append(player_row[-(len(angles) - 1) :], player_row[-(len(angles) - 1)])
    ax.plot(angles, values, color=color, linewidth=2)
    ax.fill(angles, values, color=color, alpha=0.2)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(list(stat_labels))
    ax.set_yticklabels([])
    ax.text(np.pi / 2, 1.7, player_row[0], ha="center", va="center", size=18, color=color)
    ax.grid(color="white", linewidth=1.5)
    ax.set(xlim=(0, 2 * np.pi), ylim=(0, 1))
    return ax


def player_radar_figure(
    ranked_season: pd.DataFrame,
    player: str,
    stat_labels: Sequence[str],
    offset: float,
    color: str,
) -> plt.Figure:
    """Build a matplotlib figure with one polar radar for `player`."""
    mpl.rcParams["font.size"] = 16
    mpl.rcParams["axes.linewidth"] = 0
    mpl.rcParams["xtick.major.pad"] = 15

    angles = np.linspace(0, 2 * np.pi, len(stat_labels) + 1) + offset
    row = np.asarray(ranked_season.loc[ranked_season["Player"] == player].iloc[0])

    fig = plt.figure(figsize=(8, 8), facecolor="white")
    ax = fig.add_subplot(222, projection="polar", facecolor="#ededed")
    create_radar_chart(ax, angles, row, stat_labels, color=color)
    return fig
