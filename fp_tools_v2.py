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

def get_url(endpoint=None, resource_path=None, url='firepower.ccm.com') -> str:
    """Changes the default URL
    
    Paramaters:
    endpoint:str - endpoint like 'auth/generatetoken'
    """
    logging.info(f'Entered')
    schema = 'https://'
    logging.info(f'{schema=}')
    if not resource_path:
        resource_path = get_resource_path()

    full_url = schema + url + resource_path + endpoint
    input(f"{full_url=}")
    logging.info(f'{full_url=}')

    return full_url

def get_resource_path(resource_path='/api/fmc_platform/v1') -> str:
    """Enables changing the API path"""
    input(resource_path)
    logging.info(f'Entered')
    logging.info(f"{resource_path=}")
    return resource_path

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

def get_basic_auth(USERNAME, PASSWORD):
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
        logging.error(f'Error: {e}')
        print(e)
        return return_dict
    
def load_credentials():
    """Load USERNAME and PASSWORD from the .env file."""
    logging.info(f'Entered')

    global USERNAME, PASSWORD
    # USERNAME, PASSWORD = load_credentials()
    # logging.info(f'Retrieving creds, USERNAME: XXX{USERNAME[3:-1]}XXX, PASSWORD: XXX{PASSWORD[3:-3]} ')

    # if not USERNAME or not PASSWORD:
    #     logging.error(f'Error retrieving username and password from .env file.')
    #     print("Please ensure USERNAME and PASSWORD are set in the .env file.")
    #     return ''
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
        logging.error(f'Error: {e}')
        print(f"Error: {e}")
        return return_dict
        

def get_token(USERNAME, PASSWORD):
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


def get_domainid(token):
    """
    https://www.cisco.com/c/en/us/td/docs/security/firepower/621/api/REST/Firepower_Management_Center_REST_API_Quick_Start_Guide_621/objects_in_the_rest_api.html
    UUID}
    Many URLs contain one or more UUIDs which must be specified. Most URIs include the domain UUID, 
    which can be found in the Authentication Token. When deleting or modifying an object, or requesting 
    information about a specific object, the URI will end with the object UUID.
    """
    logging.info(f'Entered')
    logging.info(f'{token.status_code=}')
    if token.status_code == 204:
        # print(f"Token response is 204")
        domain_uuid = token.headers.get('DOMAIN_UUID')
        logging.info(f'{domain_uuid=}')
        if not domain_uuid:
            msg = f"DOMAIN_UUID not found in the response headers."
            logging.error(f'{msg}')
            domain_uuid = None
    else:
        msg = f"Request failed with the status code: {token.status_code}"
        logging.error(f'{msg}')
        domain_uuid = None

    return domain_uuid

def main():
    # global USERNAME, PASSWORD
    # USERNAME, PASSWORD = load_credentials()
    # logging.info(f'Retrieving creds, USERNAME: XXX{USERNAME[3:-1]}XXX, PASSWORD: XXX{PASSWORD[3:-3]} ')

    # if not USERNAME or not PASSWORD:
    #     logging.error(f'Error retrieving username and password from .env file.')
    #     print("Please ensure USERNAME and PASSWORD are set in the .env file.")
    #     return ''

    logging.debug(f'Calling get_token')
    auth, token = get_token()
    domain_uuid = get_domainid(token)
    print(f"Done with Main - domain_uuid: {domain_uuid}")







if __name__ == "__main__":
    start_logging('firepower.log')
    logging.info(f'Logging start')
    main()
