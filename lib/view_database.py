from src.postgres.crud import Backend_Interface
import psycopg2

def script():
    ss = Backend_Interface()
    
    conn = ss.conn

