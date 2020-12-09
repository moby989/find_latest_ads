#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 16:17:57 2020

@author: moby
"""


import os


# os.environ['TWILIO_ACCOUNT_SID'] = 'AC5d94ce15b072f66e65218f798c2cf27c'
# os.environ['TWILIO_AUTH_TOKEN'] = 'c4d2a12450be983fe9d33505f0c940ab'
# os.environ['from_whatsapp_number'] = 'whatsapp:+14155238886'
# os.environ['to_whatsapp_number'] = 'whatsapp:+6282144356595'
# os.environ['to_whatsapp_number'] = 'whatsapp:+6282144356595'
# os.environ['login_and_pass_MDB'] = 'moby:ATES7F6Ok2v3pyrB'


# url_cian_z = 'https://www.cian.ru/cat.php?currency=2&deal_type=rent&engine_version=2&highway%5B0%5D=9&highway%5B1%5D=24&highway%5B2%5D=27&highway%5B3%5D=28&highway%5B4%5D=44&highway%5B5%5D=19&maxmcad=25&maxprice=80000&minarea=80&object_type%5B0%5D=1&object_type%5B1%5D=2&object_type%5B2%5D=4&offer_type=suburban&sort=creation_date_desc&totime=-2&type=4'
# url_cian_yz = 'https://www.cian.ru/cat.php?currency=2&deal_type=rent&engine_version=2&highway%5B0%5D=12&highway%5B1%5D=10&maxmcad=40&maxprice=80000&minarea=80&object_type%5B0%5D=1&object_type%5B1%5D=2&object_type%5B2%5D=4&offer_type=suburban&sort=creation_date_desc&totime=-2&type=4'
# url_cian = {'Западное':url_cian_z,'Юго-Западное':url_cian_yz}

# #url_cian = 'https://www.cian.ru/cat.php?currency=2&deal_type=rent&engine_version=2&highway%5B0%5D=49&highway%5B10%5D=129&highway%5B11%5D=10&highway%5B12%5D=29&highway%5B13%5D=5&highway%5B14%5D=40&highway%5B15%5D=19&highway%5B16%5D=2&highway%5B17%5D=12&highway%5B18%5D=42&highway%5B19%5D=41&highway%5B1%5D=9&highway%5B2%5D=16&highway%5B3%5D=17&highway%5B4%5D=24&highway%5B5%5D=27&highway%5B6%5D=28&highway%5B7%5D=44&highway%5B8%5D=30&highway%5B9%5D=4&maxmcad=50&maxprice=80000&minarea=80&object_type%5B0%5D=1&object_type%5B1%5D=2&object_type%5B2%5D=4&offer_type=suburban&sort=creation_date_desc&totime=-2&type=4'
# url_avito = 'https://www.avito.ru/moskva_i_mo/doma_dachi_kottedzhi/sdam/na_dlitelnyy_srok-ASgBAgICAkSUA9IQoAjIVQ?cd=1&f=ASgBAQECAkSUA9IQoAjIVQFA2gg01FnSWdZZAkWSCRl7ImZyb20iOjE0NTcxLCJ0byI6MTQ1NzV9whMYeyJmcm9tIjpudWxsLCJ0byI6MTQ2Nzd9&pmax=80000&pmin=40000&proprofile=1&road=2-4-5-9-10-11-12-15-16-18-23-25-26-28-29&s=104'



#TWILIO CREDENTIALS

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')

#Numbers where send messages to

from_whatsapp_number=os.getenv('from_whatsapp_number')
to_whatsapp_number=os.getenv('to_whatsapp_number')

#urls to parse 

url_cian_z = os.getenv('url_cian_z')
url_cian_yz = os.getenv('url_cian_yz')
url_cian = {'Западное':url_cian_z,'Юго-Западное':url_cian_yz}
url_avito = os.getenv('url_avito')

#MongoDb credentials
login_and_pass_MDB = os.getenv('login_and_pass_MDB')

access_line_MDB = 'mongodb+srv://'+login_and_pass_MDB+'@test-cluster-khino.gcp.mongodb.net/test-cluster?retryWrites=true&w=majority'


#other data
headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
cookies = None