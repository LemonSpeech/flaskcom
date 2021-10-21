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
    
    #this function is run by the remote terminal
    #put all code inside that is needed to initialize your remote object
    def wrapped_function():
        print("starting wrapped function")

        from flaskcom.complex_test_class import ComplexTestClass
        print(outside_variable) # this variable is used by the remote terminal and therefore copied over.
        #you shouldn't refer to big objects here, as they have to be copied via socket.
        #Better only use thinks you really need, or initialize big objects within this function.
        
        inside_variable = outside_variable
        
        print("inside_variable:",inside_variable)
        
        test_object = ComplexTestClass('hallo') #initialize the object you want to use
        
        print("end wrapped function")
        return test_object #return it
    
    #import the RemoteObject
    from flaskcom.remote_object import RemoteObject
    
    #wrap it around the function
    #returns an object that can be used like the object initialized in the wrapped function,
    #here: test_object = ComplexTestClass('hallo')
    test_object = RemoteObject(wrapped_function = wrapped_function, #the function that initializes the remote object
                               path_to_virtualenv = "../venv", #a virtualenv can loaded before exectuting the code in the remote terminal.
                               server = "localhost", #the remote object is running on another computer
                               original_working_directory = ".", #a working directory can be specified, which can be used to search for the code
                               keep_open = True, #the remote object can be kept open, when the program is exectuted the next time, it will use the open remote object instead of creating a new one
                               time_out = -1, #the time to wait for the remote terminal to start, -1 means forever
                               flaskcom_path = "./", #if flaskcom is not inside the searchpath, set a path to a folder containing flaskcom
                               debug = True,
                               verbosity_level = 0,
                               username = "johannes",
                               password = "mypassword1") #keeps the terminal open even if an error occurs
    
    print("doing the object stuff")
    
    #do some stuff with the object
    test_object.value = "this is a value"
    print(test_object.value == "this is a value")
    filename = "./flaskcom/wtmIcon_orig.png"
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
    filename = "./flaskcom/wtmIcon_orig.png"
    image = test_object.get_image(filename)
    print("type(image):",type(image)    )
    print("test_object.value:",test_object.value)
    print(type(test_object))
    print("thats it")
    


if __name__ == "__main__":
    example_remote()
    example_local()
