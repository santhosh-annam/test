from ftp_operations import *
from utils import *
import time
from card import *
from db_utils import *
from configs import *
import logging, os

def sync_details_from_sybase():
    ebankingDBConn = ebCursor = sybaseDBConn = sybaseCursor = None
    try:
        sybaseConnection = pyodbc.connect(driver="FreeTDS", server=sybase_host, database=sybase_db, port=sybase_prt, uid=sybase_usr, pwd=sybase_passwd)
        print("DB connection established")
        cursor = sybaseConnection.cursor()
        #cursor.execute("SELECT d.acct_no AS acct_no, r.rim_no AS rim, LTRIM(RTRIM(r.tin)) AS cpr, r.Birth_dt FROM dp_acct AS d JOIN rm_acct AS r ON d.rim_no = r.rim_no and r.rim_type='Personal'")
        cursor.execute("""Select a.acct_no, r.rim_no AS rim, case when n.description in ('KUWAITI','SAUDI','OMANI','QATARI','EMARATI') then r.id_value else r.tin END cpr, r.Birth_dt, ad.phone_3 from phoenix..dp_acct a, phoenix..rm_acct r, phoenix..ad_rm_nat n, phoenix..rm_personal_info i, phoenix..rm_address ad
                        where
                        a.rim_no = r.rim_no and
                        r.rim_no = i.rim_no and
                        r.rim_no = ad.rim_no and
                        ad.addr_id = 1 and
                        ad.status='Active' and
                        i.nat_id = n.nat_id and
                        r.rim_type = 'Personal' and
                        r.status='Active' and
                        a.status='Active'""")
        #sybaseCursor.execute("SELECT d.acct_no AS acct_no, r.rim_no AS rim, LTRIM(RTRIM(r.tin)) AS cpr, r.Birth_dt FROM dp_acct AS d JOIN rm_acct AS r ON d.rim_no = r.rim_no and r.rim_type='Personal'")
        sybase_results = cursor.fetchall()
        log_info("Size of sybase read : " + str(len(sybase_results)))
    
        ebankingDBConn = open_ebanking_db()
        ebCursor = ebankingDBConn.cursor()
        log_info("Connection is established to postgres database.")
        
        upsert_query = """INSERT INTO eregister.card_temp_details(account_number, rim, dob, cpr, phone) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (account_number) DO UPDATE SET account_number = EXCLUDED.account_number, dob = EXCLUDED.dob, rim = EXCLUDED.rim, cpr = EXCLUDED.cpr, phone = EXCLUDED.phone"""
    
        total_upsertions_count = 0
        for chunk_of_rows in split_list_into_chunks(sybase_results, max_records_to_insert_in_db):
            upsert_data_tuples = []
            for cpr_rim_dob_row in chunk_of_rows:  
                upsert_data = (cpr_rim_dob_row[0], cpr_rim_dob_row[1], is_date(str(cpr_rim_dob_row[3])), cpr_rim_dob_row[2], cpr_rim_dob_row[4])
                upsert_data_tuples.append(upsert_data)
            
            try:
                ebCursor.executemany(upsert_query, upsert_data_tuples)
                ebankingDBConn.commit()
                    
                affected_rows = ebCursor.rowcount
                total_upsertions_count += affected_rows
                
            except psql.IntegrityError as e:
                log_exception("IntegrityError: input data is not as per expectation - ", e)
                exit_program()
            except psql.DatabaseError as e:
                log_exception("DatabaseError: ", e)
                exit_program()
            except Exception as e:
                log_exception("ERROR: unable to insert/update data into card_temp_details - ", e)
                exit_program()
        log_info("Total num of rows upserted from sybase db to card_temp_details : " + str(total_upsertions_count))
        
        close_psql_db(ebankingDBConn, ebCursor)
        close_sybase_db(sybaseDBConn, sybaseCursor)
    except Exception as e:
        close_psql_db(ebankingDBConn, ebCursor)
        close_sybase_db(sybaseDBConn, sybaseCursor)
        log_exception("ERROR: Something went wrong - ", e)
        exit_program()   

