#=======FTP CONFIGURATIONS==================
ftp_host = "" 
ftp_username = ""
ftp_password = ""

#======FILE PATHS CONFIGURATIONS==============
local_dir = "/var/www/html/attachments/"
ftp_file_name = "cards.csv"
ftp_dir_path = "/home/devrabbit/ftp/files/"
exp_date_format = "%d-%b" #Expiration date format
dob_date_format = "%m/%d/%Y"
salt_code = "***KFHB-sinnad-salt***"

#leave it empty to create log files in same location of python scripts
log_file_dir_path = "" #

##=============Main PSQL DB CONFIGURATIONS=========== 
db_username = "eregister"
db_password = "gR8_oe5ceoqvsku7oi_ForgotPas"
db_port = "5432" #default Postgres port
db_host = "10.11.1.12"
db_name = "main"
other_db_name = "secondary_db"

##=============DB CONFIGURATIONS=========== 
sybase_host = "10.6.2.6"
sybase_prt = "10001"
sybase_usr = "eregister"
sybase_passwd = "ERE_kfH@Hfk_698269"
sybase_db = "phoenix"
sybase_driver = "FreeTDS"

###==========CHUNK CONFIGURATION=================
max_records_in_chunk = 5000
max_records_to_insert_in_db = 1000


