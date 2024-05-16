from datetime import date, datetime
from io import BytesIO
from math import floor, log
from time import time


def format_to_mustache(s):
    return f"{{{{{s}}}}}"


def get_metric_name(metric, i, value):
    return f"{metric}_{i + 1}_{value}"


def t_name(metric, i):
    return format_to_mustache(get_metric_name(metric, i, "name"))


def t_value(metric, i):
    return format_to_mustache(get_metric_name(metric, i, "value"))


def t_date(ts):
    return datetime.utcfromtimestamp(ts).strftime("%d %b, %Y")


def fig_to_bytesio(fig):
    image = BytesIO()
    fig.savefig(image, format="png")
    image.seek(0)
    return image


def format_percentage(number):
    return f"{float(number):.2f}%"


def capitalize_first_letter(string):
    return string.capitalize()


def format_number(number, decimals=1, show_magnitude=True):
    number = float(number)
    if number == 0:
        return f"{float(number):,.{decimals}f}"

    units = ["", "k", "M", "B", "T", "Q", "Qn"]
    k = 1000.0
    magnitude = int(floor(log(number, k)))
    if magnitude < 0:
        magnitude = 0

    number = number / k**magnitude if show_magnitude else number
    magnitude_unit = units[magnitude] if show_magnitude else ""
    return f"{float(number):,.{decimals}f}{magnitude_unit}"


def format_currency(number, decimals=1, show_magnitude=True):
    return f"${format_number(number, decimals, show_magnitude)}"


def format_date(time=time()):
    return date.fromtimestamp(int(time)).strftime("%d %b, %Y")


def format_protocol_name(name):
    if name == "uniswap2":
        return "Uniswap V2"
    if name == "uniswap3":
        return "Uniswap V3"
    if name == "zerox":
        return "ZeroX"
    if name == "balancer1":
        return "Balancer V1"
    if name == "compoundv2":
        return "Compound V2"
    return name.capitalize()


def format_mev_type_name(name):
    if name == "arb":
        return "Arbitrage"
    if name == "liquid":
        return "Liquidation"
    return name.capitalize()
