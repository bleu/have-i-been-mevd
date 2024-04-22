from typing import Dict, List
import discord
import pystache
from abc import ABC, abstractmethod
from lib.templates.images import generate_image
from lib.templates.utils import (
    capitalize_first_letter,
    format_currency,
)

data_formatter_configs = [
    {"key": "total_amount_usd", "formatter": format_currency},
    {"key": "most_mev_protocol_usd_amount", "formatter": format_currency},
    {"key": "most_mev_protocol_name", "formatter": capitalize_first_letter},
    {"key": "mev_txs_length", "formatter": str},
    {"key": "address", "formatter": str},
    {"key": "mev_swaps_number", "formatter": str},
    {"key": "mev_extracted_amount", "formatter": format_currency},
    {"key": "mev_profit_amount", "formatter": format_currency},
    {"key": "mev_victims_number", "formatter": str},
]


def format_variables(data):
    data = {
        config["key"]: config["formatter"](data[config["key"]])  # type: ignore
        for config in data_formatter_configs  # type: ignore
        if data.get(config["key"])
    }

    return data


class AbstractTemplate(ABC):
    @staticmethod
    @abstractmethod
    def _title_template() -> str:
        pass

    @staticmethod
    @abstractmethod
    def _stats_templates() -> List[dict[str, str]]:
        pass

    @staticmethod
    def _footers_templates() -> List[str]:
        return [
            "Stop Feeding the MEV bots!",
            "Install MEV blocker: https://mevblocker.io/",
        ]

    @classmethod
    def create_twitter_post(
        cls,
        data,
        has_image=False,
        x_image: List[str] = None,
        y_image: List[int | float] = None,
    ):
        message = dict()
        formatted_data = format_variables(data)
        title = pystache.render(cls._title_template(), formatted_data)
        stats = "\n".join(
            [
                f"{pystache.render(stat['name'], formatted_data)}: {pystache.render(stat['value'], formatted_data)}"
                for stat in cls._stats_templates()
            ]
        )
        footer = "\n".join(cls._footers_templates())
        message["text"] = f"{title}\n\n{stats}\n\n{footer}"
        if has_image:
            if not x_image or not y_image:
                raise ValueError("x_image and y_image must be provided")
            message["image"] = cls.generate_image(x_image, y_image)
        return message

    @classmethod
    def create_discord_embed(
        cls, data, inline=False, has_image=False, x_image=None, y_image=None
    ):
        output = {}
        formatted_data = format_variables(data)
        text_footer = "\n".join(cls._footers_templates())
        embed = discord.Embed(
            title=pystache.render(cls._title_template(), formatted_data),
        )

        embed.set_footer(text=pystache.render(text_footer, formatted_data))
        for stat in cls._stats_templates():
            name_template = stat["name"]
            value_template = stat["value"]
            name = pystache.render(name_template, formatted_data)
            value = pystache.render(value_template, formatted_data)
            embed.add_field(name=name, value=value, inline=inline)

        output["embed"] = embed
        if has_image:
            if not x_image or not y_image:
                raise ValueError("x_image and y_image must be provided")
            image = cls.generate_image(x_image, y_image)
            filename = "plot.png"
            discord_file = discord.File(image, filename=filename)
            embed.set_image(url=f"attachment://{filename}")
            output["file"] = discord_file

        return output

    @classmethod
    def create_telegram_message(cls, data):
        formatted_data = format_variables(data)
        text_footer = "\n".join(cls._footers_templates())
        title = pystache.render(cls._title_template(), formatted_data)
        message = f"{title}\n\n\n"
        for stat in cls._stats_templates():
            name_template = stat["name"]
            value_template = stat["value"]
            name = pystache.render(name_template, formatted_data)
            value = pystache.render(value_template, formatted_data)
            message += f"{name}: {value}\n"
        message += f"\n\n{text_footer}"
        return message

    @staticmethod
    def generate_image(x: List[str], y: List[int | float]):
        raise NotImplementedError(
            "This method should be implemented in the child class."
        )


class AddressScanTemplate(AbstractTemplate):
    @staticmethod
    def _title_template() -> str:
        return "MEV Receipt for {{address}}"

    @staticmethod
    def _stats_templates() -> List[dict[str, str]]:
        return [
            {
                "name": "MEV Suffered",
                "value": "{{total_amount_usd}} across {{mev_txs_length}} swaps",
            },
            {
                "name": "Most lost to",
                "value": "{{most_mev_protocol_name}} ({{most_mev_protocol_usd_amount}})",
            },
        ]


class WeekOverviewNumberOfSwaps(AbstractTemplate):
    @staticmethod
    def _title_template() -> str:
        return "Last Week MEV Stat"

    @staticmethod
    def _stats_templates() -> List[dict[str, str]]:
        return [
            {
                "name": "Number of swaps MEV’d",
                "value": "{{mev_swaps_number}}",
            },
        ]

    @staticmethod
    def generate_image(x: List[str], y: List[int | float]):
        title = "Last Week MEV Swaps per type"
        xlabel = "MEV Type"
        ylabel = "Number of Swaps"
        return generate_image(
            x=x,
            y=y,
            title=title,
            xlabel=xlabel,
            ylabel=ylabel,
        )


class WeekOverviewExtractedAmount(AbstractTemplate):
    @staticmethod
    def _title_template() -> str:
        return "Last Week MEV Stat"

    @staticmethod
    def _stats_templates() -> List[dict[str, str]]:
        return [
            {
                "name": "Total Extracted Amount",
                "value": "{{mev_extracted_amount}}",
            },
        ]


class WeekOverviewProfitAmount(AbstractTemplate):
    @staticmethod
    def _title_template() -> str:
        return "Last Week MEV Stat"

    @staticmethod
    def _stats_templates() -> List[dict[str, str]]:
        return [
            {
                "name": "Total MEV Bots profit",
                "value": "{{mev_profit_amount}}",
            },
        ]


class WeekOverviewVictims(AbstractTemplate):
    @staticmethod
    def _title_template() -> str:
        return "Last Week MEV Stat"

    @staticmethod
    def _stats_templates() -> List[dict[str, str]]:
        return [
            {
                "name": "Total number of MEV victim addresses",
                "value": "{{mev_victims_number}}",
            },
        ]
