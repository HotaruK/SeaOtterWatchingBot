import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


def get_connection(project_id):
    # Use the application default credentials
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {
        'projectId': project_id,
    })

    return firestore.client()
