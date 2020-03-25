import flask
from SalesforceUtilityTools import app
import logging, sys, re, json, html

class masterController(object):
    """description of class"""
    responseData = {}

    def __init__(self, *args, **kwargs):
        self.responseData = {
            'isValid': True,
            'validationErrors': []
        }

        return super().__init__(*args, **kwargs)


