import flask
from SalesforceUtilityTools import app
import logging, sys, re, json, html

class masterController(object):
    """description of class"""
    responseData = {}

    def __init__(self, *args, **kwargs):
        super().__init__()

        self.responseData = {
            'isValid': True,
            'validationErrors': []
        }
        if 'config' in kwargs:
            self.config = kwargs['config']

        return 


