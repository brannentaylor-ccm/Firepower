#!/usr/bin/python3


"""Get a list of objects from Firepower"""
import fp_tools_v2
import common_tools
import logging
import requests
import scrap
import sys

from common_tools import start_logging

def get_creds():
    """Get basic creds"""
    return fp_tools_v2.load_credentials()

def get_auth(username, password):
    """Get http basic auth"""
    return fp_tools_v2.get_basic_auth(username, password)

def get_token(username, password):
    """Get a token"""
    return fp_tools_v2.get_token(username, password)

def get_uuid(token):
    """Get the domain uuid from the token"""
    return fp_tools_v2.get_domainid(token)

def get_object_list(domain_uuid, auth):
    """Get an object list from the firewall
    https://firepower.ccm.com/api/api-explorer/api/fmc_config/v1/domain/{domainUUID}/object/networks
    """
    logging.info(f'Entered')

    # resource_path = "/api​/fmc_config​/v1​"
    resource_path = "/api/fmc_config/v1"
    endpoint = f"/domain/{domain_uuid}/object/networks"  
    

    # we have the full api_path - enter it into the arguments.
    url = fp_tools_v2.get_url(resource_path=resource_path, endpoint=endpoint)
    logging.info(f'{url=}')

    # auth = HTTPBasicAuth(USERNAME, PASSWORD)
    # logging.info(f'Got auth')

    headers = fp_tools_v2.get_headers()
    logging.info(f'{headers=}')

    payload = fp_tools_v2.get_payload()
    logging.info(f'{payload=}')

    method = "GET"
    logging.info(f'{method=}')

    logging.debug(f'Calling make_api_call')
    logging.debug(f'{url=}, {auth=}, {headers=}, {payload=}, {method=}')
    objects = fp_tools_v2.make_api_call(url, auth, headers, payload, method=method)

    return objects
    
    

    return None


def main():
    """Main is a runner function, used to call individual functions in order."""
    # retrieve the username and password for the FMC
    username, password = get_creds()
    # get a basic HTTP auth object
    basic_auth = get_auth(username, password)
    # get an API access token object
    _, token = get_token(username, password)

    scrap.read_token(token)




    sys.exit()





    domain_uuid = get_uuid(token)
    objects = get_object_list(domain_uuid, basic_auth)
    print(objects)

    




############### START HERE #####################
# if__name__ - will look into a hidden variable for the file, called 'dunder name', or 'double underscore name'.
# if this script is being run directly, as a script, and not just a container of functions, the
# if__name__ will run, to inspect the name of the script, which will be '__main__', and will evaluate to True.
# if __name__ is True, then go set some settings, and then go run the 'main()' function.
################################################
if __name__ == "__main__":
    start_logging("firepower.log")
    main()