import os, sys

# append paths
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parent_dir)

# db
from firebase_auth import start_firebase

def reset_days(db):
    days_docs = db.collection(u'DAYS').list_documents()
    for doc in days_docs:
        db.collection(u'DAYS').document(doc.id).delete()

if __name__ == "__main__":
    db = start_firebase()
    reset_days(db)
    db.close()