import collections
import re 

from dateutil import tz

from commons.trace_logger import trace_logger
import socket
import string
import random
from uuid import UUID

local_time_zone = tz.tzlocal()


@trace_logger
def find_urls(string):
    """
    extracts the list of repository from the given string. Returns an empty list if no url found.
    """
    url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string) 
    return url 


@trace_logger
def group_dict_by_key(dictionary, key):
    grouped = collections.defaultdict(list)
    for item in dictionary:
        grouped[item[key]].append(item)
    return grouped


@trace_logger
def extract_max_number(input_string): 
    # get a list of all numbers separated by  
    # lower case characters  
    # \d+ is a regular expression which means 
    # one or more digit 
    # output will be like ['100','564','365'] 
    numbers = re.findall('\d+', input_string) 
    
    # now we need to convert each number into integer 
    # int(string) converts string into integer 
    # we will map int() function onto all elements  
    # of numbers list 
    if len(numbers) > 0:
        numbers = map(int, numbers) 
        return max(numbers)
    # if no number found in string return false 
    return False

@trace_logger
def if_dns_record_is_broken(dns_record):
    try:
        status = True
        addr1 = socket.gethostbyname(dns_record)
        if len(addr1)>1:
            status = False
        ''' 
        process = os.popen("dig "+domain_name + " +short")
        output = process.read()
        process.close()
        if len(output)<1:
            print(domain_name)
        '''
    except Exception as e:
        print(e)
    return status

@trace_logger
def random_string_digits(string_length=6):
    """Generate a random string of letters and digits """
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(string_length))


# Define a function for 
# for validating an Email
@trace_logger 
def is_email_valid(email):
    status = False 
    # pass the regualar expression 
    # and the string in search() method 
    if(re.search('^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$',email)):  
        status = True
    return status
      
def uuid_convert(o):
        if isinstance(o, UUID):
            return o.hex