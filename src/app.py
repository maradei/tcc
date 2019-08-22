import os

from flask import Flask

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config.from_object('sending_email')

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USERNAME": 'disopred.uesc@gmail.com',  # os.environ['MAIL_FLASK'],
    "MAIL_PASSWORD": 'diso-8372',  # os.environ['PSWD_FLASK']
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_ASCII_ATTACHMENTS": True
}

app.config.update(mail_settings)
