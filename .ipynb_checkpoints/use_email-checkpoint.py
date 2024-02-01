import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

GMAIL = 'atsuto2002@gmail.com' # 上記でパスワードを発行したアカウントアドレスを記入
PASSWORD = 'zibc hmir jzvh pbmi'
MAIL_TO_ME = 'atsuto2002@gmail.com'
SUBJECT_TO_ME = 'おかえり'
MAILBODY_TO_ME = 'ご勤務お疲れ様です'
TRIGGER = 'trigger@applet.ifttt.com'
SUBJECT_ME_TO_TRIGGER = '#me'
SUBJECT_FRIEND_TO_TRIGGER = '#friend'
MAILBODY_TO_TRIGGER = ''

def use_email(mail_to=MAIL_TO_ME, subject=SUBJECT_TO_ME, mail_body=MAILBODY_TO_ME, img_path=None):
    message = setup_mail(subject, mail_to, mail_body)
    attach_img(message, img_path)
    send_mail(message)
    return


def setup_mail(subject, mail_to, mail_body):
    message = MIMEMultipart()
    message["Subject"] = subject
    message["To"] = mail_to
    message["From"] = GMAIL
    message.attach(MIMEText(mail_body, "html"))
    return message


def send_mail(message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(GMAIL, PASSWORD)
    server.send_message(message)
    server.quit()

def attach_img(message, img_path):
    if img_path is None:
        return
    with open(img_path, 'rb') as f:
        img = f.read()
    image = MIMEImage(img, name=img_path)
    message.attach(image)
    return