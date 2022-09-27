""" import json

def write_schedule(user_id, days, db):
    
    schedule = {
        "user_id": str(user_id),
        "days": days
    }

    # wierd type issue fix
    schedule = json.loads(json.dumps(schedule))

    db.collection(u'SCHEDULES').document(f'{user_id}').set(schedule)

 """