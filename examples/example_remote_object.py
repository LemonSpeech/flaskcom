# -*- coding: utf-8 -*-
"""
Created on Fri Feb  8 11:37:01 2019

@author: twiefel
"""
#this is an example how to create a remote object
#the function example_local() shows the original code
def example_remote():
    print
    print("----------------------")
    print("running example_remote")
    
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
        
    
    #import the RemoteObject
    from flaskcom.remote_object import RemoteObject
    from flaskcom.remote_object import VERBOSITY_INFO
    
    #wrap it around the function
    #returns an object that can be used like the object initialized in the wrapped function,
    #here: test_object = ComplexTestClass('hallo')
    test_object = RemoteObject(wrapped_function = wrapped_function, #the function that initializes the remote object
                               path_to_virtualenv = "./env3", #a virtualenv on the remote server can loaded before exectuting the code in the remote server.
                               server = "localhost", #the remote object, may be running on another computer, in this case it is the same computer
                               original_working_directory = ".", #a working directory can be specified, which can be used to search for the code
                               keep_open = True, #the remote object can be kept open, when the program is exectuted the next time, it will use the open remote object instead of creating a new one
                               time_out = -1, #the time to wait for the remote terminal to start, -1 means forever
                               debug = True, #keeps the terminal open even if an error occurs
                               verbosity_level = VERBOSITY_INFO, # makes flaskcom more verbose for debugging, can be changed to VERBOSITY_ERROR to be less verbose
                               username = "johannes", #the admin username for the remote object
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

#the original code, that was modified to use a remote object in example_remote()
def example_local():
    print
    print("----------------------")
    print("running example_local")
    
    outside_variable = "B" #this variable is initialized in the main program
    
    #this function is run to initialize the object
    def wrapped_function():
        print("starting wrapped function")

        from flaskcom.complex_test_class import ComplexTestClass
        print(outside_variable )
        inside_variable = outside_variable
        
        print("inside_variable:",inside_variable)
        
        test_object = ComplexTestClass('hallo') #initialize the object you want to use
        
        print("end wrapped function")
        return test_object #return it
    
    #initialize the object with the function. This part is replaced later to initialize the romote object
    test_object = wrapped_function()
    
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
    example_remote()
    example_local()
