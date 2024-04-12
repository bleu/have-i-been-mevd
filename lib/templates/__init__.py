from typing import List
import discord
import pystache
from abc import ABC, abstractmethod
from lib.templates.utils import (
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


class AddressScanTemplate(AbstractTemplate):
    @staticmethod
    def __title_template__() -> str:
        return "MEV Receipt for {{  address  }}"

    @staticmethod
    def __stats_templates__() -> List[str]:
        return [
            {
                "name": "MEV Suffered",
                "value": "{{ totalAmountUsd }} across {{ mevTxsLength }} swaps",
            },
            {
                "name": "Most lost to",
                "value": "{{ mostMevContractName }} (total of {{ mostMevUsdAmount }})",
            },
        ]

    @staticmethod
    def __footers_templates__() -> List[str]:
        return [
            "Stop Feeding the MEV bots!",
            "Install MEV blocker: https://cow.fi/mev-blocker",
        ]


class AddressScanAddressNotFound(AbstractTemplate):
    @staticmethod
    def __title_template__() -> str:
        return "MEV Receipt for {{  address  }}"

    @staticmethod
    def __stats_templates__() -> List[str]:
        return [
            {
                "name": "MEV Suffered",
                "value": "{{ totalAmountUsd }} across {{ mevTxsLength }} swaps",
            },
            {
                "name": "Most lost to",
                "value": "{{ mostMevContractName }} (total of {{ mostMevUsdAmount }})",
            },
        ]

    @staticmethod
    def __footers_templates__() -> List[str]:
        return [
            "Stop Feeding the MEV bots!",
            "Install MEV blocker: https://cow.fi/mev-blocker",
        ]


data_formatter_configs = [
    {"key": "totalAmountUsd", "formatter": format_currency},
    {"key": "mostMevUsdAmount", "formatter": format_currency},
    {"key": "mostMevContractName", "formatter": str},
    {"key": "mevTxsLength", "formatter": str},
    {"key": "address", "formatter": str},
]


def format_variables(data):
    data = {
        config["key"]: config["formatter"](data[config["key"]])
        for config in data_formatter_configs
        if data.get(config["key"])
    }

    return data
