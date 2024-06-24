#!/usr/bin/python3
"""Python script to hold commonly used functions("tools").

Brannen Taylor
2/17/24
"""
import concurrent.futures
import json
import logging
import os
# import requests
import time
import uuid
import random
import socket

from datetime import datetime
from pprint import pprint

def checkFileExists(fileName:str) -> bool:
    """Check for the existence of a file."""
    return os.path.exists(fileName)

def start_logging(filename='log.log', level_:str="DEBUG"):
    """Configures logging
    
    Params:
    filename:str - an optional filename.  Default: log.log
    
    Returns:
    None

    Actions: configures logging.
    """
    logLevel = f"logging.{level_}"
    logging.basicConfig(
        filename=filename,
        level=logging.INFO,
        filemode = "a", 
        format= '%(asctime)s Line:%(lineno)5d %(levelname)8s - %(filename)8s\%(funcName)10s - %(message)s',
        datefmt='%H:%M:%S'
    )


def get_date(format:int=2):
    """Returns date and or time in different formats as a string
    
    Params:
    format:int 
        - 1 for %Y%m%d%H%M%S
        - 2 for M/D/Y
    
    Returns:
    date:str - depending on option, date and or time as a string.
    """
    date = datetime.now()
    if format:
        if format == 1: #YearMonthDayHourMinSec
            date = datetime.now().strftime("%Y%m%d%H%M%S")
        if format == 2: #Month/Day/Year
            date = datetime.now().strftime("%m/%d/%Y")

    return date

def sortIPs(ips:list):
    """Sorts a list of IPs and returns them.
    Param: ips:list - a list of unsorted Ipv4 addresses.
    Returns: sorted list:list - the list that was passed in, as a IPv4 sorted list."""
    
    # sort from https://stackoverflow.com/questions/6545023/how-to-sort-ip-addresses-stored-in-dictionary-in-python and chatGPT
    # The socket.inet_aton(ip) converts each IP address to its 32-bit packed binary format, which allows the sorted() function to sort the addresses correctly.
    return sorted(ips, key=lambda ip:socket.inet_aton(ip))

def get_passphrase():
    """Create a random passphrase"""
    animals = read_json('animals.json')
    # Get list of short animals
    animals = [animal for animal in animals['data'] if len(animal) < 5]
    months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    symbols = ['@', '#', '$', '%', '&']
    # Choose randomly
    choices = []
    choices.append(random.choice(animals).title())
    choices.append(random.choice(months).title())
    choices.append(random.choice(symbols))
    choices.append(str(random.choice([2,3,4,5,6,7,8,9])))
    # Shuffle the list of choices.
    random.shuffle(choices)
    # Join the choices into a passphrase.
    passphrase = ''.join(choices)
    # Return the passphrase
    return passphrase


def start_time():
    """Call start_time first, then use get_time to get ms back"""
    # return datetime.now()
    timestamp = time.time()
    return timestamp


def get_time(start):
    """
    Calculates time from the start until the time called.  Used to time operations.

    Params:
    start:timestamp - a timestamp object - get it from start_time().

    Returns:
    formatted_time:str - a formatted time object as a string.
    """
    timestamp = start_time() - start
    # Create a datetime object from the timestamp
    datetime_object = datetime.fromtimestamp(timestamp)

    # Format the datetime object to include only the minutes and seconds
    formatted_time = datetime_object.strftime("%M:%S.%f")[:-2]

    return formatted_time


def make_dir(directory):
    """Looks to see if a directory exists below the CWD.
    If not, it will create one, with the paramater name, 
    "directory".
    
    Params:
    directory:str - a string for the directory to create.

    Returns:
    None

    Actions: Creates a directory.
    """
    if isinstance(directory, str):
        path = ".\\" + directory
        if not os.path.exists(path):
            os.mkdir(path)
            msg = f"Directory: {path} created."
            status = {"code":200, "msg":msg}
        else:
            msg = "Directory already exists."
            status = {"code":200, "msg":msg}
    else:
        msg = f"Invalid directory: {directory}"
        status = {"code":400, "msg":msg}
    
    return status
    

def get_uid():
    """Generate a unique string based on time and unique uuid to attach to filenames.
    
    Params: none
    Returns: unique:str - a unique string of epoch time in seonds and UUID.

    Brannen Taylor
    2/17/24
    """
    # get the epoch time in seconds and convert it to a string
    time_ = str(int(time.time()))
    # generate a random 7 character, upper case, unique ID
    uuid_ = (str(uuid.uuid4()).upper()[:8])
    # combine epoch time with unique id
    unique = time_ + "-" + uuid_
    return unique


