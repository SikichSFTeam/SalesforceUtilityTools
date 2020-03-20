from flask import request
from SalesforceUtilityTools import app
import logging, sys, re, json, html
from SalesforceUtilityTools.models.salesforce.api import Salesforce
from SalesforceUtilityTools.models.salesforce.util import sfdcStr

class cleanHtml(object):
    """description of class"""
    htmlTagList = ('!doctype','a','abbr','acronym','address','applet','area','article','aside','audio','b','base','basefont','bb','bdo','big','blockquote','body','br ','button','canvas','caption','center','cite','code','col','colgroup','command','datagrid','datalist','dd','del','details','dfn','dialog','dir','div','dl','dt','em','embed','eventsource','fieldset','figcaption','figure','font','footer','form','frame','frameset','h1','h2','h3','h4','h5','h6','head','header','hgroup','hr ','html','i','iframe','img','input','ins','isindex','kbd','keygen','label','legend','li','link','map','mark','menu','meta','meter','nav','noframes','noscript','object','ol','optgroup','option','output','p','param','pre','progress','q','rp','rt','ruby','s','samp','script','section','select','small','source','span','strike','strong','style','sub','sup','table','tbody','td','textarea','tfoot','th','thead','time','title','tr','track','tt','u','ul','var','video','wbr')

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

        htmlTagStr = '(' + '|'.join(cleanHtml.htmlTagList) + ')'
        reg = '<[ \/]?(.*?:)?'+ htmlTagStr +'[^<>]*>'

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
        elif not re.match('^[A-Za-z0-9_]+$', sfobject):
                responseData['isValid'] = False
                responseData['errorMessages'].append('Invalid object name: ' + sfobject + '.')

        if fields == '':
            responseData['isValid'] = False
            responseData['errorMessages'].append('At least one field is required.')

        fieldList = []
        for fld in fields.split(','):
            fld = fld.strip()
            if not re.match('^[A-Za-z0-9_]+$', fld):
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

        updateRecs = []
        while True:
            for rec in SfQry['records']:
                updRec = {
                        'Id': rec['Id'],
                    }
                for key, value in rec.items():
                    if key not in ['attributes', 'Id']:

                        if value is not None:
                            value = re.sub('<!--(\s|\S)*?-->', '', value)
                            value = re.sub(reg, '', value)
                            value = re.sub('(\\r\\n){3,}', '\\n\\n', value)
                            value = re.sub('(\\n){3,}', '\\n', value)
                            value = html.unescape(value)

                        updRec[key] = value

                updRec = sfdcStr(updRec)
                updateRecs.append(updRec)
            if SfQry['done'] == False:
                SfQry = sf.query_more(SfQry['nextRecordsUrl'], True)
            else:
                break

        responseData['debugMessages'] = []
        logger = logging.getLogger()
        
        if logger.getEffectiveLevel() <= logging.DEBUG:
            for rec in updateRecs:
                if len(responseData['debugMessages']) > 500:
                    break
                responseData['debugMessages'].append(json.dumps(rec))

            
        #app.logger.debug('sfuser:' + sfuser)


        return responseData
        
        

