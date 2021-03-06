"""
Routes and views for the flask application.

Add each endpoint to this file.  Add a call to a controller to add dynamic logic if needed.
"""

from datetime import datetime
from flask import render_template
from flask import request
import flask
from SalesforceUtilityTools import app
from SalesforceUtilityTools.controllers import *
import sys, logging, yaml

with open('config.yaml','r') as cfgFile:
    config = yaml.load(cfgFile, Loader=yaml.SafeLoader)

def _init():
    viewData = {
            'title': 'Sikich Utility Tools',
            'year': datetime.now().year,
            'sfClientId': config['salesforce']['consumerKey'],
            'sfClientSecret': config['salesforce']['consumerSecret'],
        }

    if 'SalesforceAuthCode' in flask.session.keys() and flask.session['SalesforceAuthCode'] is not None and flask.session['SalesforceAuthCode'] != '':
        viewData['IsSalesforceAuthed'] = True
    elif request.cookies.get('SalesforceAuthCode') is not None:
        viewData['IsSalesforceAuthed'] = True
        flask.session['SalesforceAuthCode'] = request.cookies.get('SalesforceAuthCode')
        flask.session['SalesforceInstance'] = request.cookies.get('SalesforceInstance')
        flask.session.modified = True
    else:
        viewData['IsSalesforceAuthed'] = False

    if 'SalesforceInstance' in flask.session.keys():
        viewData['SalesforceInstance'] = flask.session['SalesforceInstance']
    else:
        viewData['SalesforceInstance'] = ''

    return viewData

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    viewData = _init()
    return render_template(
        'index.html',
        viewData=viewData,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    viewData = _init()
    viewData['title'] = 'Contact'

    return render_template(
        'contact.html',
        viewData=viewData,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    viewData = _init()
    viewData['title']='About'

    return render_template(
        'about.html',
        viewData=viewData,
        message='Your application description page.'
    )

@app.route('/oathLogin', methods=['POST', 'GET'])
def oathLogin():
    viewData = _init()
    viewData['title']='Login'

    cntlr = oauthLoginCtrl(config=config)
    responseData = cntlr.processRequest()

    if responseData['isValid']:
        if 'state' in request.args.keys():
            return flask.redirect('/' + request.args['state'])
        else:
            return flask.redirect('/')

@app.route('/logout', methods=['POST', 'GET'])
def logout():
    viewData = _init()

    flask.session['SalesforceAuthCode'] = None
    flask.session['SalesforceHostname'] = None
    flask.session.modified = True
    return flask.redirect('/')

@app.route('/tools/cleanHtml', methods=['POST', 'GET'])
def tools_cleanHtml():
    viewData = _init()
    viewData['title']='Clean Html'

    cntlr = tools.cleanHtml()
    responseData = cntlr.processRequest()

    if responseData['isValid']:
        pass

    return render_template(
        'tools/cleanHtml.html',
        viewData=viewData,
        responseData=responseData,
    )

@app.route('/tools/createTemplate', methods=['POST', 'GET'])
def tools_createTemplate():
    viewData = _init()
    viewData['title']='Create Template'

    cntlr = tools.createTemplate()
    responseData = cntlr.processRequest()

    if responseData['isValid']:
        pass

    if 'file' in responseData and responseData['file'] is not None:
        return send_file(responseData['file'], mimetype='application/zip', attachment_filename='templates.zip')

    return render_template(
        'tools/createTemplate.html',
        viewData=viewData,
        responseData=responseData,
    )