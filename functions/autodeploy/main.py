import functions_framework
from datetime import datetime, timedelta
import pytz
from .settings import firestore_collection_name, firestore_project_id, \
    montereybay_sea_otter_url, vancouver_sea_otter_url, \
    twitter_consumer_key, twitter_consumer_secret, twitter_token, twitter_token_secret
from .firestoreController import get_firestore_connection
from .twitterController import get_twitter_oauth, post_tweet

tz_la = pytz.timezone('America/Los_Angeles')

s = [
    firestore_project_id, firestore_collection_name,
    twitter_consumer_key, twitter_consumer_secret, twitter_token, twitter_token_secret
]


@functions_framework.cloud_event
def main_cloud_event(cloud_event):
    print(f"Received event with ID: {cloud_event['id']} and data {cloud_event.data}")
    if not _check_secrets():
        print(s)
        raise RuntimeError("secrets have None, please check it")

    current_ev_time, next_ev_time = _get_base_time_events(datetime.now(tz=tz_la))
    print(f"target time: current->{current_ev_time}, next->{next_ev_time}")

    db = get_firestore_connection(firestore_project_id)
    prep_tweets = []

    # current start event
    current_events = _get_events_by_time(firestore_collection_name, current_ev_time, db)
    for ev in current_events:
        url = _get_url(ev)
        text = f"{ev.get('aquarium')}: {ev.get('date')} {ev.get('name')} has just begun! {url}"
        prep_tweets.append(text)

    # next start event
    next_events = _get_events_by_time(firestore_collection_name, next_ev_time, db)
    for ev in next_events:
        text = f"{ev.get('aquarium')}: {ev.get('name')} will begin soon, starting at {ev.get('date')}"
        prep_tweets.append(text)

    print("prep_tweets:", prep_tweets)

    # tweet
    for i in prep_tweets:
        oauth = get_twitter_oauth(twitter_consumer_key, twitter_consumer_secret, twitter_token, twitter_token_secret)
        post_tweet(i, oauth)


def _get_events_by_time(collection: str, time: str, db) -> list:
    return db.collection(collection).where("date", "==", time).stream()


def _get_base_time_events(now: datetime) -> tuple[str, str]:
    fmt = '%Y/%m/%d %H:%M:%S'
    minute = 0 if 0 <= now.minute <= 29 else 30
    adjust_now = datetime(now.year, now.month, now.day, now.hour, minute, 0, tzinfo=tz_la)

    next_event_time = adjust_now + timedelta(minutes=30)

    return adjust_now.strftime(fmt), next_event_time.strftime(fmt)


def _check_secrets():
    return False if None in s else True


def _get_url(ev):
    if ev["aquarium"] is "Monterey Bay Aquarium":
        return montereybay_sea_otter_url if ev.get('location') == "Sea Otters exhibit" else ""
    if ev["aquarium"] is "Vancouver Aquarium":
        return vancouver_sea_otter_url
    else:
        return ""
