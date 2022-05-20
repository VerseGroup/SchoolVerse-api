import os, sys

# append paths
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parent_dir)

# db
from firebase_auth import start_firebase

def reset_sports(db):
    event_docs = db.collection(u'SPORTS').list_documents()
    for doc in event_docs:
        db.collection(u'SPORTS').document(doc.id).delete()

    EXISTING_SPORTS = {
        "SPORTS" : []
    }

    db.collection(u'SPORTS').document("EXISTING_SPORTS").set(EXISTING_SPORTS)

if __name__ == "__main__":
    db = start_firebase()
    reset_sports(db)
    db.close()