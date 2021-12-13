#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 16:33:34 2021

@author: dedalus
"""

#this is an example how to create a remote object
#the function example_local() shows the original code
def setup_remote_object():

    def wrapped_function():
        from flaskcom.complex_test_class import ComplexTestClass
        test_object = ComplexTestClass('hallo') #initialize the object you want to use
        return test_object 
    

    from flaskcom.remote_object import RemoteObject
    from flaskcom.remote_object import VERBOSITY_INFO
    
    admin_remote_object = RemoteObject(wrapped_function = wrapped_function, #the function that initializes the remote object
                               path_to_virtualenv = "./env3", #a virtualenv on the remote server can loaded before exectuting the code in the remote server.
                               server = "localhost", #the remote object, may be running on another computer, in this case it is the same computer
                               original_working_directory = ".", #a working directory can be specified, which can be used to search for the code
                               keep_open = True, #the remote object can be kept open, when the program is exectuted the next time, it will use the open remote object instead of creating a new one
                               time_out = -1, #the time to wait for the remote terminal to start, -1 means forever
                               debug = True, #keeps the terminal open even if an error occurs
                               verbosity_level = VERBOSITY_INFO, # makes flaskcom more verbose for debugging, can be changed to VERBOSITY_ERROR to be less verbose
                               username = "johannes", #the admin username for the remote object
                               password = "mypassword1",
                               admin_username = "johannes",
                               reser_user_db = False) #the admin password for the remote object

    port = admin_remote_object.RO_port
    print(port)
    
    new_user = "martin"
    new_password = "mypassword2"
    
    admin_remote_object.RO_add_user(new_user, new_password)

    

    test_object = RemoteObject(wrapped_function = wrapped_function, #the function that initializes the remote object
                           path_to_virtualenv = "./env3", #a virtualenv on the remote server can loaded before exectuting the code in the remote server.
                           server = "localhost", #the remote object, may be running on another computer, in this case it is the same computer
                           original_working_directory = ".", #a working directory can be specified, which can be used to search for the code
                           keep_open = True, #the remote object can be kept open, when the program is exectuted the next time, it will use the open remote object instead of creating a new one
                           time_out = -1, #the time to wait for the remote terminal to start, -1 means forever
                           debug = True, #keeps the terminal open even if an error occurs
                           verbosity_level = VERBOSITY_INFO, # makes flaskcom more verbose for debugging, can be changed to VERBOSITY_ERROR to be less verbose
                           username = new_user, #the admin username for the remote object
                           password = new_password, #the admin password for the remote object
                           start_server = False,
                           port = port) 
    
    
    print("doing the object stuff")
    
    #do some stuff with the object
    test_object.value = "this is a value"
    print(test_object.value == "this is a value")
    filename = "./random.file"
    image = test_object.get_image(filename)
    print("type(image):",type(image)    )
    print("test_object.value:",test_object.value)
    print(type(test_object))
    print("thats it")
    
    #test_object.RO_meta_function("shutdown")

if __name__ == "__main__":
    setup_remote_object()