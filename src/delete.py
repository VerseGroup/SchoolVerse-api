from datetime import datetime
from datetime import timedelta

def delete_old_tasks(id, db):
    tasks = db.collection(u'users').document(id).collection(u'tasks').stream()

    for task in tasks:
        task_dict = task.to_dict()
        due_date = task_dict['due_date']
        intial_time = datetime.now() - timedelta(days=1)
        one_month_age = datetime.now() - timedelta(days=30)

        ### janky solution to get around time zone issues (code is EST but firebase runs UTC) - fix later
        due_date = due_date.replace(tzinfo=None)
        intial_time = intial_time.replace(tzinfo=None)
        one_month_age = one_month_age.replace(tzinfo=None)

        if due_date < intial_time and task_dict['completed'] == True or due_date < one_month_age and task_dict['completed'] == True:
            db.collection(u'users').document(id).collection(u'tasks').document(task.id).delete()
        else:
            pass

