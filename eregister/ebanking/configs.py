SALT_CODE = "***KFHB-sinnad-salt***"

# DB CONFIGURATION
DB_USERNAME = "postgres"
DB_PASSWORD = "Z1I4X29lNWNlb3F2c2t1N29pX0ZvcmdvdFBhcw=="
DB_PORT = "5432"
DB_HOST = "10.11.1.12"
DB_NAME = "main"
TB_NAME_CARD_HASH = "eregister.card_hash"
TB_NAME_AUTH_REQUESTS = "eregister.auth_requests"


# OPERATIONAL_MODE
EXECUTION_MODE = 1  # 0 for Stand alone and 1 for Integrated

# CHANNEL SETTINGS
ALLOWED_CHANNELS = {"ebankingRegistor": "https://www.kfhbonline.com/retail/OnlineRegServlet", "ebankingForget" : "https://www.kfhbonline.com/retail/ForgetPassServlet"}

# SMTP
SMTP_HOST = '10.9.1.32'
SMTP_PORT = '25'
SMTP_TIMEOUT_SECS = 10
EMAIL_SENDER = 'ebanking@kfhbonline.com'
EMAIL_RECIPIENTS = ['msallam@kfh.com.bh',
                    'amathew@kfh.com.bh',
                    'jbuhayal@kfh.com.bh',
                    'zazmi@kfh.com.bh']
CSP_VIOLATION_EMAIL_SENDER = EMAIL_SENDER
CSP_VIOLATION_EMAIL_RECIPIENTS = EMAIL_RECIPIENTS
