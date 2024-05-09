from dataclasses import asdict
import logging
import os
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

from lib.templates import AddressScanTemplate
from lib.zero_mev.transformers import (
    preprocess,
    get_scan_address_data_from_mev_transactions,
)
from lib.w3 import get_address
from lib.zero_mev.api import get_all_mev_transactions_related_to_address

from telegram.ext import (
    Application,
    CommandHandler,
)

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)


async def scan_address(update: Update, context: CallbackContext):
    invalid_address_response = (
        "Invalid address provided, please provide a valid Ethereum address."
    )
    try:
        address = context.args[0]  # type: ignore
        logging.info(f"Scanning {address} address")
        address_bytes = get_address(address)
        if not address_bytes:
            await update.message.reply_text(invalid_address_response)  # type: ignore
            return

        mev_txs = await get_all_mev_transactions_related_to_address(address_bytes)
        mev_txs_with_user_loss = preprocess(
            mev_txs, type_filter=["sandwich"], dropna_columns=[]
        )
        if mev_txs_with_user_loss.empty:
            await update.message.reply_text(  # type: ignore
                "No MEV transactions found for the provided address."
            )
            return

        scan_data = get_scan_address_data_from_mev_transactions(
            mev_txs_with_user_loss, address
        )
        response = AddressScanTemplate.create_telegram_message(asdict(scan_data))
        await update.message.reply_text(response)  # type: ignore
        return

    except (IndexError, ValueError):
        await update.message.reply_text(invalid_address_response)  # type: ignore

    except:
        await update.message.reply_text(  # type: ignore
            "An error occurred while processing the request."
        )


async def help_command(update: Update, context: CallbackContext):
    help_text = (
        "Welcome to the MEV Block Scanner Bot! Here are the commands you can use:\n\n"
        "/scan_address <address | ens_name> - reply with how much MEV a wallet has suffered.\n"
        "/help - Shows this help message."
    )
    await update.message.reply_text(help_text)  # type: ignore


def main():
    application = Application.builder().token(os.getenv("TELEGRAM_TOKEN")).build()  # type: ignore

    application.add_handler(CommandHandler("scan_address", scan_address))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("start", help_command))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
