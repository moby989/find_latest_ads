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
from datetime import datetime as dt
from datetime import timedelta as td

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from call_variables import *


#TWILIO CONNECTION
client = Client(username = TWILIO_ACCOUNT_SID,password = TWILIO_AUTH_TOKEN)

#CONNECTION TO MONGODB

MC = MongoClient(access_line_MDB)
db = MC['cian']



def getPage(link):
    """ """
    r = requests.get(link, headers = headers, cookies = cookies)
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

def sendWA(message_text,number_to = to_whatsapp_number, media_url = None):
    """  """
    client.messages.create(body=message_text,
                       media_url=media_url,
                       from_=from_whatsapp_number,
                       to=number_to)
    time.sleep(2)
    
#######################    
##CIAN  
  
properties_cian = {}

for n in url_cian.keys():
    
    all_properties = []
    
    properties = getProp(makeListLinks(url_cian[n]))

    for p in properties:
        property = {}
        property['description'] = p.find('span',{'data-mark':re.compile('OfferTitle')}).get_text()
        property['price'] = p.find('span',{'data-mark':re.compile('MainPrice')}).get_text()
        property['location'] = p.find('div',re.compile('labels')).get_text()
        property['link'] = p.find('a',re.compile('link'))['href']
        property['pict'] = p.find('picture',re.compile('picture')).img['src']
        property['_id'] = int(property['link'].split('/')[-2])
        property['post_date'] = p.find('div',re.compile('absolute')).get_text()

        check_date = property['post_date']
        check_price = property['price']
        if check_date.split(',')[0] =='сегодня' and int(check_price.split('/')[0].rstrip('₽').replace(' ','')) < 80000 :
            all_properties.append(property)    
        else:
            continue

    properties_cian[n] = all_properties
    

#upload and send CIAN

message_text = ['Объекты с ЦИАН',(dt.now()+td(hours = 3)).strftime("%c")]
for m in message_text:
    sendWA(m,to_whatsapp_number)

for n in url_cian.keys():
    sendWA('Направление: '+n,to_whatsapp_number) 
    count = 0
    for prop in properties_cian[n]:    
        try:
            result = db.rental_suburban.insert_one(prop)
            count+=1
            message_text = prop['description']+'\n'+prop['price']+'\n'+prop['location']+'\n'+prop['link']+'\n'+prop['post_date']
            media_url = prop['pict']
            try:                     
                sendWA(message_text,to_whatsapp_number,media_url) 
            except TwilioRestException:
                sendWA(message_text,to_whatsapp_number)
        except DuplicateKeyError:
            continue        
    if count == 0:
        m = 'Нет новых объектов по направлению '+n
    else:
        m = 'ЦИАН. Итого по направлению '+n+str(count)+' объект(ов).'    
    sendWA(m,to_whatsapp_number) 

    
####AVITO

all_properties_avito = []

for p in getPage(url_avito).find_all('div',re.compile('snippet snippet')):
    property = {}
    try:
        property['description'] = p.find('div',re.compile('snippet-title-row')).get_text().strip('\n ')
        property['price'] = p.find('div',re.compile('snippet-price-row')).get_text().strip('\n ').replace('\n в месяц','').replace(' ','')
        property['location'] = p.find('div',re.compile('item-address')).get_text().strip('\n ').replace('\n','')
        property['link'] = 'https://www.avito.ru'+p.a['href']
        property['pict'] = p.img['srcset'].split(',')[0].strip(' ').rstrip(' 1x')
        property['_id'] = int(p['id'].lstrip('i'))
        property['post_date'] = p.find('div',re.compile('snippet-date-info'))['data-tooltip'].strip('\n ')
    except TypeError:
        pass
    
    all_properties_avito.append(property)

#upload and send AVITO

message_text = ['Объекты с АВИТО',(dt.now()+td(hours = 3)).strftime("%c")]
for m in message_text:
    sendWA(m,to_whatsapp_number)

count = 0
for prop in all_properties_avito:
    try:
        result = db.rental_suburban_avito.insert_one(prop)
        count +=1
        message_text = prop['description']+'\n'+prop['price']+'\n'+prop['location']+'\n'+prop['link']+'\n'+prop['post_date']
        media_url = prop['pict']
        try:        
            sendWA(message_text,to_whatsapp_number,media_url) 
        except TwilioRestException:
            sendWA(message_text,to_whatsapp_number)
    except DuplicateKeyError:
        pass    

if count == 0:
    m = 'Нет новых объектов.'+'\n'+'Поиск закончен.'
else:
    m = 'Итого с АВИТО '+str(count)+' объект(ов).'+'\n'+'Поиск закончен.'
    

sendWA(m,to_whatsapp_number)    


    
print('all done')
