 #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 12:24:40 2018

@author: kazeem
"""
from cirean import db
import json


class Publisher():
    def __init__(self, name=None):
        print("HERE")
        self.name = name
        self.db = db.connection
        
    def find(self):
        publisher = self.db.run("MATCH (p:Publisher{name:{name}})"
                           "RETURN id(p)", name=self.name)
        if publisher:
            return publisher
        else:
            return None
        
    def create_publisher(self):
        tx = self.db.begin_transaction()
        self._createDbNode(tx)
            #self.set_publisher_name(tx, node_id)
        tx.commit()
        print ("Committed")
        
            
    def _createDbNode(self, tx):
        print('creating publisher')
        tx.run("MERGE (p:Publisher {name: {name}})", 
                       name=self.name)
                           
        
    @staticmethod
    def get_publisher(name):
        results = db.connection.run("MATCH (p:Publisher {name: {name}})"
                                     "RETURN p as publisher;", {'name': name})
        
        return Publisher.serialize(results.single()['publisher']) 
    
    @staticmethod
    def serialize(publisher):
        return {
                'name': publisher['name']
                }
            
    @staticmethod
    def get_all_publishers():
        results = db.connection.run("MATCH (p:Publisher)"
                                     "RETURN p as publisher;")
        
        return [Publisher.serialize(result['publisher']) for result in results] 
    
    
class Article():
    def __init__(self, pmid=None, title=None, pub_date=None, authors=None, doi=None, issn=None):
        self.pmid = pmid
        self.title = title
        self.pub_date = pub_date
        self.authors = authors
        self.issn = issn
        self.doi = doi
        self.db = db.connection
    
    def create_article(self):
        tx = self.db.begin_transaction()
        
        self._createArticleNode(tx)
        tx.commit()
        print ("Article creation Committed")
        
    def _createArticleNode(self, tx):
        tx.run("MERGE (a:Article {pmid: {pmid}, title: {title}, pub_date:{pub_date}, authors:{authors},\
                                   issn:{issn}, doi:{doi}});", pmid = self.pmid, title = self.title, 
               pub_date = self.pub_date, authors = self.authors, issn = self.issn, doi = self.doi)
    
           
        
    def find(self):#
        article = self.db.run("MATCH (a:Article {pmid:{pmid}})"
                           "RETURN id(a);", pmid=self.pmid)
        if article:
            return article
        else:
            return None
    
    def create_article_publisher_rel(self, publisher):
        self.db.run("MATCH (a:Article{pmid:{pmid}})"
                    "MATCH (p:Publisher{name:{name}})"
                    "MERGE (a) - [rel:IS_INDEXED_IN] -> (p);", 
                    {'pmid':self.pmid, 'name': publisher})
        
        
    @staticmethod
    def get_article(pmid):
        results = db.connection.run("MATCH (a:Article {pmid:{pmid}}) "
                                     "RETURN a as article;", pmid = pmid)
        
        return Article.serialize(results.single()['article'])
    
    @staticmethod
    def get_all_articles():
        results = db.connection.run("MATCH (a:Article) "
                                     "RETURN a as article;")
        
        return Article.serialize(result['article'] for result in results)
    
    @staticmethod
    def get_index_info(pmid, name):
        results = db.connection.run("MATCH (a:Article{pmid:{pmid}}) - [r:IS_INDEXED_IN] ->(p:Publisher{name:{name}}) "
                                     "RETURN a as article, collect(p.name) as publisher;", 
                                     {'pmid': pmid, 'name': name})
        
        
        return Article.serialize_indexer(results)
     
    @staticmethod
    def serialize(article):
        return {
                'pmid': article['pmid'],
                'title': article['title'],
                'pub_date': article['pub_date'],
                'authors': article['authors'],
                'issn': article['issn'],
                'doi': article['doi']
                }
    
    
    @staticmethod
    def serialize_indexer(results):
        return json.dumps({'article': results['article'],
                           'indexer': [Publisher.serialize(publisher) 
                           for publisher in results['publisher']]})
