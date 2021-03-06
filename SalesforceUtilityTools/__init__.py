"""
The flask application package.
"""
import logging, sys, os
from flask import Flask
app = Flask(__name__)
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

secret = ''
with open('secret_key.txt', mode='w+') as secretFile:
    secret = secretFile.readline().strip()
    if secret is None or secret == '':
        secret = str(os.urandom(32)).strip()
        secretFile.writelines([secret])

app.config['SECRET_KEY'] = secret
Flask.secret_key = secret

from . import views
from SalesforceUtilityTools.controllers import *