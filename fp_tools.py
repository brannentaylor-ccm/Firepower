#!/usr/bin/python3


"""FP Tools"""

from decouple import config
import os
import common_tools
import logging

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

def main():
    """Main is a runner function, used to call individual functions in order."""
    pass


############### START HERE #####################
# if__name__ - will look into a hidden variable for the file, called 'dunder name', or 'double underscore name'.
# if this script is being run directly, as a script, and not just a container of functions, the
# if__name__ will run, to inspect the name of the script, which will be '__main__', and will evaluate to True.
# if __name__ is True, then go set some settings, and then go run the 'main()' function.
################################################
if __name__ == "__main__":
    common_tools.start_logging('firepower_auto.log')
    main()