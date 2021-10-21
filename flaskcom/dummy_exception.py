# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 11:24:08 2018

@author: twiefel
"""
from __future__ import print_function

class DummyException(object):
    def __init__(self):
        import sys

        
        exc_type, exc_value, exc_traceback = sys.exc_info()
        import traceback
        tb = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        #print(tb)
        self.exception_info = tb
        #self.exception = exc_value
        #print("DummyException",len(self.exception_info), type(self.exception_info))
