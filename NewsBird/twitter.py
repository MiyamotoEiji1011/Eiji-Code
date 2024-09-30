import tweepy
import config

api_key = config.TWEETER_API_KEY
api_secret_key = config.TWEETER_API_SECRET_KEY
access_token = config.TWEETER_ACCESS_TOKEN
access_secret_token = config.TWEETER_ACCESS_SECRET_TOKEN

def client_info():
    client = tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret_key,
        access_token=access_token,
        access_token_secret=access_secret_token
    )
    return client


def create_tweet(message):
    client = client_info()
    tweet = client.create_tweet(text=message)
    return tweet
