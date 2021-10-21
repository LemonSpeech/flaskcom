# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 14:36:42 2018

@author: twiefel
"""
from __future__ import print_function
import requests
import json

#import dill
import pickle as dill
#dill.HIGHEST_PROTOCOL = 2
#dill.DEFAULT_PROTOCOL = 2
PICKLE_PROTOCOL = 2

import traceback

from .dummy_exception import DummyException

import sys


from .errorprint import print_error
from .marshalling import Marshaller

VERBOSITY_ERROR = 1
VERBOSITY_INFO = 0


def get_methods_without_import(wrapped_module, wrapped_class):
    import pkgutil
    package = pkgutil.get_loader(wrapped_module)
    import ast

    def show_info(functionNode):
        print("Function name:", functionNode.name)
        print("Args:")
        for arg in functionNode.args.args:
            print(arg.id)
    
    def get_method_as_list(method):
        method_as_list =  [method.name]
        for arg in method.args.args:
            method_as_list.append(arg.id)
        return method_as_list
    

    
    filename = package.filename
    with open(filename) as file:
        node = ast.parse(file.read())
    
    classes = [n for n in node.body if isinstance(n, ast.ClassDef)]
    

    methods_as_list = []   
    for class_ in classes:
        if class_.name != wrapped_class:
            continue
        #print("Class name:", class_.name)
        methods = [n for n in class_.body if isinstance(n, ast.FunctionDef)]
        for method in methods:
            methods_as_list.append(method.name)
            #show_info(method)
    
    return methods_as_list

current_object_id = 0
default_port = 55000
class RemoteObject(object):
    def __init__(self, port = -1, 
                 path_to_virtualenv = "", 
                 original_working_directory = ".", 
                 flaskcom_path = "../", 
                 source_commands = "", 
                 server = "localhost", 
                 wrapped_function = None, 
                 keep_open = False, 
                 time_out = 20, 
                 debug = False, 
                 start_server = True,
                 verbosity_level = VERBOSITY_ERROR,
                 username = "default_user",
                 password = "default_password",
                 new_terminal_window = True,
                 wait_for_errors = 10):

        self.RO_server = server
        self.RO_port = port
        self.RO_keep_open = keep_open
        self.RO_debug = debug
        self.RO_time_out = time_out
        self.RO_flaskcom_path = flaskcom_path
        self.RO_verbosity_level = verbosity_level
        self.RO_session = requests.Session()

        self.RO_password = password
        self.RO_username = username
        
        self.RO_wait_for_errors = wait_for_errors
            
#        dill.HIGHEST_PROTOCOL = 2
#        dill.DEFAULT_PROTOCOL = 2
#        
#        if verbosity_level<1:
#            print("Python Version")
#            print(sys.version)
#            print("Pickle Protocol")
#            print(dill.HIGHEST_PROTOCOL)





        global current_object_id
        if self.RO_verbosity_level<1:
            print("Creating Remote Object with ID",current_object_id)


        self.RO_object_id = current_object_id
        current_object_id += 1
        
        if self.RO_port == -1:
            self.RO_port = default_port+self.RO_object_id


        self.RO_marshaller = Marshaller(verbosity_level,username,password,self.RO_session,self.RO_server,self.RO_port)

        

        

        authenticated = self.RO_authenticate()
        if self.RO_verbosity_level<1:
            print("client is authenticated:",authenticated)

        status = self.RO_meta_function("status") 
        if self.RO_verbosity_level<1:print("server status:",status)
        if status == b"Unauthorized":
            print("server is running, but client is not authorized")
            authenticated = self.RO_authenticate()
            print("client is authenticated:",authenticated)
        if self.RO_verbosity_level<1:    
            print (status == "down")
        if start_server:
            if status == "down":
                if wrapped_function == None:
                    print("define wrapped_function")
                    raise NotImplementedError
                virtualenv_source_command = self.RO_marshaller.get_virtualenv_command(path_to_virtualenv, server)
                cd_command = self.RO_marshaller.get_cd_command(original_working_directory, server)
                shell_command = self.RO_marshaller.get_shell_command(server)
                source_commands = self.RO_marshaller.get_source_command(source_commands)
                geometry_command = self.RO_marshaller.get_geometry_command(self.RO_object_id)

                if wrapped_function != None:

                
                    python_command = self.RO_marshaller.get_python_command_for_server_in_file(wrapped_function,server,self.RO_port,flaskcom_path, original_working_directory, path_to_virtualenv, initial_user = self.RO_username, initial_password= self.RO_password)

                debug_command = self.RO_marshaller.get_debug_command(debug)

                if verbosity_level<1:
                    print(virtualenv_source_command)
                    print(cd_command)
                    print(source_commands)
                    print(python_command)
                    print(debug_command)

                inside_shell_command = virtualenv_source_command + cd_command+source_commands+python_command+debug_command
                if new_terminal_window:
                    command = ["gnome-terminal"+geometry_command+ " -x "+shell_command+" ' "+inside_shell_command+"' " ]
                else:
                    command = [inside_shell_command]
                if verbosity_level<1:                
                    print(command)
                    print("running in")
                    print(cd_command)
                self.RO_marshaller.start_server_terminal(command,self.RO_meta_function,time_out,self.RO_wait_for_errors)
                if self.RO_verbosity_level<1:print("server terminal started")
                status2 = self.RO_meta_function("status") 
                if self.RO_verbosity_level<1:print("server status:",status2)
                #raise
                if not self.RO_authenticate():
                    print("could not authenticate")
                    sys.exit(1)
                if wrapped_function != None:
                    if self.RO_verbosity_level<1:print("initializing wrapped function on the server")
                    self.RO_marshaller.init_server_with_wrapped_function_raw(wrapped_function,self.RO_meta_function)
                else:
                    print("wrapped_function needs to be given if start_server is True")
                    raise Exception
                

                    

        elif status == "down":
            print_error( "the server is not reachable")
            sys.exit(1)
        
        if self.RO_verbosity_level<1:print("server should run")

    def __del__(self):
        if self.RO_keep_open:
            print("keeping terminal open")
        else:
            self.RO_meta_function("shutdown")
    def RO_authenticate(self):
        return self.RO_marshaller.authenticate()

            
    def RO_meta_function(self, payload):
        if self.RO_verbosity_level<1: print("calling RO_meta_function",payload[:20],"...")
        status = "False"
        try:
            r = self.RO_session.post("http://"+self.RO_server+":"+str(self.RO_port)+"/"+"__meta_function__", data=payload)
            return_value = r.content.decode("utf-8")
            if self.RO_verbosity_level<1: 
                print("REQUEST",payload)
                print("CONTENT",return_value)
            splitted_content = return_value.split("____")
            if splitted_content[0] == "EXCEPTION":
                print
                print
                print("EXCEPTION OCCURRED IN REMOTE OBJECT, SEE OTHER CONSOLE")
                print(splitted_content[1])
                raise Exception

            status = return_value
        except Exception as err:
            if self.RO_verbosity_level<1: 
                print("an exception occured when using meta_function")
                print(err)
            #exc_info = sys.exc_info()
            #traceback.print_exception(*exc_info)
            #del exc_info
            if payload == "isup" or payload == "status":
                status = "down"
            else:
                print("call",payload[:20],"failed")
                sys.exit(1)
        if self.RO_verbosity_level<1: print("returning RO_meta_function:",status,)
        return status
    def __setattr__(self, name, value):

        if not name.startswith("RO_"):
            payload = {'attr':name, 'value':value}

            data = dill.dumps(payload, protocol = PICKLE_PROTOCOL)
            r = self.RO_session.post("http://"+self.RO_server+":"+str(self.RO_port)+"/"+"__setattr__", data=data)
        else:
            super(RemoteObject, self).__setattr__(name, value)


    def __getattr__(self,attr):
        if attr.startswith("RO_"):
            if self.RO_verbosity_level<1: 
                print("requesting:",attr)
            return super(RemoteObject, self).__getattr__(attr)
            
        payload = {'attr':attr}

        data = dill.dumps(payload, protocol = PICKLE_PROTOCOL)
        r = self.RO_session.post("http://"+self.RO_server+":"+str(self.RO_port)+"/"+"__getattr__", data=data)
        result = dill.loads(r.content)

        if isinstance(result, DummyException):
            print(result.exception_info)
            import sys
            sys.exit()

        
        if not callable(result):
            return result
        
        def hooked(*args, **kwargs):
            payload = {'attr':attr, 'args':args,"kwargs":kwargs}

            data = dill.dumps(payload, protocol = PICKLE_PROTOCOL)
            r = self.RO_session.post("http://"+self.RO_server+":"+str(self.RO_port)+"/"+"__call__", data=data)
            result = dill.loads(r.content)

            if isinstance(result, DummyException):
                print(result.exception_info)
                import sys
                sys.exit()

            return result

        return hooked


