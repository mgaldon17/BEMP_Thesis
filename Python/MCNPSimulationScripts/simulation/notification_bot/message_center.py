import os
import time

import pytz
import tweepy
import base64

def read_parameters():
    input_files_dir = os.path.join(os.path.dirname(__file__), 'config', '')

    with open(os.path.join(input_files_dir, 'auth_params.txt'), 'rb') as file:
        base64_encoded_parameters = file.read()

    # Decode the base64-encoded parameters
    decoded_parameters = base64.b64decode(base64_encoded_parameters).decode()

    parameters = {key.strip(): value.strip() for line in decoded_parameters.split('\n') if '=' in line for key, value in [line.strip().split('=')]}
    return parameters


class MessageCenter:

    # In order to be able to read the auth parameters, those must be written in a txt file in config/auth_params.txt
    # CONSUMER_KEY = ...
    # CONSUMER_SECRET = ...
    # ACCESS_TOKEN = ...
    # ACCESS_TOKEN_SECRET = ...
    # BEARER_TOKEN = ...

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