def save_cards_info(cards_data):
    ebankingDBConn = ebCursor = None

    try:
        ebankingDBConn = open_ebanking_db()
        ebCursor = ebankingDBConn.cursor()
        log_info("Connection is established to postgres database.")
           
        upsert_query = """INSERT INTO eregister.card_hash(account_number, card_exp_hash, rim, dob, cpr, phone) VALUES (%s, %s, %s, %s, %s, %s)"""

        total_upsertions_count = 0
    
        for chunk_of_rows in split_list_into_chunks(cards_data, max_records_in_chunk):
            account_numbers_list = []
            cards_list = []
            for row in chunk_of_rows:
                row_tokens = row.split(",")
                account_number = row_tokens[2].strip()
                if len(account_number) != 12 or not str(account_number).isnumeric():
                    log_warning("Invalid account_number is found in csv row : " + str(account_number))
                    continue
            
                card_number = row_tokens[0].strip()
                exp_date_str = row_tokens[3].strip()
                c = CardData(card_number, account_number, exp_date_str, None, None, None, None)
                cards_list.append(c)
                account_numbers_list.append(c.account_number)
            for card in cards_list:
                ebCursor.execute("select account_number, cpr, dob, rim, phone from eregister.card_temp_details where account_number = '" + card.account_number + "'")
                cpr_dob_rim_results = ebCursor.fetchall()
                
                if len(cpr_dob_rim_results) == 0:
                    log_warning("account_number " + str(card.account_number) + " is found in csv but not in card_temp_details table")
                else:
                    card.cpr = cpr_dob_rim_results[0][1]
                    card.dob = cpr_dob_rim_results[0][2]
                    card.rim = cpr_dob_rim_results[0][3]
                    card.phone = cpr_dob_rim_results[0][4]
                    if len(cpr_dob_rim_results) >= 2:
                        log_warning("Multiple records are found for card_number " + str(card.account_number) + " in card_temp_details table")
             

            for chunk_of_cards in split_list_into_chunks(cards_list, int(max_records_to_insert_in_db)):
                upsert_data_tuples = []             
                for card in chunk_of_cards:
                    hash_input = card.card_number + card.exp_date_str + salt_code
                    #log_info("TTTTTTTTTTTTTTTTT : " + hash_input)
                    hash_output = generate_sha256(hash_input)
            
                    upsert_data = (card.account_number, hash_output, card.rim, is_date(str(card.dob)), card.cpr, card.phone)
                    upsert_data_tuples.append(upsert_data)
            
                try:
                    #log_info("DDDDDDDDDDDDATA : " + str(upsert_data_tuples))
                    ebCursor.executemany(upsert_query, upsert_data_tuples)
                    ebankingDBConn.commit()
                    
                    affected_rows = ebCursor.rowcount
                    total_upsertions_count += affected_rows
                    log_info("Num of rows upserted in card_hash : " + str(affected_rows))
                except psql.IntegrityError as e:
                    log_exception("IntegrityError: input data is not as per expectation - ", e)
                    exit_program()
                except psql.DatabaseError as e:
                    log_exception("DatabaseError: ", e)
                    exit_program()
                except Exception as e:
                    log_exception("ERROR: unable to insert/update data in db - ", e)
                    exit_program()
                    
        log_info("Total num of rows upserted in card_hash: " + str(total_upsertions_count))
        
        close_psql_db(ebankingDBConn, ebCursor)
    except Exception as e:
        close_psql_db(ebankingDBConn, ebCursor)
        log_exception("ERROR: Something went wrong - ", e)
        exit_program()

def truncate_tables():
    ebanking_db_conn = ebanking_cursor = None
    try:
        ebanking_db_conn = open_ebanking_db()
        ebanking_cursor = ebanking_db_conn.cursor()

        ebanking_cursor.execute("TRUNCATE TABLE eregister.card_hash")
        ebanking_cursor.execute("TRUNCATE TABLE eregister.card_temp_details")
        ebanking_db_conn.commit()

        log_info("Truncated tables")
        close_psql_db(ebanking_db_conn, ebanking_cursor)
    except psql.IntegrityError as e:
        log_exception("IntegrityError: - ", e)
        close_psql_db(ebanking_db_conn, ebanking_cursor)
        exit_program()
    except psql.DatabaseError as e:
        log_exception("DatabaseError: ", e)
        close_psql_db(ebanking_db_conn, ebanking_cursor)
        exit_program()
    except Exception as e:
        log_exception("ERROR: Something went wrong - ", e)
        close_psql_db(ebanking_db_conn, ebanking_cursor)
        exit_program()

start_time = time.clock()
log_file = get_logs_folder_path() + os.path.sep + "sinnad_loading_" + date.today().strftime("%Y_%m_%d") + ".log"
logging.basicConfig(filename = log_file, level = logging.DEBUG, format = "%(asctime)s : %(levelname)s : %(message)s", filemode = 'a')

#downloaded_file ='/home/ebanking/scheduler/downloads/KFHD28122021_021201.CSV' #download_csvfile_from_sftp()
downloaded_file = download_csvfile_from_sftp()
cards_data = read_file_into_list(downloaded_file)
delete_file(downloaded_file)
if cards_data and len(cards_data) >= 1:
    truncate_tables()
    sync_details_from_sybase()
    save_cards_info(cards_data)
else:
    log_warning("No rows found in CSV")
log_info("Successfully completed the task. Time taken : " + str(time.clock() - start_time) + " seconds")
