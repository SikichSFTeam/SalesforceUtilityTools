"""
The flask application package.
"""
import logging, sys
from flask import Flask
app = Flask(__name__)
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

from . import views
from SalesforceUtilityTools.controllers.tools import *