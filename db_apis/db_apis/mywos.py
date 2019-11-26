# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#!/usr/bin/env python3

#!/usr/bin/env python

# Thanks to Dan Jacob for a part of the code !

import requests

base_url = 'https://api.clarivate.com/api/woslite/'
key = 'd98b029549e960d2302ae995768903ba6930df1b'

headers = {  # headers dict to send in request
  "X-ApiKey": key,
 }

params = {  # params to be encoded in the url
  "databaseId ": "WOS",
  "usrQuery ":'AU=(Peiretti AND Palmegiano)',
  "count":100,
  "firstRecord ":10
}

#https://api.clarivate.com/api/woslite/?databaseId=WOS&lang=en&usrQuery=AU%3D(Peiretti%20AND%20Palmegiano)&count=100&firstRecord=10

if __name__=='__main__':
    resp = requests.get('https://api.clarivate.com/api/woslite/?databaseId=WOS&lang=en&usrQuery=AU%3D(Peiretti%20AND%20Palmegiano)&count=100&firstRecord=10', headers=headers)