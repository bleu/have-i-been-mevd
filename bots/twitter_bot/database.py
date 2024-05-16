import logging
import os
import sqlite3
from datetime import datetime, timezone


class DatabaseRepliedTweets:
    def __enter__(self) -> "DatabaseRepliedTweets":
        self.conn = self._get_or_create_database()
        return self

    def __exit__(self, *args) -> None:
        self.conn.close()

    def _get_or_create_database(self) -> sqlite3.Connection:
        db_exists = os.path.exists("/data/replies.db")
        conn = sqlite3.connect("/data/replies.db", detect_types=sqlite3.PARSE_DECLTYPES)
        if not db_exists:
            logging.debug("Creating sqlite DB")
            cursor = conn.cursor()
            cursor.execute(
                """
            CREATE TABLE IF NOT EXISTS REPLIES (
                tweet_replied_id TEXT PRIMARY KEY,
                replied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            )
            conn.commit()
        else:
            logging.debug("Using existing sqlite DB")
        return conn

    def check_if_tweet_was_replied_to(self, tweet_id: str) -> bool:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT tweet_replied_id
            FROM REPLIES
            WHERE tweet_replied_id = ?
            """,
            (tweet_id,),
        )
        return cursor.fetchone() is not None

    def insert_tweet_ids(self, tweet_ids: list[str]) -> None:
        cursor = self.conn.cursor()
        current_utc_timestamp_to_database = datetime.now(timezone.utc).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        cursor.executemany(
            """
            INSERT INTO REPLIES (tweet_replied_id, replied_at)
            VALUES (?, ?)
            """,
            [(tweet_id, current_utc_timestamp_to_database) for tweet_id in tweet_ids],
        )
        self.conn.commit()
        return

    def clean_1_day_old_replies(self) -> None:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            DELETE FROM REPLIES
            WHERE replied_at < datetime('now', '-1 day')
            """
        )
        self.conn.commit()
        return
