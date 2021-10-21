# -*- coding: utf-8 -*-
"""
Created on Fri Feb  8 11:37:01 2019

@author: twiefel
"""
#this is an example how to create a remote object
#the function example_local() shows the original code
def example_client():
    print
    print("----------------------")
    print("running example_client")
    
    #import the RemoteObject
    from flaskcom.remote_object import RemoteObject
    from flaskcom.remote_object import VERBOSITY_INFO
    
    #returns an object that can be used
    test_object = RemoteObject(server = "localhost", #the remote object is on this computer
                               port=50000, # a port needs to be specified
                               start_server = False, #the server is not started, it should be there already
                               new_terminal_window = False, #forces the code to be run in the terminal it was started from
                               time_out = -1, #the time to wait for the remote terminal to start, -1 means forever
                               debug = True, #keeps the terminal open even if an error occurs
                               verbosity_level = VERBOSITY_INFO, # makes flaskcom more verbose for debugging, can be changed to VERBOSITY_ERROR to be less verbose
                               username = "admin", #the admin username for the remote object
                               password = "mypassword1") #the admin password for the remote object
    #the remote object was created
    #use it as a normal object
    #but always think about every function call is sent via networ/internet so maybe slower
    #try to reduce the communication as much as possible
    
    #when this program ends, the object is still available in another terminal
    #when
    
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


    


if __name__ == "__main__":
    example_client()

