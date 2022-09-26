# get user encryptions with id
def get_private_key(id, db) -> dict:
    user_ref = db.collection(u'users').document(f'{id}')
    doc = user_ref.get()

    if doc.exists:
        doc_dict = doc.to_dict()
        
        try:
            key = doc_dict['private_key']
        except:
            return {"message": "user does not have a private key"}

        return {
            "message": "success",
            "key": key,
        }

    else:
        return {
            "message" : "Invalid user ID"
        }