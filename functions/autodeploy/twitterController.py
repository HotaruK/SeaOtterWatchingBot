from twitter import Twitter, OAuth2


def get_twitter_connection(consumer_key: str, consumer_secret: str,bearer_token:str) -> Twitter:
    return Twitter(
        auth=OAuth2(consumer_key, consumer_secret, bearer_token)
    )


def post_tweet(text: str, t: Twitter):
    t.statuses.update(status=text)
