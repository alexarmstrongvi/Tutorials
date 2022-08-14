#!/usr/bin/env python3
print(f"\n===== Running {__file__} =====\n")
import pandas as pd
import os

def print_dir(obj):
    print("Object:", obj)
    print("Object Type:", type(obj))
    print("Attributes:")
    print('\t',"\n\t".join([x for x in dir(obj) if not x.startswith('_')]))

################################################################################
# Download files via URL
#
# Resources:
# - 
################################################################################
import urllib
# urllib.parse.quote
# urllib.request.urlopen

################################################################################
# Download files via HTTP requests
#
# Resources:
# - 
################################################################################
# Start with urllib.requests.Request

# Requests package
import requests
# response = requests.get(url, params, headers)
# text = response.text

# Sessions
# Why use sessions?
# session = requests.Session()
# resposne = session.get(url)

# from requests_futures.sessions import FuturesSession
# session = FuturesSession(max_workers=10)
# response1 = session.get(url)
# response2 = session.get(url)

################################################################################
# Authenticated APIs
################################################################################
# from requests_oauthlib import OAuth1

################################################################################
# from ediblepickle import checkpoint
