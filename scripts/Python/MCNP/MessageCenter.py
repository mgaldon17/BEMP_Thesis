import time
import pytz
import tweepy

class MessageCenter():

    # In order to be able to read the auth parameters, those must be written in a txt file in config/message_center.txt
    # CONSUMER_KEY = ...
    # CONSUMER_SECRET = ...
    # ACCESS_TOKEN = ...
    # ACCESS_TOKEN_SECRET = ...
    # BEARER_TOKEN = ...

    def __init__(self, msg):

        parameters = self.read_parameters()

        self.message = msg
        self.client = tweepy.Client(parameters['BEARER_TOKEN'],
                                    parameters['CONSUMER_KEY'],
                                    parameters['CONSUMER_SECRET'],
                                    parameters['ACCESS_TOKEN'],
                                    parameters['ACCESS_TOKEN_SECRET'])

    def read_parameters(self):
        parameters = {}
        with open("config/message_center.txt", 'r') as file:
            for line in file:

                if '=' in line:
                    key, value = line.strip().split('=')
                    parameters[key.strip()] = value.strip()

        return parameters
    def send_tweet(self):
        self.client.create_tweet(text=self.message)


if __name__ == '__main__':
    timezone = pytz.timezone('Europe/Berlin')
    timestamp = time.strftime("%H:%M:%S", time.localtime())

    message = "Simulation finished at " + str(timestamp) + "h " + str(timezone)
    MessageCenter(message).send_tweet()
