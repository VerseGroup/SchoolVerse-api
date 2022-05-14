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
            firebase_id VARCHAR(255) NOT NULL
        );
        """
        cursor = self.conn.cursor()
        cursor.execute(create_user_table_query)
        self.conn.commit()
        cursor.close()

    def create_key_table(self):
        """
        This function creates a table in the database called users.
        """
        create_user_table_query = """
        CREATE TABLE keys (
            id SERIAL PRIMARY KEY,
            platform_code VARCHAR(255) NOT NULL,
            key VARCHAR(3000) NOT NULL,
            CONSTRAINT fk_user 
            FOREIGN KEY(id) 
            REFERENCES users(id)
        );
        """
        cursor = self.conn.cursor()
        cursor.execute(create_user_table_query)
        self.conn.commit()
        cursor.close()

    #generate a user
    def generate_users(self, firebase_id):
        """
        This function creates a user in the database.
        """
        insert_user_query = """
        INSERT INTO users (firebase_id)
        VALUES (%s);
        """
        cursor = self.conn.cursor()
        cursor.execute(insert_user_query, (firebase_id,))
        self.conn.commit()
        cursor.close()
    
    #generate a key for a user 
    def generate_keys(self, platform_code, key, fk_user):
        """
        This function creates a key in the database.
        """
        insert_user_query = """
        INSERT INTO keys (platform_code, key, fk_user)
        VALUES (%s, %s, %s);
        """
        cursor = self.conn.cursor()
        cursor.execute(insert_user_query, (platform_code, key, fk_user))
        self.conn.commit()
        cursor.close()

interface = Backend_Interface()
#interface.create_user_table()
#interface.create_key_table()