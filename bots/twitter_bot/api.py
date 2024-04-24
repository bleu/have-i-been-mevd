import os
from typing import List, Optional

import tweepy


def get_client_v2() -> tweepy.Client:
    """Returns V2 version of API client

    Note: Func names are different from V1
    """
    return tweepy.Client(
        consumer_key=os.environ[f"TWITTER_API_KEY"],
        consumer_secret=os.environ[f"TWITTER_API_SECRET"],
        access_token=os.environ[f"TWITTER_ACCESS_TOKEN"],
        access_token_secret=os.environ[f"TWITTER_ACCESS_TOKEN_SECRET"],
    )


def get_client_v1() -> tweepy.API:
    """Return API client from the V1 version,
    which still being used to upload media
    """
    auth = tweepy.OAuth1UserHandler(
        os.environ[f"TWITTER_API_KEY"],
        os.environ[f"TWITTER_API_SECRET"],
        os.environ[f"TWITTER_ACCESS_TOKEN"],
        os.environ[f"TWITTER_ACCESS_TOKEN_SECRET"],
    )
    return tweepy.API(auth)


def post_tweet(
    client_v2: tweepy.Client,
    api_v1: tweepy.API,
    message: dict[str, str],
    previous_tweet_id: Optional[int] = None,
    **kwargs,
):
    """Uses the module Schedule to programatically create repeatable tasks

    Args:
        client_v2 : tweepy.Client
            Client that enables usage of the V2 API
        api_v1 : tweepy.API
            Client that enables usage of the V1 API
        message : {str: str}
            A dict containing type and message

            Ex: {"text": "A tweet!"}
        previous_tweet_id : int
            ID of the last previous tweet

            Note: This turns a tweet into a thread


    """
    image = message.get("image")
    if image:
        twitter_media = api_v1.media_upload(filename="chart.png", file=image)
        kwargs["media_ids"] = [twitter_media.media_id]  # type: ignore
    return client_v2.create_tweet(
        text=message["text"], in_reply_to_tweet_id=previous_tweet_id, **kwargs
    )


def tweet_thread(messages: List[dict[str, str]]) -> None:
    """Posts all messages in a thread

    Args:
        messages : [{str: str}]
            A list of dict containing type and message,
            following `post_tweet` message arg
    """
    client = get_client_v2()
    api = get_client_v1()
    previous_tweet_id = None
    for message in messages:
        tweet = post_tweet(client, api, message, previous_tweet_id=previous_tweet_id)
        previous_tweet_id = tweet.data["id"]
