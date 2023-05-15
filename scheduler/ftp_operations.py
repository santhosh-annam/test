from configs import *
from utils import *
from datetime import datetime
import paramiko
import os

DOWNLOADS_FOLDER_PATH = str(os.path.dirname(os.path.abspath(__file__))) + os.path.sep + "downloads" + os.path.sep
LOGS_FOLDER_PATH      = str(os.path.dirname(os.path.abspath(__file__))) + os.path.sep + "logs"

def delete_file(file_path):
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            log_info("File deleted : " + file_path)
        except OSError as e: 
            log_exception("Unable to delete file : ", e)
    else:
        log_warning("File does not exist : " + file_path)

def create_folder_if_required(folder_path):
    if not os.path.exists(folder_path):
        try:
            os.makedirs(folder_path)
            log_info("Folder is Created at " + folder_path)
            return folder_path
        except OSError as e:
            log_exception("Unable to create folder : ", e)
            exit_program()
    else:
        return folder_path

def get_downloads_folder_path(): 
    return create_folder_if_required(DOWNLOADS_FOLDER_PATH)

def get_logs_folder_path():
    return create_folder_if_required(LOGS_FOLDER_PATH)

def download_csvfile_from_sftp():
    try:
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect("10.114.114.100", username = "KFH0011", password = "Kfh@1234", timeout=10)
        sftp = ssh.open_sftp()

        csv_folder_path = "/04-KFH/Production/Outbound/DAILY_CSV/"
        csv_file_name = datetime.today().strftime('KFHD%d%m%Y.CSV')
        local_downloads_folder = get_downloads_folder_path()
        
        csv_files = sftp.listdir(csv_folder_path)
        for filename in csv_files:
            if filename.__contains__("_") and filename.__contains__("."):
                if filename.split("_")[0] == csv_file_name.split(".")[0] and filename.split(".")[1] == csv_file_name.split(".")[1]:
                    csv_file_name = filename;
                    break
        
        downloaded_file = local_downloads_folder + csv_file_name
        sftp.get(csv_folder_path + csv_file_name, downloaded_file)
        sftp.close()
        return downloaded_file
    except Exception as e:
        log_exception("Error while downloading the file from SFTP server : ", e)
        exit_program()
        
