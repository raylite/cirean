
from cirean.main import bp
from cirean import db

import os
from flask import flash, request, redirect, render_template, url_for, current_app
#from werkzeug.utils import secure_filename
from cirean.models import Publisher, Article

import pandas as pd
#import json


@bp.route('/')
def index():
    name = 'Wos'
    
    publisher = Publisher(name=name)
    publisher.create_publisher()
    
    result = publisher.find()
    
    article = Article(pmid=106297123, title='My trial of graph', pub_date='20/6/1999', authors='Akanbi and Adejumo', 
                      doi='doi.10.fx.1023', issn=10923764378)
    article.create_article()
    
    ar = article.find()
    
    article.create_article_publisher_rel(name)

    
    return render_template('upload.html', result = id(result), node = Publisher.get_publisher(name), 
                           ps = Publisher.get_all_publishers(), ar = id(ar), an = Article.get_article(106297))
    
    
    ##working now. Move to form creation and input processing for refworks
