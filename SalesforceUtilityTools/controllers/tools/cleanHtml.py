from flask import request
from SalesforceUtilityTools import app
import logging, sys, re, json, html
from SalesforceUtilityTools.models.salesforce.api import Salesforce
from SalesforceUtilityTools.models.salesforce.util import sfdcStr
from .sfToolController import sfToolController

class cleanHtml(sfToolController):
    """description of class"""
    htmlTagList = ('!doctype','a','abbr','acronym','address','applet','area','article','aside','audio','b','base','basefont','bb','bdo','big','blockquote','body','br ','button','canvas','caption','center','cite','code','col','colgroup','command','datagrid','datalist','dd','del','details','dfn','dialog','dir','div','dl','dt','em','embed','eventsource','fieldset','figcaption','figure','font','footer','form','frame','frameset','h1','h2','h3','h4','h5','h6','head','header','hgroup','hr ','html','i','iframe','img','input','ins','isindex','kbd','keygen','label','legend','li','link','map','mark','menu','meta','meter','nav','noframes','noscript','object','ol','optgroup','option','output','p','param','pre','progress','q','rp','rt','ruby','s','samp','script','section','select','small','source','span','strike','strong','style','sub','sup','table','tbody','td','textarea','tfoot','th','thead','time','title','tr','track','tt','u','ul','var','video','wbr')

    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)

    def processRequest(self):

        if request.method != 'POST':
            self.responseData['isValid'] = False
            return self.responseData

        htmlTagStr = '(' + '|'.join(cleanHtml.htmlTagList) + ')'
        reg = '<[ \/]?(.*?:)?'+ htmlTagStr +'[^<>]*>'

         
        sfobject = request.form['object'] if 'object' in request.form.keys() else ''
        fields = request.form['fields'] if 'fields' in request.form.keys() else ''
        performUpdate = request.form['performUpdate'] if 'performUpdate' in request.form.keys() else False

        # Input Validation

        self.handleFormLogin()
        if not self.responseData['isValid']:
            return self.responseData

        if sfobject == '':
            self.responseData['isValid'] = False
            self.responseData['validationErrors'].append('Object is required.')
        elif not re.match('^[A-Za-z0-9_]+$', sfobject):
                self.responseData['isValid'] = False
                self.responseData['validationErrors'].append('Invalid object name: ' + sfobject + '.')

        if fields == '':
            self.responseData['isValid'] = False
            self.responseData['validationErrors'].append('At least one field is required.')

        fieldList = []
        for fld in fields.split(','):
            fld = fld.strip()
            if not re.match('^[A-Za-z0-9_]+$', fld):
                self.responseData['isValid'] = False
                self.responseData['validationErrors'].append('Invalid field name: ' + fld + '.')
            else:
                fieldList.append(fld)

        if not self.responseData['isValid']:
            return self.responseData

        # End Input Validation

        fields = ', '.join(fieldList)

        query = "select Id, {0} from {1}".format(fields, sfobject)
        SfQry = self.sf.query(query)

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
                SfQry = self.sf.query_more(SfQry['nextRecordsUrl'], True)
            else:
                break

        self.responseData['preview'] = []
        self.responseData['errors'] = []
        if not performUpdate:
            for rec in updateRecs:
                self.responseData['preview'].append(rec)
        else:
            sfResponse = self.sf.bulk.__getattr__(sfobject).update(updateRecs)

            for i in range(len(sfResponse)):
                if sfResponse[i]['success'] == False:
                    try:
                        r = {
                                'errors': sfResponse[i]['errors']
                            }
                        for key, value in sfResponse[i].items():
                            r[key] = value

                        self.responseData['errors'].append(r)
                    except:
                        self.responseData['errors'].append(
                                sfResponse[i]['errors']
                            )
            
        return self.responseData
        
        

