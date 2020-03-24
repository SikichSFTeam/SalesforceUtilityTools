"""
Routes and views for the flask application.

Add each endpoint to this file.  Add a call to a controller to add dynamic logic if needed.
"""

from datetime import datetime
from flask import render_template
from flask import request
from SalesforceUtilityTools import app
from SalesforceUtilityTools.controllers import *
import sys, logging, yaml

def _init():
    with open('config.yaml','r') as cfgFile:
        config = yaml.load(cfgFile, Loader=yaml.SafeLoader)

    viewData = {
            'title': 'Sikich Utility Tools',
            'year': datetime.now().year,
            'sfClientId': config['salesforce']['consumerKey'],
            'sfClientSecret': config['salesforce']['consumerSecret'],
        }

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
    viewData['title']='About'

    cntlr = oauthLoginCtrl()
    responseData = cntlr.processRequest()

    if responseData['isValid']:
        pass


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

    return render_template(
        'tools/createTemplate.html',
        viewData=viewData,
        responseData=responseData,
    )