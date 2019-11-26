# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 15:19:58 2019

@author: ja18581
"""

#google scholar scraper
#inspired from https://github.com/OrganicIrradiation/scholarly/blob/master/scholarly/scholarly.py

from __future__ import absolute_import, division, print_function, unicode_literals

from bs4 import BeautifulSoup

import hashlib
import pprint
import random
import re
import requests
import time
import pandas as pd


_SESSION = requests.Session()
_GOOGLEID = hashlib.md5(str(random.random()).encode('utf-8')).hexdigest()[:16]
_COOKIES = {'GSP': 'ID={0}:CF=4'.format(_GOOGLEID)}
_HEADERS = {
    'accept-language': 'en-US,en',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/41.0.2272.76 Chrome/41.0.2272.76 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml'
    }
_HOST = 'https://scholar.google.com'
_PUBSEARCH = '/scholar?q={0}'

class gscholar_search():
    
    def __init__(self):
        self.articles = []
        self.search_list = []
        
    def __call__(self, slist):
        self.search_list = slist
        for search_string in self.search_list:
            print (search_string)
            g = self.search_pubs_query(search_string)
            self._flatten_result(g)
        return self.articles
        
    def search_pubs_query(self, query):
        """Search by scholar query and return a generator of Publication objects"""
        url = _PUBSEARCH.format(requests.utils.quote(query))
        soup = self._get_soup(_HOST+url)
        return self._search_scholar_soup(soup)

    def _get_page(self, pagerequest):
        """Return the data for a page on scholar.google.com"""
        # Note that we include a sleep to avoid overloading the scholar server
        time.sleep(5+random.uniform(0, 5))
        resp = _SESSION.get(pagerequest, headers=_HEADERS, cookies=_COOKIES)
        if resp.status_code == 200:
            return resp.text
        if resp.status_code == 503:
            # Inelegant way of dealing with the G captcha
            raise Exception('Error: {0} {1}'.format(resp.status_code, resp.reason))
            # TODO: Need to fix captcha handling
            # dest_url = requests.utils.quote(_SCHOLARHOST+pagerequest)
            # soup = BeautifulSoup(resp.text, 'html.parser')
            # captcha_url = soup.find('img').get('src')
            # resp = _handle_captcha(captcha_url)
            # return _get_page(re.findall(r'https:\/\/(?:.*?)(\/.*)', resp)[0])
        else:
            raise Exception('Error: {0} {1}'.format(resp.status_code, resp.reason))



    def _get_soup(self, pagerequest):
        """Return the BeautifulSoup for a page on scholar.google.com"""
        html = self._get_page(pagerequest)
        html = html.replace(u'\xa0', u' ')
        return BeautifulSoup(html, 'html.parser')
    
    def _search_scholar_soup(self, soup):
        """Generator that returns Publication objects from the search page"""
        while True:
            for row in soup.find_all('div', 'gs_or'):
                try:
                    yield Publication(row)
                except:
                    break
            if soup.find(class_='gs_ico gs_ico_nav_next'):
                url = soup.find(class_='gs_ico gs_ico_nav_next').parent['href']
                soup = self._get_soup(_HOST+url)
            else:
                break
    def _flatten_result(self, g):
        for record in iter(g):
            try:
                print (record)
                self.articles.append(record.bib)
            except:
                break

class Publication(object):
    """Returns an object for a single publication"""
    def __init__(self, __data, pubtype=None):
        self.bib = dict()
        
        databox = __data.find('div', class_='gs_ri')
        title = databox.find('h3', class_='gs_rt')
        if title.find('span', class_='gs_ctu'): # A citation
            title.span.extract()
        elif title.find('span', class_='gs_ctc'): # A book or PDF
            title.span.extract()
        self.bib['title'] = title.text.strip()
        authorinfo = databox.find('div', class_='gs_a')
        self.bib['author'] = ' and '.join([i.strip() for i in authorinfo.text.split(' - ')[0].split(',')])
        self.bib['year'] = int(re.search('\s(\d{4})\s', authorinfo.text).groups()[0])
        if databox.find('div', class_='gs_rs'):
            self.bib['abstract'] = databox.find('div', class_='gs_rs').text
            if self.bib['abstract'][0:8].lower() == 'abstract':
                self.bib['abstract'] = self.bib['abstract'][9:].strip()
                    

       
    def __str__(self):
        return pprint.pformat(self.__dict__)
    
    


if __name__ == '__main__':
    gss = gscholar_search()
    search= ['Determination of non-liposomal and liposomal doxorubicin in plasma by LC-MS/MS coupled with an effective solid phase extraction: In comparison with ultrafiltration technique and application to a pharmacokinetic study.',
             'babatunde olorisade']
    
    df = pd.DataFrame(gss(search))
    