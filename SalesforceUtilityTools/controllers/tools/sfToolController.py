from flask import request
from SalesforceUtilityTools import app
from ..masterController import masterController
import logging, sys, re, json, html
from SalesforceUtilityTools.models.salesforce.api import Salesforce
from SalesforceUtilityTools.models.salesforce.util import sfdcStr

class sfToolController(masterController):
    sf = None

    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)


    def handleFormLogin(self):
        sfuser = request.form['username'] if 'username' in request.form.keys() else ''
        sfpass = request.form['password'] if 'password' in request.form.keys() else ''
        sftoken = request.form['token'] if 'token' in request.form.keys() else ''
        sfdomain = request.form['domain'] if 'domain' in request.form.keys() else ''

        # Input Validation

        if sfuser == '':
            self.responseData['isValid'] = False
            self.responseData['validationErrors'].append('Username is required.')

        if sfpass == '':
            self.responseData['isValid'] = False
            self.responseData['validationErrors'].append('Password is required.')

        if sftoken == '':
            self.responseData['isValid'] = False
            self.responseData['validationErrors'].append('Token is required.')

        if sfdomain == '':
            self.responseData['isValid'] = False
            self.responseData['validationErrors'].append('Domain is required.')

        if self.responseData['isValid']:
            self.sf = Salesforce(username=sfuser, password=sfpass, security_token=sftoken, domain=sfdomain)


