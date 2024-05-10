import os
from typing import List, Optional
from datetime import datetime, timedelta

import tweepy


class TwitterAPI:
    def __init__(self):
        self.client_v2 = self._get_client_v2()
        self.client_v1 = self._get_client_v1()
        self.tweet_response_limit = 20

    def _get_client_v2(self) -> tweepy.Client:
        """Returns V2 version of API client

        Note: Func names are different from V1
        """
        return tweepy.Client(
            consumer_key=os.environ[f"TWITTER_API_KEY"],
            consumer_secret=os.environ[f"TWITTER_API_SECRET"],
            access_token=os.environ[f"TWITTER_ACCESS_TOKEN"],
            access_token_secret=os.environ[f"TWITTER_ACCESS_TOKEN_SECRET"],
            wait_on_rate_limit=True,
            bearer_token=os.environ[f"TWITTER_BEARER_TOKEN"],
        )

    def _get_client_v1(self) -> tweepy.API:
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

    def get_me_id(self):
        # Returns the ID of the authenticated user for tweet creation purposes
        return self.client_v2.get_me().data.id  # type: ignore

    def get_mentions(
        self,
        look_back_timedelta: timedelta = timedelta(minutes=20),
    ) -> List[tweepy.Tweet]:
        start_time = datetime.now() - look_back_timedelta

        # Convert to required string format
        start_time_str = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")

        return self.client_v2.get_users_mentions(
            id=self.get_me_id(),
            start_time=start_time_str,
        ).data  # type: ignore

    def get_last_replied_tweets_ids(self):
        # Returns the ID of the last tweet replied to
        tweets = self.client_v2.get_users_tweets(id=self.get_me_id(), expansions=["referenced_tweets.id"], tweet_fields=["referenced_tweets"]).data  # type: ignore
        referenced_tweets_lists = [
            tweet.referenced_tweets for tweet in tweets if tweet.referenced_tweets
        ]
        return [
            referend_tweet.id
            for referenced_tweet_list in referenced_tweets_lists
            for referend_tweet in referenced_tweet_list
        ]

    def post_tweet(
        self,
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
            twitter_media = self.client_v1.media_upload(
                filename="chart.png", file=image
            )
            kwargs["media_ids"] = [twitter_media.media_id]  # type: ignore
        return self.client_v2.create_tweet(
            text=message["text"], in_reply_to_tweet_id=previous_tweet_id, **kwargs
        )

    def tweet_thread(self, messages: List[dict[str, str]]) -> None:
        """Posts all messages in a thread

        Args:
            messages : [{str: str}]
                A list of dict containing type and message,
                following `post_tweet` message arg
        """
        previous_tweet_id = None
        for message in messages:
            tweet = self.post_tweet(message, previous_tweet_id=previous_tweet_id)
            previous_tweet_id = tweet.data["id"]  # type: ignore
