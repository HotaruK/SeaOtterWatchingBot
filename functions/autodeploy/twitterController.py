import requests
from requests_oauthlib import OAuth1
from .settings import twitter_tweet_post_url


def get_twitter_oauth(consumer_key: str, consumer_secret: str,
                      access_token: str, access_token_secret: str) -> OAuth1:
    return OAuth1(consumer_key, consumer_secret, access_token, access_token_secret)


def post_tweet(text: str, oauth: OAuth1):
    r = requests.post(twitter_tweet_post_url, auth=oauth, json={"text": text},
                      headers={"Content-Type": "application/json"})
    r.raise_for_status()
