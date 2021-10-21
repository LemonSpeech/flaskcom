# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 16:49:11 2018

@author: twiefel
"""
from __future__ import print_function
import requests
import json
import dill
class Client:
    def __init__(self, handler_function,port,server="localhost"):
        self.server = server
        self.port = port
        self.handler_function = handler_function
    def call(self,args):
        #args = ["bli","bla","blub"]
        payload = {'args':args}
        r = requests.post("http://"+self.server+":"+str(self.port)+"/server", data=payload)
        result = r.json()["return_values"]
        return result

def get_methods_without_import(wrapped_module, wrapped_class):
    import pkgutil
    package = pkgutil.get_loader(wrapped_module)
    #print(package.filename)
    import ast

    def show_info(functionNode):
        print("Function name:", functionNode.name)
        print("Args:")
        for arg in functionNode.args.args:
            #print(arg)
            #import pdb; pdb.set_trace()
            #print("\tParameter name:", arg)
            #print(ast.dump(arg))
            print(arg.id)
    
    def get_method_as_list(method):
        method_as_list =  [method.name]
        for arg in method.args.args:
            method_as_list.append(arg.id)
        return method_as_list
    

    
    filename = package.filename
    with open(filename) as file:
        node = ast.parse(file.read())
    
    #functions = [n for n in node.body if isinstance(n, ast.FunctionDef)]
    
    classes = [n for n in node.body if isinstance(n, ast.ClassDef)]
    
    #for function in functions:
    #    show_info(function)
    
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

class ClientWrapperSlim(object):
    def __init__(self,wrapped_module, wrapped_class, port, server="localhost",complex_datatypes = False):
        self.ClientWrapper_wrapped_module = wrapped_module
        self.ClientWrapper_wrapped_class = wrapped_class
        self.ClientWrapper_complex_datatypes = complex_datatypes
        #attrs = vars(self.ClientWrapper_wrapped_class)
        #print(dir(self.ClientWrapper_wrapped_class))
        #print(attrs)
        #print(self.ClientWrapper_wrapped_class.__dict__.items())
        from types import FunctionType
        
        def methods(cls):
            return [x for x, y in cls.__dict__.items() if type(y) == FunctionType]
        #self.ClientWrapper_methods = methods(self.ClientWrapper_wrapped_class)
        self.ClientWrapper_methods = get_methods_without_import(self.ClientWrapper_wrapped_module, self.ClientWrapper_wrapped_class)
        self.ClientWrapper_server = server
        self.ClientWrapper_port = port
    def ClientWrapper_meta_function(self, payload):
        #print("ClientWrapper_meta_function",payload)
        try:
            r = requests.post("http://"+self.ClientWrapper_server+":"+str(self.ClientWrapper_port)+"/"+"__meta_function__", data=payload)
            #print(r.content)
            return r.content
        except:
            if payload == "isup":
                return "False"
            else:
                raise
        return "False"
    def __setattr__(self, name, value):
        #print("__setattr__",name,value)
        #raw_input()
        if not name.startswith("ClientWrapper_"):
            #print("wrapped object attribute")
            payload = {'attr':name, 'value':value}
            #print(payload)
            if not self.ClientWrapper_complex_datatypes:
                data = json.dumps(payload)
                r = requests.post("http://"+self.ClientWrapper_server+":"+str(self.ClientWrapper_port)+"/"+"__setattr__", json=data)
            else:
                data = dill.dumps(payload)
                r = requests.post("http://"+self.ClientWrapper_server+":"+str(self.ClientWrapper_port)+"/"+"__setattr__", data=data)
        else:
            super(ClientWrapperSlim, self).__setattr__(name, value)

    def __getattr__(self,attr):
        if attr.startswith("ClientWrapper_"):
            return super(ClientWrapperSlim, self).__getattr__(attr)
        #print("getting attr",[attr])
        #orig_attr = self.ClientWrapper_wrapped_class.__getattribute__(attr)
        if attr in self.ClientWrapper_methods:
            #print("running method",attr)
            #print("attr",attr,"is callable")
            def hooked(*args, **kwargs):

                #print("args",args)
                #print("kwargs",kwargs)
                #print(attr)
                
                payload = {'attr':attr, 'args':args,"kwargs":kwargs}
                #print("payload",payload)
                if not self.ClientWrapper_complex_datatypes:
                    data = json.dumps(payload)
                    r = requests.post("http://"+self.ClientWrapper_server+":"+str(self.ClientWrapper_port)+"/"+"__getattr__", json=data)
                    result = r.json()["return_values"]
                else:
                    data = dill.dumps(payload)
                    #print("sending")
                    #print([data])
                    r = requests.post("http://"+self.ClientWrapper_server+":"+str(self.ClientWrapper_port)+"/"+"__getattr__", data=data)
                    result = dill.loads(r.content)

                    
                # prevent wrapped_class from becoming unwrapped
                if type(result) == type(self.ClientWrapper_wrapped_class) and result == self.ClientWrapper_wrapped_class:
                    return self
                    
                return result
            if isinstance(hooked, Exception):
                raise hooked
            return hooked
        else:
            #print("running attr",attr)
            payload = {'attr':attr}
            #print("attr",attr,"is not callable")
            #print("payload",payload)
            if not self.ClientWrapper_complex_datatypes:
                data = json.dumps(payload)
                r = requests.post("http://"+self.ClientWrapper_server+":"+str(self.ClientWrapper_port)+"/"+"__getattr__", json=data)
                result = r.json()["return_values"]
            else:
                data = dill.dumps(payload)
                #print("sending")
                #print([data])
                r = requests.post("http://"+self.ClientWrapper_server+":"+str(self.ClientWrapper_port)+"/"+"__getattr__", data=data)
                result = dill.loads(r.content)
            if isinstance(result, Exception):
                raise result
            return result
   

class ClientWrapper:
    def __init__(self,wrapped_class, port, server="localhost",complex_datatypes = False):
        self.wrapped_class = wrapped_class
        self.complex_datatypes = complex_datatypes
        #attrs = vars(self.wrapped_class)
        #print(dir(self.wrapped_class))
        #print(attrs)
        #print(self.wrapped_class.__dict__.items())
        from types import FunctionType
        
        def methods(cls):
            return [x for x, y in cls.__dict__.items() if type(y) == FunctionType]
        self.methods = methods(self.wrapped_class)
        self.server = server
        self.port = port

    def __getattr__local(self,attr):
        #print("getting attr",[attr])
        #orig_attr = self.wrapped_class.__getattribute__(attr)
        orig_attr = getattr(self.wrapped_class,attr)
        
        if callable(orig_attr):
            def hooked(*args, **kwargs):
                self.pre()
                result = orig_attr(*args, **kwargs)
                # prevent wrapped_class from becoming unwrapped
                if result == self.wrapped_class:
                    return self
                self.post()
                return result
            return hooked
        else:
            return orig_attr

    def __getattr__(self,attr):
        #print("getting attr",[attr])
        #orig_attr = self.wrapped_class.__getattribute__(attr)
        if attr in self.methods:
            #print("attr",attr,"is callable")
            def hooked(*args, **kwargs):

                #print("args",args)
                #print("kwargs",kwargs)

                payload = {'args':args,"kwargs":kwargs}
                
                if not self.complex_datatypes:
                    data = json.dumps(payload)
                    r = requests.post("http://"+self.server+":"+str(self.port)+"/"+attr, json=data)
                    result = r.json()["return_values"]
                else:
                    data = dill.dumps(payload)
                    #print("sending")
                    #print([data])
                    r = requests.post("http://"+self.server+":"+str(self.port)+"/"+attr, data=data)
                    result = dill.loads(r.content)

                    
                # prevent wrapped_class from becoming unwrapped
                if type(result) == type(self.wrapped_class) and result == self.wrapped_class:
                    return self
                    
                return result
            return hooked
        else:
            #print("attr",attr,"is not callable")
            r = requests.post("http://"+self.server+":"+str(self.port)+"/"+attr)
            if not self.complex_datatypes:
                result = r.json()["return_values"]
            else:
                result = dill.loads(r.content)
            return result

