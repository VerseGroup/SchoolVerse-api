from json import load
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()



class Backend_Interface:
    def __init__(self):
        self.DATABASE_URL = os.environ['DATABASE_URL']
        self.conn = psycopg2.connect(self.DATABASE_URL, sslmode='require')

    def create_user_table(self):
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

    

    #generate a user
    def create_user(self, firebase_id, key):
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
    
    

interface = Backend_Interface()
#interface.create_user_table()
#interface.create_user(42, "hello")