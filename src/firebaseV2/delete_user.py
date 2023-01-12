from src.firebaseV2.auth import delete_user as delete_auth

def delete_user(db, user_id):
    schedules = db.collection(u'users').document(f'{user_id}').collection(u'schedule').stream()
    
    for schedule in schedules:
        db.collection(u'users').document(f'{user_id}').collection(u'schedule').document(schedule.id).delete()

    tasks = db.collection(u'users').document(f'{user_id}').collection(u'tasks').stream()
    for task in tasks:
        db.collection(u'users').document(f'{user_id}').collection(u'tasks').document(task.id).delete()

    db.collection(u'users').document(f'{user_id}').delete()

    delete_auth(user_id)