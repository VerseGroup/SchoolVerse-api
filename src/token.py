def verify_token(db, user_id, token):
    user_dict = db.collection(u'USERS').document(user_id).get().to_dict()
    if user_dict['token'] == token:
        return True
    else:
        return False

def verify_ios_token(db, token):
    token = db.collection(u'QUEUES').document(u'ios').get().to_dict()['token']
    if token == token:
        return True
    else:
        return False