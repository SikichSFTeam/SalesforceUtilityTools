import flask
from SalesforceUtilityTools import app
from ..masterController import masterController
import logging, sys, re, json, html
from SalesforceUtilityTools.models.salesforce.api import Salesforce
from SalesforceUtilityTools.models.salesforce.util import sfdcStr

class sfToolController(masterController):
    sf = None
    SalesforceAuthCode = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'SalesforceAuthCode' in flask.session:
            self.SalesforceAuthCode = flask.session['SalesforceAuthCode']
            self.SalesforceInstance = flask.session['SalesforceInstance']

        return


    def handleFormLogin(self):
        if self.SalesforceAuthCode is not None:
            self.sf = Salesforce(session_id=self.SalesforceAuthCode, instance_url=self.SalesforceInstance)

        else:
            sfuser = flask.request.form['username'] if 'username' in flask.request.form.keys() else ''
            sfpass = flask.request.form['password'] if 'password' in flask.request.form.keys() else ''
            sftoken = flask.request.form['token'] if 'token' in flask.request.form.keys() else ''
            sfdomain = flask.request.form['domain'] if 'domain' in flask.request.form.keys() else ''

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


