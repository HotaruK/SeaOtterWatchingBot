import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime


class AquariumEvent:
    def __init__(self, aquarium: str, location: str, event_name: str, event_type: str,
                 event_date: datetime, document_id=None):
        self.id = document_id
        self.aquarium = aquarium
        self.location = location
        self.name = event_name
        self.type = event_type
        self.date = event_date

    def get_dict(self):
        return {
            "aquarium": self.aquarium,
            "location": self.location,
            "name": self.name,
            "type": self.type,
            "date": self.date.strftime('%Y/%m/%d %H:%M:%S')
        }


def get_connection(project_id):
    # Use the application default credentials
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {
        'projectId': project_id,
    })

    return firestore.client()
