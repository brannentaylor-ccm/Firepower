#!/usr/bin/python3
"""FP Tools"""

import common_tools
import logging
import os
import requests
import urllib3
import json

from decouple import config
from requests.auth import HTTPBasicAuth


def get_creds():
    """Read the .env file and return credentials
    Returns:
    str: username
    str: password
    """
    # Check file existence
    if common_tools.checkFileExists(".env"):
        logging.info(f'Checked .env file exists: True')
        # logging.info(f"Returning: {config('x_cisco_meraki_api_key')[-4:]}")
        username = config('fmc_user')
        password = config('fmc_password')
        logging.info(f'Returning: {username=}, password: xxxx{password[4:-4]}xxxx')
        return username, password
    
    else:
        msg = "Error. Your '.env' was file not found."
        print(msg)
        logging.error(f'{msg}')
        os._exit()

def get_auth(username=None, password=None) -> str:
    '''Creates https basic auth string
        
    Parameters:
    username:None - enables a change to the username from the global variable.
    password:None - enables a change to the username from the global variable.
    
    Returns:
    HTTPbasicAuth:str - hashed httpbasicauth string.
    '''
    if username and password:
        b64_encode =  HTTPBasicAuth(username, password)
    else:
        b64_encode = HTTPBasicAuth(USERNAME, PASSWORD) #global variables.

    return b64_encode
    
def get_method(method='GET'):
    """Changes the HTTPS method."""
    return method

def get_url(endpoint:str, url='firepower.ccm.com') -> str:
    """Changes the default URL
    
    Paramaters:
    endpoint:str - endpoint like 'auth/generatetoken'
    """
    schema = 'https://'
    api_path = get_api_path()
    full_url = schema + url + api_path + endpoint
    logging.info(f'{full_url=}')

    return full_url

def get_headers(auth, content_type='application/json'):
    """Builds https headers"""
    headers = {'Content-Type':content_type,
               'Authorization':auth}
    return headers

def get_api_path(api_path='api/fmc_platform/v1') ->str:
    """Enables changing the API path"""
    return api_path

def get_payload(payload='') -> str:
    """Returns payload for https requests"""
    return payload


def get_token():
    """Using the credentials, get the token"""
    # username, password = get_creds()
    # suppress the warning about the verifying the certificate
    urllib3.disable_warnings()

    # auth = HTTPBasicAuth(username, password)
    # method = 'https://'
    # url = 'firepower.ccm.com/'
    # api_path = 'api/fmc_platform/v1/'
    # endpoint = 'auth/generatetoken'
    method = get_method('POST')
    try:
        # token = requests.post(f"{method}{url}{api_path}{endpoint}", auth=auth, verify=False)
        auth = get_auth()
        token = requests.request(method, get_url('/auth/generatetoken'), headers=get_headers(auth), data=get_payload())
        logging.info(f'{token=}')
        return token
    
    except Exception as e:
        logging.error(f'Error retrieving token.')
        print(e)

def main():
    """Main is a runner function, used to call individual functions in order."""
    global USERNAME
    global PASSWORD
    USERNAME, PASSWORD = get_creds()
    
    response = get_token()
    print(response)


############### START HERE #####################
# if__name__ - will look into a hidden variable for the file, called 'dunder name', or 'double underscore name'.
# if this script is being run directly, as a script, and not just a container of functions, the
# if__name__ will run, to inspect the name of the script, which will be '__main__', and will evaluate to True.
# if __name__ is True, then go set some settings, and then go run the 'main()' function.
################################################
if __name__ == "__main__":
    common_tools.start_logging('firepower_auto.log')
    main()