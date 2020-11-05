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
import browsercookie
from datetime import datetime as dt

from pymongo import MongoClient
#from pymongo.errors import BulkWriteError
from pymongo.errors import DuplicateKeyError


TWILIO_ACCOUNT_SID='AC1c1e1d41829ede543024e07b8a8218d0'
TWILIO_AUTH_TOKEN='5a3f6c412083fc2313b20a985e1703fe'


url_cian = 'https://www.cian.ru/cat.php?currency=2&deal_type=rent&engine_version=2&highway%5B0%5D=49&highway%5B10%5D=129&highway%5B11%5D=10&highway%5B12%5D=29&highway%5B13%5D=5&highway%5B14%5D=40&highway%5B15%5D=19&highway%5B16%5D=2&highway%5B17%5D=12&highway%5B18%5D=42&highway%5B19%5D=41&highway%5B1%5D=9&highway%5B2%5D=16&highway%5B3%5D=17&highway%5B4%5D=24&highway%5B5%5D=27&highway%5B6%5D=28&highway%5B7%5D=44&highway%5B8%5D=30&highway%5B9%5D=4&maxmcad=50&maxprice=80000&minarea=80&object_type%5B0%5D=1&object_type%5B1%5D=2&object_type%5B2%5D=4&offer_type=suburban&sort=creation_date_desc&totime=-2&type=4'
url_avito = 'https://www.avito.ru/moskva_i_mo/doma_dachi_kottedzhi/sdam/na_dlitelnyy_srok-ASgBAgICAkSUA9IQoAjIVQ?cd=1&f=ASgBAQECAkSUA9IQoAjIVQFA2gg01FnSWdZZAkWSCRl7ImZyb20iOjE0NTcxLCJ0byI6MTQ1NzV9whMYeyJmcm9tIjpudWxsLCJ0byI6MTQ2Nzd9&pmax=80000&pmin=40000&proprofile=1&road=2-4-5-9-10-11-12-15-16-18-23-25-26-28-29&s=104'

# this is the Twilio sandbox testing number
from_whatsapp_number='whatsapp:+14155238886'
# replace this number with your own WhatsApp Messaging number
to_whatsapp_number='whatsapp:+6282144356595'
#to_whatsapp_number='whatsapp:+79163549495'
client = Client(username = TWILIO_ACCOUNT_SID,password = TWILIO_AUTH_TOKEN)


MC = MongoClient('mongodb+srv://moby:ATES7F6Ok2v3pyrB@test-cluster-khino.gcp.mongodb.net/test-cluster?retryWrites=true&w=majority')
db = MC['cian']

cookies = {'__cfduid': 'dddb769ec4efb40abfb88ec36e253d1f91604432836',
 '__gads': 'ID=5fb292aefa8ef6fc:T=1598524615:S=ALNI_MZGBi3q0Eq7Ghfty1M818jHDRHhXg',
 '_dc_gtm_UA-2546784-1': '1',
 '_fbp': 'fb.1.1598524636054.2084898715',
 '_ga': 'GA1.2.1558263237.1598524635',
 '_gid': 'GA1.2.1768226770.1604432842',
 '_ym_d': '1598524613',
 '_ym_isad': '2',
 '_ym_uid': '1598524613753067361',
 '_ym_visorc_188382': 'w',
 '_ym_visorc_34241905': 'b',
 '_ym_visorc_419506': 'w',
 'buyer_laas_location': '107620',
 'buyer_location_id': '107620',
 'buyer_selected_search_radius4': '0_general',
 'dfp_group': '7',
 'f': '5.cc913c231fb04ced4b5abdd419952845a68643d4d8df96e9a68643d4d8df96e9a68643d4d8df96e9a68643d4d8df96e94f9572e6986d0c624f9572e6986d0c624f9572e6986d0c62ba029cd346349f36c1e8912fd5a48d02c1e8912fd5a48d0246b8ae4e81acb9fa143114829cf33ca746b8ae4e81acb9fa46b8ae4e81acb9fae992ad2cc54b8aa858f6718e375efe92a0aa1f8b1204bb276443a580474a5fe5915ac1de0d034112ad09145d3e31a56946b8ae4e81acb9fae2415097439d4047d50b96489ab264edc772035eab81f5e1e992ad2cc54b8aa8d99271d186dc1cd03de19da9ed218fe23de19da9ed218fe23de19da9ed218fe2e992ad2cc54b8aa846b8ae4e81acb9fa51b1fde863bf5c12f8ee35c29834d631c9ba923b7b327da7270c0755c0f4af4dc63c0367ea4a0fd72985db2d99140e2d9149e7c08f48f76ae1b31d40e35adfda38f0f5e6e0d2832ea1387b7c21005b504938c41efda3055a0df103df0c26013a0df103df0c26013aafbc9dcfc006bed9ba579619ddae8a612bbd4711fd6b5aab3de19da9ed218fe23de19da9ed218fe2d6fdecb021a45a31ddc8f1ee18e9df21fc7852884e906f31',
 'luri': 'moskva_i_mo',
 'sessid': 'c9d80c60566374c4f396d78c20748557.1604571408',
 'so': '1604572460',
 'sx': 'H4sIAAAAAAACA03NwQ2DMAwAwF385uEQB1y2KRY1koPysMBqEbuXT6UucHfCWPb6rvOz70WaBJsRmYcITCccMMHjWEta05ZfZiwNlYWFHF28ESN0sMCUBqShjIx8dcCfNcUmKYqg36BgeDMM%2FZHZcq3ZlnlviHeIJKwaFKqmTv8k84DX9QUwKrZgpwAAAA%3D%3D',
 'u': '2k9b9swx.qlboe4.1e7ygbw3wds00',
 'v': '1604571408',
 'abp': '0',
 'isCriteoSetNew': 'True',
 'lastViewingTime': '1604516444545',
 'no-ssr': '1',
 'showedStoryIds': '46-44-45-43-41-42-39-32-31-30-25'}

headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}


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
print(cookies)
#######################    
##CIAN    
#all_properties = []
#
#for p in getProp(makeListLinks(url_cian)):
#    property = {}
#    property['description'] = p.find('span',{'data-mark':re.compile('OfferTitle')}).get_text()
#    property['price'] = p.find('span',{'data-mark':re.compile('MainPrice')}).get_text()
#    property['location'] = p.find('div',re.compile('labels')).get_text()
#    property['link'] = p.find('a',re.compile('link'))['href']
#    property['pict'] = p.find('picture',re.compile('picture')).img['src']
#    property['_id'] = int(property['link'].split('/')[-2])
#    property['post_date'] = p.find('div',re.compile('absolute')).get_text()
#    
#    all_properties.append(property)
#    
#
##upload and send CIAN
#
#message_text = ['Объекты с ЦИАН',dt.now().strftime("%c")]
#for m in message_text:
#    #sendWA(m,'whatsapp:+79163549495')
#    sendWA(m,'whatsapp:+6282144356595')
#count = 0
#for prop in all_properties:
#    try:
#        result = db.rental_suburban.insert_one(prop)
#    count +=1
#        message_text = prop['description']+'\n'+prop['price']+'\n'+prop['location']+'\n'+prop['link']+'\n'+prop['post_date']
#        media_url = prop['pict']
#        try:        
##            sendWA(message_text,'whatsapp:+79163549495',media_url)
#            sendWA(message_text,'whatsapp:+6282144356595',media_url) 
#        except TwilioRestException:
# #           sendWA(message_text,'whatsapp:+79163549495')
#            sendWA(message_text,'whatsapp:+6282144356595')
#    except DuplicateKeyError:        
#        pass
    
#if count == 0:
#    m = 'Нет новых объектов.'+'\n'+'Поиск закончен.'
#else:
#    m = 'Итого с ЦИАН '+str(count)+' объект(ов).'+'\n'+'Поиск закончен.'
#    
#sendWA(m,'whatsapp:+6282144356595')
##sendWA(m,'whatsapp:+79163549495')    

    
#AVITO

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

message_text = ['Объекты с АВИТО',dt.now().strftime("%c")]
for m in message_text:
    #sendWA(m,'whatsapp:+79163549495')
    sendWA(m,'whatsapp:+6282144356595')

count = 0
for prop in all_properties_avito:
    try:
        result = db.rental_suburban_avito.insert_one(prop)
        count +=1
        message_text = prop['description']+'\n'+prop['price']+'\n'+prop['location']+'\n'+prop['link']+'\n'+prop['post_date']
        media_url = prop['pict']
        try:        
  #          sendWA(message_text,'whatsapp:+79163549495',media_url)
            sendWA(message_text,'whatsapp:+6282144356595',media_url) 
        except TwilioRestException:
   #         sendWA(message_text,'whatsapp:+79163549495')
            sendWA(message_text,'whatsapp:+6282144356595')
    except DuplicateKeyError:
        pass    

if count == 0:
    m = 'Нет новых объектов.'+'\n'+'Поиск закончен.'
else:
    m = 'Итого с АВИТО '+str(count)+' объект(ов).'+'\n'+'Поиск закончен.'
    
sendWA(m,'whatsapp:+6282144356595')
#sendWA(m,'whatsapp:+79163549495')    


    
print('all done')
