from SalesforceUtilityTools import app
import logging, sys, re, json, html, flask
from SalesforceUtilityTools.models.salesforce.api import Salesforce
from SalesforceUtilityTools.models.salesforce.util import sfdcStr
from .masterController import masterController

class oauthLoginCtrl(masterController):
    """description of class"""

    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)

    def processRequest(self):
        request = flask.request

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

        flask.session['SalesforceAuthCode'] = authCode
        host = request.referrer.split('//')[1].split('.')[0]
        flask.session['SalesforceHostname'] = host
        flask.session.modified = True
        
        # Create hook to set cookie value
        @flask.after_this_request
        def add_header(response):
            response.set_cookie('SalesforceAuthCode', value=authCode)
            response.set_cookie('SalesforceHostname', value=host)
            return response

        return self.responseData