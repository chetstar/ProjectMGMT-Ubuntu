
CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'
WTF_CSRF_ENABLED = True
import os
basedir = os.path.abspath(os.path.dirname(__file__))
import os
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename

UPLOAD_FOLDER = 'app/static/img'
ALLOWED_EXTENSIONS = set(['TXT', 'PDF', 'PNG', 'JPG', 'JPEG', 'GIF'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
# SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

# from sqlalchemy import create_engine
# SQLALCHEMY_DATABASE_URI = create_engine("mssql+pyodbc://dashboarddatadev", encoding='windows-1255', convert_unicode=True)
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

SQLALCHEMY_DATABASE_URI = 'postgresql://chet@localhost/chet'

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
# SQLALCHEMY_BINDS = {
#     'request':      'sqlite:///' + os.path.join(basedir, 'app.db')
# }



# MAIL_SERVER = "allsmtp.acgov.org"
# MAIL_PORT = 25
# MAIL_USE_TLS = False
# MAIL_USE_SSL = False
# MAIL_USERNAME = 'you'
# MAIL_PASSWORD = 'your-password'

# # administrator list
# ADMINS = ['Chet@acbhcs.org']