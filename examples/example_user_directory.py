#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 24 14:56:41 2021

@author: twiefel
"""

#this is an example how to create a remote object
#the function example_local() shows the original code
def setup_remote_object():

    def wrapped_function():
        class UserDirectoryTest:
            def write_data_to_user_directory(self, text):
                from flaskcom.user import get_user_directory
                file_path = get_user_directory()+"/test_file.txt"
                with open(file_path, "w") as f:
                    f.write(text)
                return file_path
        user_directory_test_object = UserDirectoryTest()
        return user_directory_test_object 
    

    from flaskcom.remote_object import RemoteObject
    from flaskcom.remote_object import VERBOSITY_INFO
    
    admin_username = "johannes"
    admin_password = "mypassword1"
    
    admin_remote_object = RemoteObject(wrapped_function = wrapped_function, #the function that initializes the remote object
                               path_to_virtualenv = "./env3", #a virtualenv on the remote server can loaded before exectuting the code in the remote server.
                               server = "localhost", #the remote object, may be running on another computer, in this case it is the same computer
                               original_working_directory = ".", #a working directory can be specified, which can be used to search for the code
                               keep_open = True, #the remote object can be kept open, when the program is exectuted the next time, it will use the open remote object instead of creating a new one
                               time_out = -1, #the time to wait for the remote terminal to start, -1 means forever
                               debug = True, #keeps the terminal open even if an error occurs
                               verbosity_level = VERBOSITY_INFO, # makes flaskcom more verbose for debugging, can be changed to VERBOSITY_ERROR to be less verbose
                               username = admin_username, #the admin username for the remote object
                               password = admin_password,
                               admin_username = admin_username,
                               reser_user_db = False) #the admin password for the remote object

    port = admin_remote_object.RO_port
    print(port)
    
    text = "this is example text of "+admin_username
    
    print("filepath admin:", admin_remote_object.write_data_to_user_directory(text))
    
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
    
    text = "this is example text of "+new_user
    
    print("filepath user:", test_object.write_data_to_user_directory(text))


if __name__ == "__main__":
    setup_remote_object()