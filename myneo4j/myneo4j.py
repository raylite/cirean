#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 15:08:55 2019

@author: ja18581
"""

from neo4j import GraphDatabase
from flask import current_app

try:
    from flask import _app_ctx_stack as stack
except:
    from flask import _request_ctx_stack as stack
    
    
class Neo4j(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)
        else:
            self.driver = None
            
    def init_app(self, app):
        self.driver = None
        
        if hasattr(app, 'teardown_appcontext'):
            app.teardown_appcontext(self.teardown)
        else:
            app.teardown_request(self.teardown)
    
    def connect(self):
        self.driver = GraphDatabase.driver(current_app.config['NEO4J_URL'], 
                                           auth=(current_app.config['NEO4J_USERNAME'],
                                           current_app.config['NEO4J_PASSWORD']))
        return self.driver
        
    #@current_app.teardown_appcontext    
    def teardown(self, exception):
        ctx = stack.top
        if hasattr(ctx, 'neo4j_db'):
            ctx.neo4j_db.close()
            
    @property
    def connection(self):
        ctx = stack.top
        if ctx is not None:
            if not hasattr(ctx, 'neo4j_db'):
                ctx.neo4j_db = self.connect().session()
            return ctx.neo4j_db
