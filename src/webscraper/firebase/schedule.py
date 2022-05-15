import json

def write_schedule(user_id, days, db):

    day_array = []

    for key in days:
        day = days[key]
        day['day'] = "Day " + str(key)
        day_array.append(day)

    schedule = {
        "user_id": user_id,
        "days": day_array
    }

    # wierd type issue fix
    schedule = json.loads(json.dumps(schedule))

    print(schedule)

    db.collection(u'SCHEDULES').document(f'{user_id}').set(schedule)

