#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 16:17:57 2020

@author: moby
"""


import os

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')

TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')


print(TWILIO_ACCOUNT_SID)
print(TWILIO_AUTH_TOKEN)

