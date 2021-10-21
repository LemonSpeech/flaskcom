# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 15:38:10 2018

@author: twiefel
"""
#this is a test if something gets imported when wrapping the class
#this output should not appear
from __future__ import print_function
print("importing module of complex test class")

class ComplexTestClass(object):
    def __init__(self, unused_string = "unused_string"):
        pass
    def get_image(self, filename, unused_kwarg=True):
        image = [1]*100
        return image
    def test_exception(self):
        raise Exception("this is a manually raised exception")


class ComplexTestSubClass(ComplexTestClass):
    def __init__(self, *args, **kwargs):
        super(ComplexTestSubClass, self).__init__( *args, **kwargs)
    def get_string(self, string):
        return "received "+string
    


#this class shouldnt be loaded
class UnusedClass:
    def unused_method(self, unused_param):
        pass
