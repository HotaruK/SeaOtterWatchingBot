import functions_framework
from datetime import datetime, timedelta
import pytz
from .settings import firestore_collection_name, firestore_project_id, montereybay_sea_otter_url, \
    twitter_consumer_key, twitter_consumer_secret, twitter_token, twitter_token_secret
from .firestoreController import get_firestore_connection
from .twitterController import get_twitter_connection, post_tweet

s = [
    firestore_project_id, firestore_collection_name,
    twitter_token, twitter_token_secret, twitter_consumer_key, twitter_consumer_secret
]


@functions_framework.cloud_event
def main_cloud_event(cloud_event):
    print(f"Received event with ID: {cloud_event['id']} and data {cloud_event.data}")
    if not _check_secrets():
        print(s)
        raise RuntimeError("secrets have None, please check it")

    current_ev_time, next_ev_time = _get_base_time_events(datetime.now(tz=pytz.timezone('America/Los_Angeles')))
    print(f"target time: current->{current_ev_time}, next->{next_ev_time}")

    db = get_firestore_connection(firestore_project_id)
    prep_tweets = []

    # current start event
    current_events = _get_events_by_time(firestore_collection_name, current_ev_time, db)
    for ev in current_events:
        url = montereybay_sea_otter_url if ev.location == "Sea Otters exhibit" else ""
        text = f"{ev.name} has just begun! {url}"
        prep_tweets.append(text)

    # next start event
    next_events = _get_events_by_time(firestore_collection_name, next_ev_time, db)
    for ev in next_events:
        text = f"{ev.name} will begin soon, starting at {ev.date}"
        prep_tweets.append(text)

    print("prep_tweets:", prep_tweets)

    # tweet
    if prep_tweets:
        t = get_twitter_connection(twitter_token, twitter_token_secret,
                                   twitter_consumer_key, twitter_consumer_secret)
        post_tweet(text, t)


def _get_events_by_time(collection: str, time: str, db) -> list:
    return db.collection(collection).where("date", "==", time).stream()


def _get_base_time_events(now: datetime) -> tuple[str, str]:
    fmt = '%Y/%m/%d %H:%M:%S'
    minute = 0 if 0 <= now.minute <= 29 else 30
    adjust_now = datetime(now.year, now.month, now.day, now.hour, minute, 0,
                          tzinfo=pytz.timezone('America/Los_Angeles'))

    next_event_time = adjust_now + timedelta(minutes=30)

    return adjust_now.strftime(fmt), next_event_time.strftime(fmt)


def _check_secrets():
    return False if None in s else True
