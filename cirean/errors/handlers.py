#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  1 10:21:03 2019

@author: ja18581
"""

from flask import render_template
from cirean import db
from cirean.errors import bp


@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 400

@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500