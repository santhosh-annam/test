import smtplib
from ebanking.configs import SMTP_HOST
from ebanking.configs import SMTP_PORT
from ebanking.configs import SMTP_TIMEOUT_SECS
from ebanking.configs import EMAIL_RECIPIENTS
from ebanking.configs import EMAIL_SENDER
from ebanking.configs import CSP_VIOLATION_EMAIL_RECIPIENTS
from ebanking.configs import CSP_VIOLATION_EMAIL_SENDER


msg = """From: ERegistration <eregister@kfhbonline.com>
To: Viswanath <visu@pronteff.com>
Subject: Customer Authentication Status

Dear Customer Care Executive,

Please find below the account authentication status of the customer.
        Account Number - {0}
        RIM - {1}
        CPR - {2}
        Channel - {3}
        Phone number - {4}
        Authentication Status - Success


This is an auto generated email.
"""


def shoot_email(account_id, cpr, rim, channel, phone):

    message = msg.format(account_id, rim, cpr, channel, phone)

    try:
        smtp_obj = smtplib.SMTP(SMTP_HOST,
                                SMTP_PORT,
                                timeout=SMTP_TIMEOUT_SECS)
        smtp_obj.sendmail(EMAIL_SENDER, EMAIL_RECIPIENTS, message)
        smtp_obj.quit()
        print("Successfully sent email")
    except smtplib.SMTPException as e:
        print("Error: unable to send email ", e)

csp_msg = """From: ERegistration <eregister@kfhbonline.com>
To: Viswanath <visu@pronteff.com>
Subject: Content-Security-Policy violation on {0}

Hello,

The following Content-Security-Policy violation occurred on {1}.
        {2}


This is an auto generated email.
"""


def shoot_csp_violation_email(domain, violation_data):
    message = csp_msg.format(domain, domain, violation_data)
    try:
        smtp_obj = smtplib.SMTP(SMTP_HOST,
                                SMTP_PORT,
                                timeout=SMTP_TIMEOUT_SECS)
        smtp_obj.sendmail(CSP_VIOLATION_EMAIL_SENDER,
                          CSP_VIOLATION_EMAIL_RECIPIENTS,
                          message)
        smtp_obj.quit()
        print("Successfully sent email")
    except smtplib.SMTPException as e:
        print("Error: unable to send email ", e)
