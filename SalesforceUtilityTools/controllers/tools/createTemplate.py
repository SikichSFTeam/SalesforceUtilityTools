import logging, sys, html, csv, io, zipfile
from flask import request
from SalesforceUtilityTools import app
from SalesforceUtilityTools.models.salesforce.api import Salesforce
from SalesforceUtilityTools.models.salesforce.util import sfdcStr
from .sfToolController import sfToolController

class createTemplate(sfToolController):
    """Class to control createTemplate page"""

    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)

    def processRequest(self):
        if request.method != 'POST':
            self.responseData['isValid'] = False
            return self.responseData

        sfobjects = request.form['objects'].split(',') if 'objects' in request.form.keys() else ''

        zipFile = io.BytesIO()
        recordTypes = ''
        with zipfile.ZipFile(zipFile, 'w', compression=zipfile.ZIP_DEFLATED) as zip:
            for obj in sfobjects:
                desc = self.sf.__getattr__(obj).describe()
                objectName = desc['name']
                fields = parseDesc(desc)
                data = writeCsv(fields, objectName)
                with io.StringIO() as csvFile:
                    csvWtr = csv.writer(csvFile)
                    csvWtr.writerows(data)
                    zip.write(csvFile,arcname=objectName+'.csv')

                recordTypes += obj + ' Record Types'
                for rt in desc['recordTypeInfos']:
                    if not rt['available']:
                        continue
        
                    recordTypes += '  name' + ': ' + str(rt['name'])
                    recordTypes += '    default' + ': ' + str(rt['defaultRecordTypeMapping'])
                    recordTypes += '    recordTypeId' + ': ' + str(rt['recordTypeId'])

            print(recordTypes)
            with io.StringIO() as textFile:
                textFile.writelines(recordTypes)
                zip.write(textFile,arcname='RecordTypes.txt')

        self.responseData['file'] = zipFile

    def parseDesc(desc):
        output = [[],[],[],[]]
        for fld in desc['fields']:
            if not fld['updateable'] and not fld['createable']:
                continue
        
            #UI Label
            output[0].append(fld['label'])
        
            #Data Type
            if fld['precision'] != 0  or fld['scale'] != 0:
                output[1].append(fld['type'] + '(' + str(fld['precision']) + ',' + str(fld['scale']) + ')')
            elif fld['length'] != 0:
                output[1].append(fld['type'] + '(' + str(fld['length']) + ')')
            else:
                output[1].append(fld['type'])

            # Update/Create
            output[2].append(('Updateable ' if fld['updateable'] else '') + ('Creatable ' if fld['createable'] else '') + ('ExternalID ' if fld['externalId'] else ''))

            # Field API Name (keep last)
            output[3].append(fld['name'])

            if fld['relationshipName'] is not None:
                #UI Label
                output[0].append(fld['label'])

                #Data Type
                output[1].append(', '.join(fld['referenceTo']) + ' via External Id')

                # Update/Create
                output[2].append(('Updateable ' if fld['updateable'] else '') + ('Creatable ' if fld['createable'] else '') + ('ExternalID ' if fld['externalId'] else ''))

                # Field API Name (keep last)
                output[3].append(fld['relationshipName'] + '.<ExternalIdField>')

        return output
