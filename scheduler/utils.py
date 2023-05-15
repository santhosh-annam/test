import sys, hashlib, uuid
import logging
from datetime import date
from configs import *
from dateutil.parser import parse
from utils import *

def log_info(msg):
    print(msg)
    logging.info(msg)

def log_warning(msg):
    print(msg)
    logging.warning(msg)
    
def log_error(msg):
    print(msg)
    logging.error(msg)
   
def log_exception(message, ex):
    print(message, ex)
    logging.exception(ex) 

def exit_program():
    msg = "Exiting from program"
    logging.critical(msg)
    sys.exit(msg)
    
def read_file_into_list(filepath):
    file = None
    try:
        file = open(filepath)
        cards_data = []
        for row in file:
            cards_data.append(row)
        
        file.close()
        return cards_data
    except Exception as e:
        if file: 
            file.close()
        log_exception("ERROR while reading csv file - " + filepath, e)
        exit_program()
        
        
def generate_sha256(input_string):
    hash_object = hashlib.sha256(input_string.encode())
    output = hash_object.hexdigest()
    return output

def generate_saltcode():
    return str(uuid.uuid4())

def split_list_into_chunks(input_list, chunk_size): 
    for i in range(0, len(input_list), chunk_size):
        yield input_list[i : i + chunk_size]
        
def is_date(string, fuzzy=False):
    try:
        parse(string, fuzzy=fuzzy)
        return string
    except ValueError:
        return None
