import os
import time

import pytz
import tweepy
from dotenv import load_dotenv

# Load credentials from a .env file (searched from the current working
# directory upwards). Copy .env.example to .env and fill in your values.
load_dotenv()

REQUIRED_KEYS = (
    "BEARER_TOKEN",
    "CONSUMER_KEY",
    "CONSUMER_SECRET",
    "ACCESS_TOKEN",
    "ACCESS_TOKEN_SECRET",
)


def read_parameters():
    parameters = {key: os.getenv(key) for key in REQUIRED_KEYS}
    missing = [key for key, value in parameters.items() if not value]
    if missing:
        raise RuntimeError(
            "Missing Twitter credentials in the environment: "
            + ", ".join(missing)
            + ". Copy .env.example to .env and fill in the values."
        )
    return parameters


class MessageCenter:

    # Credentials are read from environment variables (loaded from .env):
    # CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, BEARER_TOKEN

    def __init__(self, msg):
        parameters = read_parameters()

        self.message = msg
        self.client = tweepy.Client(parameters['BEARER_TOKEN'],
                                    parameters['CONSUMER_KEY'],
                                    parameters['CONSUMER_SECRET'],
                                    parameters['ACCESS_TOKEN'],
                                    parameters['ACCESS_TOKEN_SECRET'])

    def send_tweet(self):
        self.client.create_tweet(text=self.message)


if __name__ == '__main__':
    timezone = pytz.timezone('Europe/Berlin')
    timestamp = time.strftime("%H:%M:%S", time.localtime())

    message = "Simulation finished at " + str(timestamp) + "h " + str(timezone)
    MessageCenter(message).send_tweet()
