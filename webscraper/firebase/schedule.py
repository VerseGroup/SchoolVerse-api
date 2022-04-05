def write_schedule(user_id, schedule, day, db):
    
    day = {
        "day": day,
        "schedule": schedule
    }

    current_data = db.collection(u'SCHEDULES').document(f'{user_id}').get().to_dict()

    if current_data is None:
        days = [day]
        new_data = {
            "days": days,
            "user_id": user_id
        }
        db.collection(u'SCHEDULES').document(f'{user_id}').set(new_data)
    else:
        current_days = current_data['days']
        if day in current_days:
            print("Day already exists")
        else:
            current_days.append(day)
            new_data = {
                "days": current_days,
                "user_id": user_id
            }
            db.collection(u'SCHEDULES').document(f'{user_id}').set(new_data)
            
def check_day_exists(user_id, day, db):
    current_data = db.collection(u'SCHEDULES').document(f'{user_id}').get().to_dict()
    if current_data is None:
        return False
    else:
        current_days = current_data['days']
        if day in current_days:
            return True
        else:
            return False

