from SalesforceUtilityTools import app
import logging, sys, re, json, html, flask, requests
from SalesforceUtilityTools.models.salesforce.api import Salesforce
from SalesforceUtilityTools.models.salesforce.util import sfdcStr
from .masterController import masterController
from flask import request

class oauthLoginCtrl(masterController):
    """description of class"""

    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)

    def processRequest(self):
        print('Form...')
        for key, value in request.form.items():
            print('    ' + key + ': ' + value)

        print('Args...')
        for key, value in request.args.items():
            print('    ' + key + ': ' + value)

        authCode = None
        if 'code' in request.form.keys():
            code = request.form['code']
        elif request.method == 'GET' and 'code' in request.args.keys():
            code = request.args['code']
        
        host = request.referrer.split('//')[1].split('/')[0]
        query = 'https://' + host + '/services/oauth2/token'
        data = {
            'grant_type':'authorization_code',
            'code': code,
            'client_id': self.config['salesforce']['consumerKey'],
            'client_secret': self.config['salesforce']['consumerSecret'],
            'redirect_uri': flask.url_for('oathLogin',_external=True),
            '': ''
            }
        head = {
                'Content-type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json',
            }
        resp = requests.post(query,data,headers=head)
        
        if resp.status_code != 200:
            # This means something went wrong.
            raise ErrorConnectionError('GET ' +url+ ' {}'.format(resp.status_code))
        
        rd = resp.json()
        accessToken = rd['access_token']
        print('accessToken:' + accessToken)
        instance = rd['instance_url']


        if authCode is None:
            return self.responseData

        flask.session['SalesforceAuthCode'] = accessToken
        flask.session['SalesforceInstance'] = instance
        flask.session.modified = True
        
        # Create hook to set cookie value
        #@flask.after_this_request
        #def add_header(response):
        #    response.set_cookie('SalesforceAuthCode', value=authCode)
        #    response.set_cookie('SalesforceInstance', value=instance)
        #    return response

        return self.responseData