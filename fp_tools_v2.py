#!/usr/bin/python3
"""Firepower tools - create basic auth, get a token from the FMC.

Brannen Taylor - 20240624

NOTE:  To retrieve credentials securely, you must store them in an .env file.  In the format:
fmc_user = SVC.CiscoAuto
fmc_password = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX

These creds are stored in Keeper.  They are in AD, but configured as local authentication on the FMC.

"""

import logging
import requests
import urllib3

from common_tools import start_logging
from requests.auth import HTTPBasicAuth
from decouple import config

def get_url(endpoint:str, url='firepower.ccm.com') -> str:
    """Changes the default URL
    
    Paramaters:
    endpoint:str - endpoint like 'auth/generatetoken'
    """
    logging.info(f'Entered')
    schema = 'https://'
    logging.info(f'{schema=}')
    api_path = get_api_path()
    full_url = schema + url + api_path + endpoint
    logging.info(f'{full_url=}')

    return full_url

def get_api_path(api_path='/api/fmc_platform/v1') -> str:
    """Enables changing the API path"""
    logging.info(f'Entered')
    logging.info(f"{api_path=}")
    return api_path

def get_headers():
    """Return the headers for the API request."""
    logging.info(f'Entered')
    headers =  {
        'Content-Type': 'application/json'
    }
    logging.info(f'{headers=}')
    return headers

def get_payload():
    """Return the payload for the API request."""
    logging.info(f'Entered')
    payload = {}
    logging.info(f'{payload=}')
    return payload

def get_basic_auth():
    """Return HTTP Basic Auth using the global USERNAME and PASSWORD."""
    # input(f"{USERNAME=}, {PASSWORD=}")
    logging.info(f'Entered')
    logging.info(f'Returning basic auth')
    return HTTPBasicAuth(USERNAME, PASSWORD)

def make_api_call(url, auth, headers, payload, method="GET"):
    """Make the API call and return the response."""
    logging.info(f'Entered')
    verify=False
    logging.info(f'{url=}, {auth=}, {headers=}, {payload=}, {method=}, {verify=}')
    urllib3.disable_warnings()
    try:
        response = requests.request(method, url, auth=auth, headers=headers, data=payload, verify=verify)
        return response
    except Exception as e:
        logging.error(f'{e}')
        msg = "Error from 'make_api_call'"
        code = 503
        return_dict = {'Code':code, 'MSG':msg}
        logging.error(f'Returning {return_dict}')
        return return_dict
    
def load_credentials():
    """Load USERNAME and PASSWORD from the .env file."""
    logging.info(f'Entered')
    try:
        USERNAME = config('fmc_user')
        PASSWORD = config('fmc_password')
        logging.info(f'Got creds successfully {USERNAME=}, PASSWORD:XXX{PASSWORD[3:-3]}XXX')
        return USERNAME, PASSWORD
    except Exception as e:
        logging.error(f'{e}')
        msg = "Error from 'load_credentials'"
        code = 503
        return_dict = {'Code':code, 'MSG':msg}
        logging.error(f'Returning {return_dict}')
        print(f"Error: {e}")
        return return_dict
        

def get_token():
    """Make an API call to Firepower to get a token"""
    logging.info(f'Entered')
    api_path = '/auth/generatetoken'
    logging.info(f'{api_path=}')
    url = get_url(api_path)
    logging.info(f'{url=}')
    auth = HTTPBasicAuth(USERNAME, PASSWORD)
    logging.info(f'Got auth')
    headers = get_headers()
    logging.info(f'{headers=}')
    payload = get_payload()
    logging.info(f'{payload=}')
    method = "POST"
    logging.info(f'{method=}')
    logging.debug(f'Calling make_api_call')
    logging.debug(f'{url=}, {auth=}, {headers=}, {payload=}, {method=}')
    token = make_api_call(url, auth, headers, payload, method=method)

    return auth, token
        
def main():
    global USERNAME, PASSWORD
    USERNAME, PASSWORD = load_credentials()
    logging.info(f'Retrieving creds, USERNAME: XXX{USERNAME[3:-1]}XXX, PASSWORD: XXX{PASSWORD[3:-3]} ')
    if not USERNAME or not PASSWORD:
        logging.error(f'Error retrieving username and password from .env file.')
        print("Please ensure USERNAME and PASSWORD are set in the .env file.")
        return

    logging.debug(f'Calling get_token')
    auth, token = get_token()
    print(auth)
    print(token)

if __name__ == "__main__":
    start_logging('firepower.log')
    logging.info(f'Logging start')
    main()
