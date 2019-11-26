#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 17:30:14 2019

@author: ja18581
"""

from py2neo import Graph, Node
#from py2neo.data import Node

def createNodeWithLabelPropertiesWithCast():
    print("Start - Creating Node with Label and Properties")
    # Authenticate the user using py2neo.authentication
    # Ensure that you change the password 'sumit' as per your database configuration.
    #py2neo.authenticate("localhost:7474", "neo4j", "neo4j")
    # Connect to Graph and get the instance of Graph
    graph = Graph("http://localhost:7474", auth = ("neo4j", "neo4j"))
    #Define a LIST of Labels
    labels = [ 'FirstLabel' ,'SecondLabel' ]
    #Define a DICTIONARY
    properties = {'name':'MyPythonNode2', 'neo4j_version':'2.2'}
    #CAST the node and invoke graph.create method.
    node = Node.cast(labels,properties)
    resultNode, = graph.create(node)
    print("Node - ", resultNode)
    print("End - Creating Node with Label and Properties")
    
def createNodedicts():
    print("Start - Creating Node with Label and Properties")
# Authenticate the user using py2neo.authentication
# Ensure that you change the password 'sumit' as per your
   
    # Connect to Graph and get the instance of Graph
    graph = Graph("http://localhost:7474", auth=("neo4j", "neo4j"))
    
    #Define a LIST of Labels
    labels = [ 'FirstLabel' ,'SecondLabel' ]
    #Define a DICTIONARY
    properties = {'name':'MyPythonNode2', 'neo4j_version':'2.2'}
    #CAST the node and invoke graph.create method.
    node = Node.cast(labels,properties)
    result, = graph.create(node)
    print("Node - ", result)
    print("End - Creating Node with Label and Properties")
    
    
    
if __name__ == '__main__':
    #authenticate("localhost:7474", "neo4j", "p@55w0rd")
    print("Start Creating Nodes")
    createNode()
    print("End Creating Nodes")
    print("Start Creating Nodes from dicts")
    createNodedicts()
    print("End Creating Nodes from dicts")
    