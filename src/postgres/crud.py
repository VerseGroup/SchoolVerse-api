import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

class Backend_Interface:
    def __init__(self):
        self.DATABASE_URL = os.environ['DATABASE_URL']
        self.conn = psycopg2.connect(self.DATABASE_URL, sslmode='require')

    def create_user_table(self):
        try:
            """
            This function creates a table in the database called users.
            """
            create_user_table_query = """
            CREATE TABLE users (
                id SERIAL PRIMARY KEY,
                firebase_id VARCHAR(255) NOT NULL,
                keychain VARCHAR(3000) NOT NULL
            );
            """
            cursor = self.conn.cursor()
            cursor.execute(create_user_table_query)
            self.conn.commit()
            cursor.close()
        except:
            curs = self.conn.cursor()
            curs.execute("ROLLBACK")
            self.conn.commit()
            return {"message": "FAILED TO CREATE USER TABLE"}

    #generate a user
    def create_user(self, firebase_id, key):
        try:
            """
            This function creates a user in the database.
            """
            insert_user_query = """
            INSERT INTO users (firebase_id, keychain)
            VALUES (%s, %s);
            """
            cursor = self.conn.cursor()
            cursor.execute(insert_user_query, (firebase_id, key,))
            self.conn.commit()
            cursor.close()
            return None
        except Exception as e:
            curs = self.conn.cursor()
            curs.execute("ROLLBACK")
            self.conn.commit()
            return {"error": "FAILED TO CREATE USER", "message": "hello" + str(e)}


    #update user keychain
    def update_user_keychain(self, firebase_id, key):
        try:
            """
            This function updates a user's keychain in the database.
            """
            update_user_keychain_query = """
            UPDATE users
            SET keychain = %s
            WHERE firebase_id = %s;
            """
            cursor = self.conn.cursor()
            cursor.execute(update_user_keychain_query, (key, firebase_id,))
            self.conn.commit()
            cursor.close()
        except:
            curs = self.conn.cursor()
            curs.execute("ROLLBACK")
            self.conn.commit()
            return {"message": "FAILED TO UPDATE USER KEYCHAIN"}
    
    #get user keychain
    def get_user_keychain(self, firebase_id):
        try:
            """
            This function gets a user's keychain from the database.
            """
            get_user_keychain_query = """
            SELECT keychain
            FROM users
            WHERE firebase_id = %s;
            """
            cursor = self.conn.cursor()
            cursor.execute(get_user_keychain_query, (firebase_id,))
            keychain = cursor.fetchone()
            cursor.close()
            return keychain
        except:
            curs = self.conn.cursor()
            curs.execute("ROLLBACK")
            self.conn.commit()
            return None
    
    #delete user by firebase_id
    def delete_user(self, firebase_id):
        try:
            """
            This function deletes a user from the database.
            """
            delete_user_query = """
            DELETE FROM users
            WHERE firebase_id = %s;
            """
            cursor = self.conn.cursor()
            cursor.execute(delete_user_query, (firebase_id,))
            self.conn.commit()
            cursor.close()
        except:
            curs = self.conn.cursor()
            curs.execute("ROLLBACK")
            self.conn.commit()
            return {"message": "FAILED TO DELETE USER"}
    

#interface = Backend_Interface()
#interface.create_user_table()
#interface.create_user(42, "hello")