import matplotlib.pyplot as plt
import seaborn as sns

from typing import List, Union
from lib.templates.utils import format_currency, fig_to_bytesio


def bar_plot(
    x: List[str], y: List[Union[int, float]], xlabel: str, ylabel: str, title: str
):
    sns.set_theme(style="darkgrid")

    fig, ax = plt.subplots(figsize=(10, 6))

    colors = [
        "#c0392b",
        "#e74c3c",
        "#d35400",
        "#e67e22",
        "#f39c12",
    ]

    sns.barplot(x=x, y=y, palette=colors, ax=ax)

    ax.set_title(
        title,
        fontsize=16,
        color="white",
        fontweight="bold",
    )
    ax.set_xlabel(xlabel, fontsize=14, color="white", fontweight="bold")
    ax.set_ylabel(ylabel, fontsize=14, color="white", fontweight="bold")

    ax.tick_params(axis="x", colors="white", labelsize=12)
    ax.tick_params(axis="y", colors="white", labelsize=12)

    for i, v in enumerate(y):
        ax.text(
            i, v + 3, format_currency(v), color="white", ha="center", fontweight="bold"
        )

    ax.set_facecolor("#1e1e1e")
    fig.set_facecolor("#121212")

    for spine in ax.spines.values():
        spine.set_visible(False)

    image = fig_to_bytesio(fig)
    plt.close(fig)
    return image
