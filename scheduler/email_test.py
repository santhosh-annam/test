import smtplib

sender = 'ebanking@kfhbonline.com'
receivers = ['visu@pronteff.com','amathew@kfh.com.bh','jbuhayal@kfh.com.bh','zazmi@kfh.com.bh']

message = """From: ERegistration <from@fromdomain.com>
To: Viswanath <visu@pronteff.com>
Subject: SMTP e-mail test

This is a test e-mail message from KFHB e-registration.
"""

try:
   smtpObj = smtplib.SMTP('10.9.1.32','25')
   smtpObj.sendmail(sender, receivers, message)         
   print("Successfully sent email")
except smtplib.SMTPException as e:
   print("Error: unable to send email ", e)