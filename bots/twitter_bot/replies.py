import logging
import re

import tweepy
import asyncio
from typing import List
from dataclasses import asdict

from lib.templates import AddressScanTemplate
from lib.w3 import get_address
from lib.zero_mev.api import (
    get_all_mev_transactions_related_to_address,
)
from lib.zero_mev.transformers import (
    preprocess,
    get_scan_address_data_from_mev_transactions,
)
from twitter_bot.api import TwitterAPI
from twitter_bot.database import DatabaseRepliedTweets


async def reply_on_mentions():
    with DatabaseRepliedTweets() as database_replied_tweets:
        database_replied_tweets.clean_1_day_old_replies()
        logging.info("Replying on mentions")
        twitter_api = TwitterAPI()
        mentions = twitter_api.get_mentions()
        if not mentions:
            logging.info("No mentions found.")
            return
        mentions_to_reply = filter_not_replied_mentions(
            mentions, database_replied_tweets
        )
        await asyncio.gather(
            *[reply_on_mention(twitter_api, mention) for mention in mentions_to_reply]
        )
        database_replied_tweets.insert_tweet_ids(
            [mention["id"] for mention in mentions_to_reply]
        )


def filter_not_replied_mentions(
    mentions: List[tweepy.Tweet], database_replied_tweets: DatabaseRepliedTweets
) -> List[tweepy.Tweet]:
    return [
        mention
        for mention in mentions
        if database_replied_tweets.check_if_tweet_was_replied_to(mention["id"]) is False
    ]


async def reply_on_mention(twitter_api: TwitterAPI, mention: tweepy.Tweet):
    logging.info(f"Replying to mention {mention['id']}")
    eth_address = extract_eth_address(mention["text"])
    address_bytes = get_address(eth_address)
    if not address_bytes:
        logging.info("Invalid Ethereum address found in the tweet.")
        # twitter_api.post_tweet(
        #     {
        #         "text": "Invalid Ethereum address found in the tweet. Please provide a valid Ethereum address or ENS name on the tweet text."
        #     },
        #     previous_tweet_id=mention["id"],
        # )
        return

    mev_txs = await get_all_mev_transactions_related_to_address(address_bytes)  # type: ignore
    mev_txs_with_user_loss = preprocess(
        mev_txs, type_filter=["sandwich"], dropna_columns=[]
    )
    if mev_txs_with_user_loss.empty:
        twitter_api.post_tweet(
            {"text": "No MEV transactions found for the provided address."},
            previous_tweet_id=mention["id"],
        )
        return

    scan_data = get_scan_address_data_from_mev_transactions(
        mev_txs_with_user_loss, eth_address
    )

    output = AddressScanTemplate.create_twitter_post(asdict(scan_data))
    twitter_api.post_tweet(output, previous_tweet_id=mention["id"])
    return


def extract_eth_address(text: str) -> str:
    eth_address_pattern = r"\b0x[a-fA-F0-9]{40}\b"
    eth_ens_pattern = r"\b[a-zA-Z0-9-]+\.eth\b"

    eth_address_match = re.search(eth_address_pattern, text)
    if eth_address_match:
        return eth_address_match.group(0)

    eth_ens_match = re.search(eth_ens_pattern, text)
    if eth_ens_match:
        return eth_ens_match.group(0)

    return ""
