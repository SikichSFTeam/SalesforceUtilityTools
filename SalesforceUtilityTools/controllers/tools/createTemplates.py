class createTemplates(object):
    """Class to control createTemplates page"""

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

    def processRequest():
        if request.method != 'POST':
            self.responseData['isValid'] = False
            return self.responseData
