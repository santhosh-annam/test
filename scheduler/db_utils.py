import psycopg2 as psql
import pyodbc
from configs import *
from utils import *

def close_psql_db(ebankingDB, ebCursor):
    if(ebCursor):
        ebCursor.close()
        
    if(ebankingDB):
        ebankingDB.close()
        log_info("Postgres db is closed politely")

def close_sybase_db(sybaseDB, sbCursor):
    if(sbCursor):
        sbCursor.close()
        
    if(sybaseDB):
        sybaseDB.close()
        log_info("Sybase db is closed politely")
        
def open_ebanking_db():
    try:
        ebankingDB = psql.connect(user = db_username,
                            password = db_password,
                            host = db_host,
                            port = db_port,
                            database = db_name)
        return ebankingDB
    except psql.OperationalError as e:
        log_exception("ERROR : Unable to connect to " + db_name + " database - ", e)
        exit_program()
        
def open_sybase_db():
    try:
        sybaseDB = pyodbc.connect(driver="FreeTDS", server=sybase_host, database=sybase_db, port=sybase_prt, uid=sybase_usr, pwd=sybase_passwd)
        #sybaseDB = psql.connect(user = sybase_usr, password = sybase_passwd, host = sybase_host, port = sybase_prt, database = sybase_db)
        return sybaseDB;
    except psql.OperationalError as e:
        log_exception("ERROR : Unable to connect to " + sybase_db + " database - ", e)
        exit_program()      
        
     
def truncate_tables(ebDBConn, ebCursor):
    try:
        ebCursor.execute("TRUNCATE TABLE eregister.card_hash;")
        ebCursor.execute("TRUNCATE TABLE eregister.card_temp_details;")
        ebDBConn.commit()
        
    except psql.OperationalError as e:
        log_exception("ERROR : Unable to connect to truncate tables.", e)
        exit_program() 