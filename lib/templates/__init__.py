from typing import List
import discord
import pystache
from abc import ABC, abstractmethod
from lib.templates.utils import (
    capitalize_first_letter,
    format_currency,
)


class AbstractTemplate(ABC):
    @staticmethod
    @abstractmethod
    def __title_template__() -> str:
        pass

    @staticmethod
    @abstractmethod
    def __stats_templates__() -> List[str]:
        pass

    @staticmethod
    @abstractmethod
    def __footers_templates__() -> List[str]:
        pass

    @classmethod
    def create_discord_embed(cls, data, inline=False):
        formatted_data = format_variables(data)
        text_footer = "\n".join(cls.__footers_templates__())
        embed = discord.Embed(
            title=pystache.render(cls.__title_template__(), formatted_data),
        )

        embed.set_footer(text=pystache.render(text_footer, formatted_data))
        for stat in cls.__stats_templates__():
            name_template = stat["name"]
            value_template = stat["value"]
            name = pystache.render(name_template, formatted_data)
            value = pystache.render(value_template, formatted_data)
            embed.add_field(name=name, value=value, inline=inline)
        return embed

    @classmethod
    def create_telegram_message(cls, data):
        formatted_data = format_variables(data)
        text_footer = "\n".join(cls.__footers_templates__())
        title = pystache.render(cls.__title_template__(), formatted_data)
        message = f"{title}\n\n\n"
        for stat in cls.__stats_templates__():
            name_template = stat["name"]
            value_template = stat["value"]
            name = pystache.render(name_template, formatted_data)
            value = pystache.render(value_template, formatted_data)
            message += f"{name}: {value}\n"
        message += f"\n\n{text_footer}"
        return message


class AddressScanTemplate(AbstractTemplate):
    @staticmethod
    def __title_template__() -> str:
        return "MEV Receipt for {{address}}"

    @staticmethod
    def __stats_templates__() -> List[str]:
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

    @staticmethod
    def __footers_templates__() -> List[str]:
        return [
            "Stop Feeding the MEV bots!",
            "Install MEV blocker: https://cow.fi/mev-blocker",
        ]


class WeekOverviewTemplate(AbstractTemplate):
    @staticmethod
    def __title_template__() -> str:
        return "Weekly MEV Report"

    @staticmethod
    def __stats_templates__() -> List[str]:
        return [
            {
                "name": "Number of swaps MEV’d (frontruns and sandwiches)",
                "value": "{{mev_swaps_number}}",
            },
            {
                "name": "Amount of MEV extracted",
                "value": "{{mev_extracted_amount}}",
            },
            {
                "name": "Amount in MEV bot profits",
                "value": "{{mev_profit_amount}}",
            },
            {
                "name": "Total number of MEV victim addresses",
                "value": "{{mev_victims_number}}",
            },
        ]

    @staticmethod
    def __footers_templates__() -> List[str]:
        return [
            "Stop Feeding the MEV bots!",
            "Install MEV blocker: https://cow.fi/mev-blocker",
        ]


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
        config["key"]: config["formatter"](data[config["key"]])
        for config in data_formatter_configs
        if data.get(config["key"])
    }

    return data
