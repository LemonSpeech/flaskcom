# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 16:49:05 2018

@author: twiefel
"""
from __future__ import print_function
import sys
from flask import Flask, request, jsonify
import base64
import dill
import traceback
from .dummy_callable import DummyCallable
from .dummy_exception import DummyException
from .dummy_object import DummyObject
import json
from pprint import pprint
import os
import importlib

class Server(object):
    def __init__(self, wrapped_class, port, verbosity_level = 0):
        self.wrapped_class = wrapped_class
        self.port = port

        self.app = Flask(__name__)
        self.verbosity_level = verbosity_level
        def getattr_handler_function():
            if verbosity_level<1:
                print(str(request.url_rule))

            attr = str(request.url_rule)[1:]
            if verbosity_level<1:
                print("getting attr",[attr])
            
            try:


                new_data = dill.loads(request.data)
                if verbosity_level<1:
                    print(new_data)
                attr = new_data["attr"]
                if verbosity_level<1:
                    print("getting attr",[attr])

                orig_attr = getattr(self.wrapped_class,attr)
                if callable(orig_attr):
                    return_values = DummyCallable()
                else:
                    return_values = orig_attr
            except Exception, err:
                print("exception")
                exc_info = sys.exc_info()
                print(type(err))
                print(isinstance(err, Exception))
                print(exc_info)
                return_values = err
                return_values = DummyException()
                exc_info = sys.exc_info()
                traceback.print_exception(*exc_info)
                del exc_info

            pickled_return_values = dill.dumps(return_values)
            return pickled_return_values

        def call_handler_function():
            if verbosity_level<1:
                print(str(request.url_rule))

            attr = str(request.url_rule)[1:]
            if verbosity_level<1:
                print("handling call",[attr])
            
            try:

                new_data = dill.loads(request.data)
                
                if verbosity_level<1:
                    print(new_data)
                    
                attr = new_data["attr"]
                
                if verbosity_level<1:
                    print("getting attr",[attr])
                
                orig_attr = getattr(self.wrapped_class,attr)
                
                return_values = orig_attr(*new_data["args"],**new_data["kwargs"])
                
                    
            except Exception, err:
                print("exception")
                exc_info = sys.exc_info()
                print(type(err))
                print(isinstance(err, Exception))
                print(exc_info)
                return_values = err
                return_values = DummyException()
                exc_info = sys.exc_info()
                traceback.print_exception(*exc_info)



            pickled_return_values = dill.dumps(return_values)
            return pickled_return_values
                
        def setattr_handler_function():

            new_data = dill.loads(request.data)
            
            attr = new_data["attr"]
            
            value = new_data["value"]
            if verbosity_level<1:
                print("setting attr",[attr],[value])
            setattr(self.wrapped_class,attr,value)
            
            return "None"
        
        def meta_handler_function():
            command = request.data
            return_value = "True"
            if self.verbosity_level < 1:
                print("incoming meta request:", command[:30],"...")
            if command == "shutdown":
                func = request.environ.get('werkzeug.server.shutdown')
                if func is None:
                    raise RuntimeError('Not running with the Werkzeug Server')
                func()
            if command == "status":
                if self.verbosity_level < 1:
                    print("checking status",self.wrapped_class)

                if type(self.wrapped_class) == DummyObject:
                    return_value = "INITIALIZING"
                elif type(self.wrapped_class) == DummyException:
                    return_value = "ERROR"
                else:
                    return_value =  "RUNNING_"+str(type(self.wrapped_class))+"_"+self.ID

            if command.startswith("initstringcode"):
                
                if self.verbosity_level < 1:
                    print("initializing function with string code")
                try:
                    print(command)
                    base64_encoded_dilled_function = command.split("_")[1]
    
                    base64_decoded_dilled_function = base64.decodestring(base64_encoded_dilled_function)
    
                    undilled_function = dill.loads(base64_decoded_dilled_function)
                    
                    def tuplify(value):
                        if isinstance(value, list):
                            return tuple(tuplify(x) for x in value)
                        elif isinstance(value, dict):
                            for key,value2 in value.iteritems():
                                value[key] = tuplify(value2)
                            return value
                        if isinstance(value, tuple):
                            return tuple(tuplify(x) for x in value)
                        else:
                            return value     
                     
                    def freeze(data):
                        return frozenset(data)[0]
                    
                    if self.verbosity_level < 1:
                        print(undilled_function)
                        print("base64_decoded_dilled_function hash",hash(base64_decoded_dilled_function))
                        print("base64_encoded_dilled_function hash", hash(base64_encoded_dilled_function))
                        print("undilled_function code hash",hash(undilled_function[0]))
                    
    
                    if len(undilled_function[1])>0:
                        if self.verbosity_level < 1:
                            print("found free vars:")
                            print(undilled_function[1])
    
                        for free_var,closure_val in undilled_function[1]:
                            if self.verbosity_level < 1:
                                print(free_var,"=", closure_val)
    
                    code_lines = undilled_function[0].splitlines()
                    function_name = code_lines[0].split("(")[0].split("def")[1].strip()
                    leading_spaces = len(code_lines[0].split("def")[0])
                    if self.verbosity_level < 1:
                        print(leading_spaces)
                        print(function_name)
                        
                    code_lines[0]=code_lines[0].replace(function_name,"marshalled_function")
                    
                    tuplified_undilled_function = tuplify(undilled_function)
    
                    if self.verbosity_level < 1: pprint(tuplified_undilled_function)
    
                    module_name = "flaskcom_tmp_"+str(hash(tuplified_undilled_function))
                    
                    function_parameters = ", ".join([free_var[0] for free_var in undilled_function[1]])
                    function_signature = "def marshalled_function("+function_parameters+"):"
                    
                    with open("/tmp/"+module_name+".py", "wb") as f:
                        f.write(function_signature+"\n")
                        for code_line in code_lines[1:]:
                            stripped_code_line = code_line.lstrip()
                            code_line = code_line[min(leading_spaces, len(code_line)-len(stripped_code_line)):]
                            f.write(code_line+"\n")
                    if self.verbosity_level < 1:
                        print(module_name)
                        print("i am here",os.getcwd())
                        
                    sys.path.append(os.getcwd())
    
                    pprint( sys.path)
                    
                    sys.path.append("/tmp/")
                    module = importlib.import_module(module_name)
                    function_arguments = [free_var[1] for free_var in undilled_function[1]]
                    wrapped_object = module.marshalled_function(*function_arguments)
    
                    self.wrapped_class = wrapped_object
                    self.ID = base64_encoded_dilled_function[:10]
                    
                    if self.verbosity_level < 1: print("initialized",self.wrapped_class)
                    return_value =  "RUNNING____"+str(type(self.wrapped_class))+"____"+self.ID
                except Exception:
                    import traceback
                    tb = traceback.format_exc()
                    return_value = "EXCEPTION____"+tb
                    
            if self.verbosity_level < 1: print("returning",return_value)
            return return_value
            
        self.app.add_url_rule(rule='/'+"__meta_function__", view_func = meta_handler_function,methods=['POST',])            

        self.app.add_url_rule(rule='/'+"__getattr__", view_func = getattr_handler_function,methods=['POST',])

        self.app.add_url_rule(rule='/'+"__setattr__", view_func = setattr_handler_function,methods=['POST',])
        
        self.app.add_url_rule(rule='/'+"__call__", view_func = call_handler_function,methods=['POST',])
    
    def start(self):
        
        self.app.run(host='0.0.0.0',port=self.port, debug=False, use_reloader=False, threaded=True)
    
    def stop(self):
        self.app.shutdown()
    
    def __del__(self):
        self.stop()
        

