import os, sys

# append paths
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parent_dir)

# db
from firebase_auth import start_firebase

def reset_events(db):
    event_docs = db.collection(u'EVENTS').list_documents()
    for doc in event_docs:
        db.collection(u'EVENTS').document(doc.id).delete()

    EXISTING_EVENTS = {
        "EVENTS" : []
    }

    db.collection(u'EVENTS').document("EXISTING_EVENTS").set(EXISTING_EVENTS)

if __name__ == "__main__":
    db = start_firebase()
    reset_events(db)
    db.close()