def write_json(filename:str, data:any, uid:bool = False, save_dir=None):
    """Accept a filename and data and output it to filename.json file.
    
    Params:
    filename:str - string of the filename to save to.
    data:any - any data passed in, will be conferted to .json in the .json file.
    uid:bool - add a uid to the filename - True?  False by default.  Adding a UUID will prevent overwrite.
    
    Returns:
    status:dict - a dictionary with a status code and message

    Actions: writes a .json file.
    
    Brannen Taylor
    2/17/24
    """
    FUNCTEST = False
    status = {"code":0, "msg":None}
    # validity checks
    valid_types = [str, list, dict, bool, int, float, tuple]
    if filename and data:
        # if function testing more explicit log data, else just the first 25 chars.
        if FUNCTEST:
            logging.info(f'{filename=}, {data}')
        else:
            logging.info(f'{filename=}, {str(data)[:25]}')
        if isinstance(filename, str):
            if type(data) in valid_types:
                status = {"code":200, "msg":"Data is acceptable."}
                logging.info(f'{status}')
            else:
                logging.error("Error. filename or  data is incorrect")
                return {"code":500, "msg":"Error. filename or  data is incorrect."}
        else:
            logging.error("Error.  Invalid filename.")
            return {"code":500, "msg":"Error. Invalid filename."}
            
    else:
        logging.error("Error. filename or  data is incorrect")
        return {"code":500, "msg":"Error. filename or  data is incorrect."}
    
    # proceed with file save
    if status["code"] == 200:
        # Add a unique ID?
        if uid:
            filename += ("-" + get_uid())
        filename += ".json"
        # Save to sub folder/directory?
        if save_dir:
            if not os.path.isdir(f'.\\{save_dir}'):
                logging.info(f'{save_dir} does not exist')
                try:
                    os.mkdir(f".\\{save_dir}")
                    logging.info(f'Created directory {save_dir}')
                except Exception as e:
                    print(e)
                    logging.error(f'Error creating directory. {e}')
            # directory exists, change dir
            os.chdir(f".\\{save_dir}")
        # Write the file        
        try:
            with open(filename, "w") as f:
                f.write(json.dumps(data, indent=2))
                logging.info(f'Wrote file: {filename}')
                status = {"code":200, "msg":f"{filename} written successfully."}
                if save_dir:  
                    # If saved into a sub directory, will have moved into it abvoe.  Move one step out and up.
                    os.chdir("..\\")
                    logging.info(f'{os.getcwd()=}')
        except Exception as e:
            status = {"code":500, "msg":f"Error: {e}"}
            logging.error(status)
    
    return status


def read_json(filename:str):
    """Reads a .json file and returns data.
    
    Params:
    filename:str - filename to open and read data.  Must be a .json file.

    Returns:
    status:dict - a dictionary with status codes and data.
    
    Brannen Taylor
    2/17/24"""
    if isinstance(filename, str):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
                logging.info(f'Opened {filename} successfully')
                status = {"code":200, "data": data}
        except FileNotFoundError:
            status = {"code":500, "msg":f"{filename} wasn't found."}
            logging.warning(f'{status}')
        except ValueError:
            status = {"code":500, "msg":f"{filename} is an invalid .json file."}
            logging.warning(f'{status}')
        except Exception as e:
            status = {"code":500, "msg":e}
            logging.warning(f'{status}')
    else:
        status = {"code":500, "msg":f"{filename} is not a string. Please check the filename."}

    return status


def get_intersection (list1:list, list2:list) -> list:
    """Compares 2 lists and returns a list of common elements, a 'common subset'.
    
    Params:
    list1:list - the first list.
    list2:list - the second list.
    
    Returns:
    list:list - returns a list of common elements.
    """
    for list_ in [list1, list2]:
        # check arguments are lists
        if not isinstance(list_, list):
            try:
                list_ = list(list_)
                print(f"Converted list: list_")
            except TypeError as e:
                msg = f"Invalid list"
                logging.error(f"{msg}")
                result = {'code':401, 'msg':None}
                break
            except Exception as e:
                print(e)
                msg = e
                logging.error(f"Error: {e}")
                result = {'code':402, 'msg':None}
                break
        else:
            # 2 Arguments are lists, compare elements, return a list of elements in common.
            logging.info("valid list arguments")
            # list comprehension for each element in list 1, add to list, if list1 element is in list2.
            matches = [x for x in list1 if x in list2]
            logging.info(f'Matches: {matches}')
            result = {'code':200, 'msg':matches}

    return result


def is_jsonable(data):
    """Tests to see if the data is serilizeable into json"""
    try:
        json.dumps(data)
        return True
    except (TypeError, OverflowError):
        return False


def run_multithread(a_function, an_iterable):
    """Runs threading each iterable in an_iterable against a_function.
    from Corey Schafer - Youtube
    https://youtu.be/IEEhzQoKtQU?t=1573
    
    Params:
    a_function:function - the function you want to call with multiple threads.
    an_iterable:iterable - the list, or iterable, you want to iterate over.
    
    Returns:
    """
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(a_function, an_iterable)


def main():
    # print(get_uid())

    # bogus = [
    #     "dude",
    #     "bodacious",
    #     "bogus",
    #     "most non-triumphant",
    # ]
    # # bogus = {"something":"something"}

    # print(write_json('delme', bogus))
    # filename = "delme.json"
    # pprint(read_json(filename))

    # start = start_time()
    # print(type(start))
    # time.sleep(.5)
    # endtime = get_time(start)
    # print(type(endtime))
    # timetaken = endtime
    # print(timetaken)
    print(get_passphrase())

if __name__ == "__main__":
    main()


