def write_creds(username, password, user_id, platform_code, db):

    # getting the current cred array
    user_ref = db.collection(u'USERS').document(f'{user_id}')
    doc = user_ref.get()
    
    # if it exists, update the array
    if doc.exists:
        doc_dict = doc.to_dict()
        creds = doc_dict['CREDS']
        creds[f'{platform_code}'] = [username, password]
    
    # if it doesnt exist, create the array
    else:
        creds = {f"{platform_code}" : [username, password]}

    # formatting the creds into the dictionary
    formatted_data = {"CREDS" : creds}

    # writing the data to the database
    db.collection(u'USERS').document(f'{user_id}').update(formatted_data) 
    
    return {"message" : "success"}

# get user encryptions with id
def get_encrypted_credentials(id, platform_code, db) -> dict:
    user_ref = db.collection(u'USERS').document(f'{id}')
    doc = user_ref.get()

    if doc.exists:
        doc_dict = doc.to_dict()
        creds = doc_dict['CREDS']

        try:
            return {
                "code" : '0',
                "username_ciphertext" : creds[f'{platform_code}'][0],
                "password_ciphertext" : creds[f'{platform_code}'][1]
            }

        except:
            return {
                "message" : "error with reading cipher, probably doesn't exist",
                "code" : "1-a"
            }

    else:
        return {
            "message" : "Invalid user ID",
            "code" : "1a"
        }