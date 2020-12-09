#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 16:17:57 2020

@author: moby
"""


import os

#TWILIO CREDENTIALS

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')

#Numbers where send messages to

from_whatsapp_number=os.getenv('from_whatsapp_number')
to_whatsapp_number=os.getenv('to_whatsapp_number')

#urls to parse 

url_cian_z = os.getenv(url_cian_z)
url_cian_yz = os.getenv(url_cian_yz)
url_cian = {'Западное':url_cian_z,'Юго-Западное':url_cian_yz}

#MongoDb credentials
login_and_pass_MDB = os.getenv('login_and_pass_MDB')
access_line = 'mongodb+srv://'+login_and_pass_MDB+'@test-cluster-khino.gcp.mongodb.net/test-cluster?retryWrites=true&w=majority'

#other data
headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
