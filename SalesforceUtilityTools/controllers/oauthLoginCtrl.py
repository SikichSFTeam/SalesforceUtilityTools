from flask import request, response
from SalesforceUtilityTools import app
import logging, sys, re, json, html
from SalesforceUtilityTools.models.salesforce.api import Salesforce
from SalesforceUtilityTools.models.salesforce.util import sfdcStr

class oauthLoginCtrl(object):
    """description of class"""

    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)

    def processRequest():

        print('Form...')
        for key, value in request.form.items():
            print('    ' + key + ': ' + value)

        print('Args...')
        for key, value in request.args.items():
            print('    ' + key + ': ' + value)

        authCode = None
        if request.method == 'POST' and 'code' in request.form.keys():
            authCode = request.form['code']
        elif request.method == 'GET' and 'code' in request.args.keys():
            authCode = request.args['code']

        if authCode is None:
            return 


        response.set_cookie('SalesforceAuthCode', value=authCode)