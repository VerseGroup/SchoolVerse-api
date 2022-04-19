import os, sys

# append paths
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parent_dir)

# db 
from firebase_auth import start_firebase

def reset_task_tables(db):
    task_reference = db.collection(u'TASKS')
    task_docs = task_reference.list_documents()
    for doc in task_docs:
        task_reference.document(doc.id).delete()

if __name__ == "__main__":
    db = start_firebase()
    reset_task_tables(db)
    db.close()