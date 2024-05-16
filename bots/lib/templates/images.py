import matplotlib.font_manager as font_manager
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns

from typing import List, Union
from lib.templates.utils import format_currency, fig_to_bytesio

COLORS = ["#FF4242", "#FFB800", "#015F2A", "#FFADD0", "#743C3C", "#FFE298"]
FONT_COLOR = "#1E0E00"

font_path = "lib/templates/Nunito.ttf"
font_manager.fontManager.addfont(font_path)
prop = font_manager.FontProperties(fname=font_path)

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = prop.get_name()


def generate_base_plot(title: str):
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.set_facecolor("#FFFAEE")
    ax.set_facecolor("#FFFAEE")
    ax.set_title(
        title,
        fontsize=16,
        color=FONT_COLOR,
        fontweight="heavy",
        pad=20,
    )
    return fig, ax


def bar_plot(
    x: List[str], y: List[Union[int, float]], xlabel: str, ylabel: str, title: str
):
    x = [str(i).capitalize() for i in x]

    fig, ax = generate_base_plot(title)

    custom_cmap = LinearSegmentedColormap.from_list(
        "custom_green_red", [COLORS[2], COLORS[0]]
    )

    norm = plt.Normalize(min(y), max(y))  # type: ignore
    colors = [custom_cmap(norm(value)) for value in y]  # type: ignore

    sns.barplot(x=x, y=y, palette=colors, ax=ax)
    plt.grid(color=FONT_COLOR, linestyle="--", linewidth=0.3)

    ax.set_xlabel(
        xlabel,
        fontsize=14,
        color=FONT_COLOR,
        fontweight="bold",
    )
    ax.set_ylabel(
        ylabel,
        fontsize=14,
        color=FONT_COLOR,
        fontweight="bold",
    )

    ax.tick_params(axis="x", colors=FONT_COLOR, labelsize=12)
    ax.tick_params(axis="y", colors=FONT_COLOR, labelsize=12)

    for i, v in enumerate(y):
        ax.text(
            i,
            v + 3,
            format_currency(v),
            ha="center",
            color=FONT_COLOR,
            fontweight="bold",
        )

    for spine in ax.spines.values():
        spine.set_visible(False)

    image = fig_to_bytesio(fig)
    plt.close(fig)
    return image


def pie_plot(x: List[str], y: List[Union[int, float]], title: str):
    fig, ax = generate_base_plot(title)
    labels = [str(i).capitalize() for i in x]
    ax.pie(
        y,
        labels=labels,
        colors=COLORS,
        autopct="%1.1f%%",
        startangle=140,
        pctdistance=1.15,
        labeldistance=1.3,
        textprops={
            "color": FONT_COLOR,
            "fontweight": "bold",
            "fontsize": 16,
        },
    )
    ax.axis("equal")

    image = fig_to_bytesio(fig)
    plt.close(fig)
    return image
