# get user encryptions with id
def get_private_key(id, db) -> dict:

    dict = db['users'].find_one({'_id' : id})

    if dict:
        
        try:
            key = dict['private_key']

            return {
            "message": "success",
            "key": key,
            }

        except:
            return {"message": "user does not have a private key"}
            
    else:
        return {
            "message" : "Invalid user ID"
        }