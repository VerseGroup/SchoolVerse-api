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

interface = Backend_Interface()
#interface.create_user_table()
#interface.create_key_table()