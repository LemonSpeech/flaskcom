# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 16:50:04 2018

@author: twiefel
"""

def test_server_wrapper():
    from server import ServerWrapper
    from test_class import TestClass
    
    #create the test object 
    test_object = TestClass(5)

    #wrap the test object in the server wrapper.
    #e voila, the test object can be used by the client
    test_object = ServerWrapper(test_object,54010)
    
def test_complex_server_wrapper():
    from server import ServerWrapper
    from complex_test_class import ComplexTestClass
    
    #create the test object 
    test_object = ComplexTestClass()

    #wrap the test object in the server wrapper.
    #e voila, the test object can be used by the client
    test_object = ServerWrapper(test_object,54010,complex_datatypes = True)

def main():
    test_complex_server_wrapper()
    
if __name__ == "__main__":
    main()