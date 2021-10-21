# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 15:03:50 2020

@author: twiefel
"""
from __future__ import print_function
try:
    unichr(1)
except:
    unichr = chr
def print_error(text):
    unicode_number = 9608
    line = unichr(unicode_number)*(len(text)+8)
    print("\033[1;31;40m"+line+"\033[0m")
    print("\033[1;31;40m"+unichr(unicode_number)+unichr(unicode_number)+unichr(unicode_number),text, unichr(unicode_number)+unichr(unicode_number)+unichr(unicode_number)+"\033[0m")
    print("\033[1;31;40m"+line+"\033[0m")
