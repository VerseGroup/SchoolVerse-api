def write_schedule(user_id, days, db):
    
    schedule = {
        "user_id": user_id,
        "days": days
    }

    db.collection(u'SCHEDULES').document(f'{user_id}').set(schedule)

