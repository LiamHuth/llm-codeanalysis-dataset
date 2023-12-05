#
#



import re
import random
import string

from lib.core.data import kb
from lib.core.enums import PRIORITY

__priority__ = PRIORITY.NORMAL

def dependencies():
    pass

def tamper(payload, **kwargs):
    retVal = payload
    if payload:
        all_ascii_letters = string.ascii_letters
        random_chars = ''.join(random.choice(all_ascii_letters) for i in range(3))
        retVal = retVal.replace("<here>",random_chars)
    return retVal