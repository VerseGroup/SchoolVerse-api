def write_schedule(user_id, schedule, day, db):
    schedule = {"schedule": schedule}
    schedule['day'] = day
    schedule['user_id'] = user_id
    db.collection(u'SCHEDULES').document(f'{user_id}').set(schedule)
