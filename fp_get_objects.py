#!/usr/bin/python3


"""Get a list of objects from Firepower"""
import fp_tools_v2
import common_tools
import requests

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

def main():
    """Main is a runner function, used to call individual functions in order."""
    # retrieve the username and password for the FMC
    username, password = get_creds()
    # get a basic HTTP auth object
    basic_auth = get_auth(username, password)
    # get an API access token object
    _, token = get_token(username, password)
    domain_uuid = get_uuid(token)
    print(domain_uuid)




############### START HERE #####################
# if__name__ - will look into a hidden variable for the file, called 'dunder name', or 'double underscore name'.
# if this script is being run directly, as a script, and not just a container of functions, the
# if__name__ will run, to inspect the name of the script, which will be '__main__', and will evaluate to True.
# if __name__ is True, then go set some settings, and then go run the 'main()' function.
################################################
if __name__ == "__main__":
    main()