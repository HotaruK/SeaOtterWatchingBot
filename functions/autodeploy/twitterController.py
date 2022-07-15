from twitter import Twitter, OAuth


def get_twitter_connection(token: str, token_secret: str, consumer_key: str, consumer_secret: str) -> Twitter:
    return Twitter(
        auth=OAuth(token, token_secret, consumer_key, consumer_secret)
    )


def post_tweet(text: str, t: Twitter):
    t.statuses.update(status=text)
