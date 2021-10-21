# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 10:42:18 2018

@author: twiefel
"""

class TestClass:
    def __init__(self,saved_value):
        self.saved_value = saved_value
        
    def add_to_saved_value(self,input_value):
        print "processing_input",input_value
        self.saved_value+=input_value
        return self.saved_value
    
    def substract_from_saved_value(self,input_value):
        print "processing_input",input_value
        self.saved_value-=input_value
        return self.saved_value
    
    def get_saved_value(self):
        print "get_saved_value",self.saved_value
        return self.saved_value
    def get_nothing(self):
        pass