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
#from call_variables import TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN,from_whatsapp_number,to_whatsapp_number,url_cian,url_avito
from call_variables import *


#TWILIO_ACCOUNT_SID='AC5d94ce15b072f66e65218f798c2cf27c'
#TWILIO_AUTH_TOKEN='c4d2a12450be983fe9d33505f0c940ab'

url_cian_z = 'https://www.cian.ru/cat.php?currency=2&deal_type=rent&engine_version=2&highway%5B0%5D=9&highway%5B1%5D=24&highway%5B2%5D=27&highway%5B3%5D=28&highway%5B4%5D=44&highway%5B5%5D=19&maxmcad=25&maxprice=80000&minarea=80&object_type%5B0%5D=1&object_type%5B1%5D=2&object_type%5B2%5D=4&offer_type=suburban&sort=creation_date_desc&totime=-2&type=4'
url_cian_yz = 'https://www.cian.ru/cat.php?currency=2&deal_type=rent&engine_version=2&highway%5B0%5D=12&highway%5B1%5D=10&maxmcad=40&maxprice=80000&minarea=80&object_type%5B0%5D=1&object_type%5B1%5D=2&object_type%5B2%5D=4&offer_type=suburban&sort=creation_date_desc&totime=-2&type=4'
url_cian = {'Западное':url_cian_z,'Юго-Западное':url_cian_yz}

#url_cian = 'https://www.cian.ru/cat.php?currency=2&deal_type=rent&engine_version=2&highway%5B0%5D=49&highway%5B10%5D=129&highway%5B11%5D=10&highway%5B12%5D=29&highway%5B13%5D=5&highway%5B14%5D=40&highway%5B15%5D=19&highway%5B16%5D=2&highway%5B17%5D=12&highway%5B18%5D=42&highway%5B19%5D=41&highway%5B1%5D=9&highway%5B2%5D=16&highway%5B3%5D=17&highway%5B4%5D=24&highway%5B5%5D=27&highway%5B6%5D=28&highway%5B7%5D=44&highway%5B8%5D=30&highway%5B9%5D=4&maxmcad=50&maxprice=80000&minarea=80&object_type%5B0%5D=1&object_type%5B1%5D=2&object_type%5B2%5D=4&offer_type=suburban&sort=creation_date_desc&totime=-2&type=4'
url_avito = 'https://www.avito.ru/moskva_i_mo/doma_dachi_kottedzhi/sdam/na_dlitelnyy_srok-ASgBAgICAkSUA9IQoAjIVQ?cd=1&f=ASgBAQECAkSUA9IQoAjIVQFA2gg01FnSWdZZAkWSCRl7ImZyb20iOjE0NTcxLCJ0byI6MTQ1NzV9whMYeyJmcm9tIjpudWxsLCJ0byI6MTQ2Nzd9&pmax=80000&pmin=40000&proprofile=1&road=2-4-5-9-10-11-12-15-16-18-23-25-26-28-29&s=104'


client = Client(username = TWILIO_ACCOUNT_SID,password = TWILIO_AUTH_TOKEN)
cookies = None



MC = MongoClient('mongodb+srv://moby:ATES7F6Ok2v3pyrB@test-cluster-khino.gcp.mongodb.net/test-cluster?retryWrites=true&w=majority')
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
    sendWA(m,'whatsapp:+79163549495')
    sendWA(m,'whatsapp:+6282144356595')

for n in url_cian.keys():
    sendWA('Направление: '+n,'whatsapp:+79163549495')
    sendWA('Направление: '+n,'whatsapp:+6282144356595') 
    count = 0
    for prop in properties_cian[n]:    
        try:
            result = db.rental_suburban.insert_one(prop)
            count+=1
            message_text = prop['description']+'\n'+prop['price']+'\n'+prop['location']+'\n'+prop['link']+'\n'+prop['post_date']
            media_url = prop['pict']
            try:        
                sendWA(message_text,'whatsapp:+79163549495',media_url)
                sendWA(message_text,'whatsapp:+6282144356595',media_url) 
            except TwilioRestException:
                sendWA(message_text,'whatsapp:+79163549495')
                sendWA(message_text,'whatsapp:+6282144356595')
        except DuplicateKeyError:
            continue        
    if count == 0:
        m = 'Нет новых объектов по направлению '+n
    else:
        m = 'ЦИАН. Итого по направлению '+n+str(count)+' объект(ов).'    
    sendWA(m,'whatsapp:+6282144356595')
    sendWA(m,'whatsapp:+79163549495') 

    
#AVITO

#all_properties_avito = []
#
#for p in getPage(url_avito).find_all('div',re.compile('snippet snippet')):
#    property = {}
#    try:
#        property['description'] = p.find('div',re.compile('snippet-title-row')).get_text().strip('\n ')
#        property['price'] = p.find('div',re.compile('snippet-price-row')).get_text().strip('\n ').replace('\n в месяц','').replace(' ','')
#        property['location'] = p.find('div',re.compile('item-address')).get_text().strip('\n ').replace('\n','')
#        property['link'] = 'https://www.avito.ru'+p.a['href']
#        property['pict'] = p.img['srcset'].split(',')[0].strip(' ').rstrip(' 1x')
#        property['_id'] = int(p['id'].lstrip('i'))
#        property['post_date'] = p.find('div',re.compile('snippet-date-info'))['data-tooltip'].strip('\n ')
#    except TypeError:
#        pass
#    
#    all_properties_avito.append(property)
#
##upload and send AVITO
#
#message_text = ['Объекты с АВИТО',(dt.now()+td(hours = 3)).strftime("%c")]
#for m in message_text:
#    #sendWA(m,'whatsapp:+79163549495')
#    sendWA(m,'whatsapp:+6282144356595')
#
#count = 0
#for prop in all_properties_avito:
#    try:
#        result = db.rental_suburban_avito.insert_one(prop)
#        count +=1
#        message_text = prop['description']+'\n'+prop['price']+'\n'+prop['location']+'\n'+prop['link']+'\n'+prop['post_date']
#        media_url = prop['pict']
#        try:        
#  #          sendWA(message_text,'whatsapp:+79163549495',media_url)
#            sendWA(message_text,'whatsapp:+6282144356595',media_url) 
#        except TwilioRestException:
#   #         sendWA(message_text,'whatsapp:+79163549495')
#            sendWA(message_text,'whatsapp:+6282144356595')
#    except DuplicateKeyError:
#        pass    
#
#if count == 0:
#    m = 'Нет новых объектов.'+'\n'+'Поиск закончен.'
#else:
#    m = 'Итого с АВИТО '+str(count)+' объект(ов).'+'\n'+'Поиск закончен.'
#    
#sendWA(m,'whatsapp:+6282144356595')
##sendWA(m,'whatsapp:+79163549495')    


    
print('all done')
