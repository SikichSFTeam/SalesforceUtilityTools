from flask import request
from SalesforceUtilityTools import app
import logging, sys, re, json
from SalesforceUtilityTools.models.salesforce.api import Salesforce

class cleanHtml(object):
    """description of class"""

    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)

    def processRequest():
        responseData = {
                'isValid': True,
                'errorMessages': []
            }

        if request.method != 'POST':
            responseData['isValid'] = False
            return responseData

        sfuser = request.form['username'] if 'username' in request.form.keys() else ''
        sfpass = request.form['password'] if 'password' in request.form.keys() else ''
        sftoken = request.form['token'] if 'token' in request.form.keys() else ''
        sfdomain = request.form['domain'] if 'domain' in request.form.keys() else ''
        sfobject = request.form['object'] if 'object' in request.form.keys() else ''
        fields = request.form['fields'] if 'fields' in request.form.keys() else ''

        # Input Validation

        if sfuser == '':
            responseData['isValid'] = False
            responseData['errorMessages'].append('Username is required.')

        if sfpass == '':
            responseData['isValid'] = False
            responseData['errorMessages'].append('Password is required.')

        if sftoken == '':
            responseData['isValid'] = False
            responseData['errorMessages'].append('Token is required.')

        if sfdomain == '':
            responseData['isValid'] = False
            responseData['errorMessages'].append('Domain is required.')

        if sfobject == '':
            responseData['isValid'] = False
            responseData['errorMessages'].append('Object is required.')
        elif not re.match('^[A-Za-z0-9_]*$', sfobject):
                responseData['isValid'] = False
                responseData['errorMessages'].append('Invalid object name: ' + sfobject + '.')

        if fields == '':
            responseData['isValid'] = False
            responseData['errorMessages'].append('At least one field is required.')

        fieldList = []
        for fld in fields.split(','):
            fld = fld.strip()
            if not re.match('^[A-Za-z0-9_]$', fld):
                responseData['isValid'] = False
                responseData['errorMessages'].append('Invalid field name: ' + fld + '.')
            else:
                fieldList.append(fld)

        if not responseData['isValid']:
            return responseData

        # End Input Validation

        sf = Salesforce(username=sfuser, password=sfpass, security_token=sftoken, domain=sfdomain)

        fields = ', '.join(fieldList)

        query = "select Id, {0} from {1}".format(fields, sfobject)
        SfQry = sf.query(query)

        while True:
            for rec in SfQry['records']:
                app.logger.debug(json.dumps(rec))
            if SfQry['done'] == False:
                SfQry = sf.query_more(SfQry['nextRecordsUrl'], True)
            else:
                break

        #app.logger.debug('sfuser:' + sfuser)


        return responseData
        
        

