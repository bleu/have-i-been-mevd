import matplotlib.pyplot as plt
import seaborn as sns

from typing import List, Union
from lib.templates.utils import format_currency, fig_to_bytesio


def generate_base_plot(title: str):
    sns.set_theme(style="darkgrid")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_facecolor("#1e1e1e")
    fig.set_facecolor("#121212")
    ax.set_title(title, fontsize=16, color="white", fontweight="bold")
    return fig, ax


def bar_plot(
    x: List[str], y: List[Union[int, float]], xlabel: str, ylabel: str, title: str
):
    sns.set_theme(style="darkgrid")
    x = [str(i).capitalize() for i in x]

    fig, ax = generate_base_plot(title)
    norm = plt.Normalize(min(y), max(y))  # type: ignore
    colors = plt.cm.Reds(norm(y))  # type: ignore

    sns.barplot(x=x, y=y, palette=colors, ax=ax)

    ax.set_xlabel(
        xlabel,
        fontsize=14,
        color="white",
        fontweight="bold",
    )
    ax.set_xlabel(xlabel, fontsize=14, color="white", fontweight="bold")
    ax.set_ylabel(ylabel, fontsize=14, color="white", fontweight="bold")

    ax.tick_params(axis="x", colors="white", labelsize=12)
    ax.tick_params(axis="y", colors="white", labelsize=12)

    for i, v in enumerate(y):
        ax.text(
            i, v + 3, format_currency(v), ha="center", color="white", fontweight="bold"
        )

    ax.set_facecolor("#1e1e1e")
    fig.set_facecolor("#121212")

    for spine in ax.spines.values():
        spine.set_visible(False)

    image = fig_to_bytesio(fig)
    plt.close(fig)
    return image


def pie_plot(x: List[str], y: List[Union[int, float]], title: str):
    colors = [
        "#c0392b",
        "#e67e22",
        "#f39c12",
        "#d35400",
        "#e74c3c",
    ]
    fig, ax = generate_base_plot(title)
    labels = [str(i).capitalize() for i in x]
    ax.pie(
        y,
        labels=labels,
        colors=colors,
        autopct="%1.1f%%",
        startangle=140,
        pctdistance=1.15,
        labeldistance=1.3,
        textprops={"color": "white", "fontweight": "bold", "fontsize": 16},
    )
    ax.axis("equal")

    image = fig_to_bytesio(fig)
    plt.close(fig)
    return image
