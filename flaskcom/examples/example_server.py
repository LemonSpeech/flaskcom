# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 16:50:04 2018

@author: twiefel
"""


#this is an example how to create a server
def example_server():
    print
    print("----------------------")
    print("running example_server")
    
    outside_variable = "B" #this variable is initialized in the main program
    
    #this function is run by the remote server
    #put all code inside that is needed to initialize your remote object
    def wrapped_function():
        print("starting wrapped function")

        #for example we import a class here.
        #make sure the package of the class is installed in the virtualenv provided to path_to_virtualenv
        #it is not necessary that the package is installed on the client virtualenv
        from flaskcom.complex_test_class import ComplexTestClass
        print(outside_variable) # this variable is used by the remote terminal and therefore copied over.
        #you shouldn't refer to big objects here, as they have to be copied via socket.
        #Better only use things you really need, or initialize big objects within this function.
        
        inside_variable = outside_variable
        
        print("inside_variable:",inside_variable)
        
        test_object = ComplexTestClass('hallo') #initialize the object you want to use
        
        print("end wrapped function")
        return test_object #return the object that you want to use at the main problem
        #the object runs on the remote server but can be used like a normal object in the main program (with some limitations)
        
    

    from flaskcom.remote_object import RemoteObject
    from flaskcom.remote_object import VERBOSITY_INFO
    from flaskcom.remote_object import VERBOSITY_ERROR
    
    #creates the server object from the wrapped_function
    test_server = RemoteObject(wrapped_function = wrapped_function, #the function that initializes the remote object
                               path_to_virtualenv = "./env3", #a virtualenv can loaded before exectuting the code in the remote terminal.
                               server = "localhost", #must be localhost. this script can only be started when started from the server
                               #server = "localhost", #the remote object is on this computer
                               port=50000, # a port needs to be specified
                               new_terminal_window = False, #forces the code to be run in the terminal it was started from
                               original_working_directory = ".", #a working directory can be specified, which can be used to search for the code
                               keep_open = False, #the terminal is not kept open. if True, the server will run in the background till the terminal is closed
                               time_out = -1, #the time to wait for the remote terminal to start, -1 means forever
                               wait_for_errors = 0, #dont wait for the server to be started
                               verbosity_level = VERBOSITY_INFO, # makes flaskcom more verbose for debugging, can be changed to VERBOSITY_ERROR to be less verbose
                               username = "admin", #the admin username for the remote object
                               password = "mypassword1") #the admin password for the remote object
    input("press enter to shutdown the server") #when keep_open is False, this prevents the server to stop immediately
    #the remote server was created
    #check example_client.py to use it
    #run example_client.py in another terminal, keep this terminal open


if __name__ == "__main__":
    example_server()

