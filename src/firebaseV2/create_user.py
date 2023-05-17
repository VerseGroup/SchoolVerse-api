def create_user(db, user_id, email, name, grade):
    try:
        db.collection(u'users').document(f'{user_id}').set({
            u'user_id': user_id,
            u'email': email,
            u'display_name': name,
            u'grade_level': grade,
            u'approved': False,
            u'courses': [],
            u'task_ids': [],
            u'subscribed_sports': [],
            u'club_ids': [],
        })
        return (True, '')
    except Exception as e:
        return (False, str(e))