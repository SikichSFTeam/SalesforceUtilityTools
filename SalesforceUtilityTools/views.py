"""
Routes and views for the flask application.

Add each endpoint to this file.  Add a call to a controller to add dynamic logic if needed.
"""

from datetime import datetime
from flask import render_template
from flask import request
from SalesforceUtilityTools import app
from SalesforceUtilityTools.controllers import *
import sys, logging

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/oathLogin', methods=['POST', 'GET'])
def oathLogin():
    cntlr = oauthLoginCtrl()
    responseData = cntlr.processRequest()

    if responseData['isValid']:
        pass


@app.route('/tools/cleanHtml', methods=['POST', 'GET'])
def tools_cleanHtml():
    cntlr = tools.cleanHtml()
    responseData = cntlr.processRequest()

    if responseData['isValid']:
        pass

    return render_template(
        'tools/cleanHtml.html',
        title='Clean Html',
        year=datetime.now().year,
        responseData=responseData,
    )

@app.route('/tools/createTemplate', methods=['POST', 'GET'])
def tools_createTemplate():
    cntlr = tools.createTemplate()
    responseData = cntlr.processRequest()

    if responseData['isValid']:
        pass

    return render_template(
        'tools/createTemplate.html',
        title='Create Template',
        year=datetime.now().year,
        responseData=responseData,
    )