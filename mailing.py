import smtplib
from email.mime.text import MIMEText
import config

cfg = config.Config()

class Mailing:
    def __init__(self):
        return

    def mail_list(self):
        fp = open(cfg.get_file('text'), 'rb')
        mail_msg = MIMEText(fp.read())
        fp.close()

        mail_msg['Subject'] = 'Nano Shopping List - ' + time.strftime("%d/%m/%Y")
        mail_msg['From'] = cfg.get_mail('from')
        mail_msg['To'] = cfg.get_mail('to')

        smtp = smtplib.SMTP('127.0.0.1', 25)
        smtp.sendmail(mail_from, [mail_to], mail_msg.as_string())
        smtp.quit()
