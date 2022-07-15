import functions_framework
from datetime import datetime, timedelta
from settings import firestore_collection_name, firestore_project_id, montereybay_sea_otter_url
from .firestoreController.firestore import get_connection


@functions_framework.cloud_event
def main_cloud_event(cloud_event):
    print(f"Received event with ID: {cloud_event['id']} and data {cloud_event.data}")

    current_ev_time, next_ev_time = _get_base_time_events(datetime.now())
    db = get_connection(firestore_project_id)

    # current start event
    current_events = _get_events_by_time(firestore_collection_name, current_ev_time, db)
    for ev in current_events:
        url = montereybay_sea_otter_url if ev.location == "Sea Otters exhibit" else ""
        text = f"{ev.name} has just begun! {url}"
    # todo:tweet

    # next start event
    next_events = _get_events_by_time(firestore_collection_name, next_ev_time, db)
    for ev in next_events:
        text = f"{ev.name} will begin soon, starting at {ev.date}"
    # todo: tweet


def _get_events_by_time(collection: str, time: str, db) -> list:
    return db.collection(collection).where("date", "==", time).stream()


def _get_base_time_events(now: datetime) -> tuple[str, str]:
    fmt = '%Y/%m/%d %H:%M:%S'
    minute = 0 if 0 <= now.minute <= 29 else 30
    adjust_now = datetime(now.year, now.month, now.day, now.hour, minute, 0)

    next_event_time = adjust_now + timedelta(minutes=30)

    return adjust_now.strftime(fmt), next_event_time.strftime(fmt)


# def _post_notificaton_tweet():
