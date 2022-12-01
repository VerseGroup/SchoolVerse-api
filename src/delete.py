from datetime import datetime
from datetime import timedelta

def delete_old_tasks(id, db):
    tasks = db.collection(u'users').document(id).collection(u'tasks').stream()

    for task in tasks:
        task_dict = task.to_dict()
        due_date = task_dict['due_date']
        seven_days_ago = datetime.now() - timedelta(days=7)

        ### janky solution to get around time zone issues (code is EST but firebase runs UTC) - fix later
        due_date_date = datetime.strptime(due_date, '%Y-%m-%d').split()
        due_date_day = due_date_date[2]
        due_date_month = due_date_date[1]
        due_date_year = due_date_date[3]
        seven_days_ago = datetime.strptime(seven_days_ago, '%Y-%m-%d').split()
        seven_days_ago_day = seven_days_ago[2]
        seven_days_ago_month = seven_days_ago[1]
        seven_days_ago_year = seven_days_ago[3]

        due_date_date = datetime(int(due_date_year), int(due_date_month), int(due_date_day))
        seven_days_ago = datetime(int(seven_days_ago_year), int(seven_days_ago_month), int(seven_days_ago_day))

        ###

        if due_date < seven_days_ago and task_dict['completed'] == True:
            db.collection(u'users').document(id).collection(u'tasks').document(task.id).delete()
        else:
            pass

