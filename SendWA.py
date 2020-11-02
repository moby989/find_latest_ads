#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 14:00:02 2020

@author: moby
"""

import requests
from bs4 import BeautifulSoup as bs
import re
import time
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

from pymongo import MongoClient
#from pymongo.errors import BulkWriteError
from pymongo.errors import DuplicateKeyError


TWILIO_ACCOUNT_SID='AC1c1e1d41829ede543024e07b8a8218d0'
TWILIO_AUTH_TOKEN='5a3f6c412083fc2313b20a985e1703fe'


url_cian = 'https://www.cian.ru/cat.php?currency=2&deal_type=rent&engine_version=2&maxmcad=70&maxprice=80000&minarea=80&object_type%5B0%5D=1&object_type%5B1%5D=2&object_type%5B2%5D=4&offer_type=suburban&region=-1&sort=creation_date_desc&totime=-2&type=4'


# this is the Twilio sandbox testing number
from_whatsapp_number='whatsapp:+14155238886'
# replace this number with your own WhatsApp Messaging number
to_whatsapp_number='whatsapp:+6282144356595'
#to_whatsapp_number='whatsapp:+79163549495'
client = Client(username = TWILIO_ACCOUNT_SID,password = TWILIO_AUTH_TOKEN)


MC = MongoClient('mongodb+srv://moby:ATES7F6Ok2v3pyrB@test-cluster-khino.gcp.mongodb.net/test-cluster?retryWrites=true&w=majority')
db = MC['cian']


def getPage(link):
    """ """
    r = requests.get(link)
    time.sleep(3)
    page = bs(r.content,features="html.parser")

    return page    


def makeListLinks(url_cian):
    """ """
    l_list = [url_cian]
    for link in getPage(l_list[0]).find_all('a',re.compile('list-item')):
        if not bool(re.search('www.cian.ru',link['href'])):
            link['href'] = 'https://www.cian.ru'+link['href']
        l_list.append(link['href'])
    
    return l_list

def getProp(listLinks):
    """ """
    all_properties = []
    for link in listLinks:
        soup = getPage(link)
        all_properties.extend(soup.find_all('article',re.compile('_93444fe79c')))

    return all_properties

def sendWA(message_text,media_url = None):
    """  """
    client.messages.create(body=message_text,
                       media_url=media_url,
                       from_=from_whatsapp_number,
                       to=to_whatsapp_number)
    time.sleep(2)
 
#######################    
    
all_properties = []

for p in getProp(makeListLinks(url_cian)):
    property = {}
    property['description'] = p.find('span',{'data-mark':re.compile('OfferTitle')}).get_text()
    property['price'] = p.find('span',{'data-mark':re.compile('MainPrice')}).get_text()
    property['location'] = p.find('div',re.compile('labels')).get_text()
    property['link'] = p.find('a',re.compile('link'))['href']
    property['pict'] = p.find('picture',re.compile('picture')).img['src']
    property['_id'] = int(property['link'].split('/')[-2])
    property['post_date'] = p.find('div',re.compile('absolute')).get_text()
    
    all_properties.append(property)
    

#upload and send
for prop in all_properties:
    try:
        result = db.rental_suburban.insert_one(prop)
        message_text = prop['description']+'\n'+prop['price']+'\n'+prop['location']+'\n'+prop['link']+'\n'+prop['post_date']
        media_url = prop['pict']
        try:        
            sendWA(message_text,media_url)         
        except TwilioRestException:
            sendWA(message_text)
    except DuplicateKeyError:
        pass

print('all done')
