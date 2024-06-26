from requests.auth import HTTPBasicAuth
import requests

# auth_ = HTTPBasicAuth('username', 'password')


def read_token(token):
    """
    https://www.cisco.com/c/en/us/td/docs/security/firepower/621/api/REST/Firepower_Management_Center_REST_API_Quick_Start_Guide_621/objects_in_the_rest_api.html
    UUID}
    Many URLs contain one or more UUIDs which must be specified. Most URIs include the domain UUID, 
    which can be found in the Authentication Token. When deleting or modifying an object, or requesting 
    information about a specific object, the URI will end with the object UUID.
    """
    # logging.info(f'Entered')
    # logging.info(f'{token.status_code=}')
    # if token.status_code == 204:
    #     # print(f"Token response is 204")
    #     domain_uuid = token.headers.get('DOMAIN_UUID')
    #     logging.info(f'{domain_uuid=}')
    #     if not domain_uuid:
    #         msg = f"DOMAIN_UUID not found in the response headers."
    #         logging.error(f'{msg}')
    #         domain_uuid = None
    # else:
    #     msg = f"Request failed with the status code: {token.status_code}"
    #     logging.error(f'{msg}')
    #     domain_uuid = None

    # return domain_uuid
    if token.status_code == 204:
        """
        {'Date': 'Wed, 26 Jun 2024 15:03:17 GMT', 'Server': 'Apache', 
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains', 
        'Cache-Control': 'no-store', 'Accept-Ranges': 'bytes', 
        'Vary': 'Accept-Charset,Accept-Encoding,Accept-Language,Accept', 
        'X-auth-access-token': 'a22e9669-0ef4-46fd-bd5e-c871a9bfcbb4', 
        'X-auth-refresh-token': '26330413-e0a7-4c6c-9144-76d9eb45ab96', 
        'USER_UUID': 'ecbd2ca4-2fd7-11ef-89ec-89a9c5c90a21', 'DOMAIN_ID': '111', 
        'DOMAIN_UUID': 'e276abec-e0f2-11e3-8169-6d9ed49b625f', 
        'global': 'e276abec-e0f2-11e3-8169-6d9ed49b625f', 
        'DOMAINS': '[{"uuid":"e276abec-e0f2-11e3-8169-6d9ed49b625f",
        "name":"Global"}]', 'X-Frame-Options': 'SAMEORIGIN', 
        'X-UA-Compatible': 'IE=edge', 'X-Permitted-Cross-Domain-Policies': 
        'none', 'X-XSS-Protection': '1; mode=block', 
        'Referrer-Policy': 'same-origin', 'Content-Security-Policy': "base-uri 'self'", 
        'X-Content-Type-Options': 'nosniff', 'Keep-Alive': 'timeout=5, max=100', 
        'Connection': 'Keep-Alive'}
        
        """
        # print(token.headers['X-auth-access-token'])
        headers = {'X-auth-access-token':token.headers['X-auth-access-token'],
                   'Authorization':'replace me with https basic get_auth'}
        print(headers)

        #TODO : modify the get_headers and add in the tokens, and https basic auth.
""""""

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
    main()