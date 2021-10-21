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

class Server(object):
    def __init__(self, wrapped_class, port, verbosity_level = 0):
        self.S_wrapped_class = wrapped_class
        self.S_port = port

        self.S_app = Flask(__name__)
        self.S_verbosity_level = verbosity_level
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

                orig_attr = getattr(self.S_wrapped_class,attr)
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
                    
                orig_attr = getattr(self.S_wrapped_class,attr)
                
                if verbosity_level<2:
                    print(attr+"(...)","was called")
                    
                if callable(orig_attr):
                    if verbosity_level<1:
                        print("calling",new_data)
                    def hooked(*args, **kwargs):
                        result = orig_attr(*args, **kwargs)
                        # prevent wrapped_class from becoming unwrapped
                        if type(result) == type(self.S_wrapped_class) and result == self.S_wrapped_class:
                            return self
                        return result
                    return_values = hooked(*new_data["args"],**new_data["kwargs"])
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



            pickled_return_values = dill.dumps(return_values)
            return pickled_return_values
                
        def setattr_handler_function():

            new_data = dill.loads(request.data)
            
            attr = new_data["attr"]
            
            value = new_data["value"]
            if verbosity_level<1:
                print("setting attr",[attr],[value])
            setattr(self.S_wrapped_class,attr,value)
            return "None"
        
        def meta_handler_function():
            command = request.data
            return_value = "True"
            print("incoming meta request:", command[:30],"...")
            if command == "shutdown":
                func = request.environ.get('werkzeug.server.shutdown')
                if func is None:
                    raise RuntimeError('Not running with the Werkzeug Server')
                func()
            if command == "status":
                print("checking status",self.S_wrapped_class)
                #print(type(self.S_wrapped_class) == DummyObject)
                #print(type(self.S_wrapped_class) == DummyException)
                if type(self.S_wrapped_class) == DummyObject:
                    return_value = "INITIALIZING"
                elif type(self.S_wrapped_class) == DummyException:
                    return_value = "ERROR"
                else:
                    return_value =  "RUNNING_"+str(type(self.S_wrapped_class))+"_"+self.S_ID
            if command.startswith("initbytecode"):
                print("initializing function")
                base64_encoded_dilled_function = command.split("_")[1]
                #print(base64_encoded_dilled_function)
                base64_decoded_dilled_function = base64.decodestring(base64_encoded_dilled_function)
                #print(base64_decoded_dilled_function)
                undilled_function = dill.loads(base64_decoded_dilled_function)
                
                print(undilled_function)
                print("undilled_function hash",hash(undilled_function))
                print("base64_decoded_dilled_function hash",hash(base64_decoded_dilled_function))
                print("base64_encoded_dilled_function hash", hash(base64_encoded_dilled_function))
                print("undilled_function code hash",hash(undilled_function.__code__.co_code))
                
                print("has __code__",hasattr(undilled_function,"__code__"))
                print(type(undilled_function))
                #print(locals())
                if hasattr(undilled_function.__code__, "co_freevars") and len(undilled_function.__code__.co_freevars)>0:
                    print("found free vars:")
                    print(undilled_function.__code__.co_freevars)
                    for free_var,closure_val in zip(undilled_function.__code__.co_freevars,undilled_function.__closure__):
                        #import numpy as np                        
                        print(free_var,"=", closure_val.cell_contents)
#                    print(vars())
#                    #wrapped_function()
#                    print(dir(undilled_function.__code__))
#                    print(undilled_function.__globals__)
#                    print("A",undilled_function.__code__.co_freevars    )
#                    print(undilled_function.__code__.co_nlocals)
#                    print(undilled_function.__code__.co_consts)
#                    print(undilled_function.__dict__)
#                    print(undilled_function.__defaults__)
#                    print(undilled_function.__closure__)
#                    print(undilled_function.__closure__[0].cell_contents)
#                    print(undilled_function.__code__.co_cellvars)
#               print
                import inspect
#                def blub():
#                    pass
#                print(inspect.getsource(blub.__code__))
                print
                print("function:")
                try:
                    print( inspect.getsource(undilled_function.__code__))
                except IOError:
                    print()
                    print("CANNOT DISPLAY SOURCE CODE")
                wrapped_object = undilled_function()#
                self.S_wrapped_class = wrapped_object
                self.S_ID = base64_encoded_dilled_function[:10]
                print("initialized",self.S_wrapped_class)
                return_value =  "RUNNING____"+str(type(self.S_wrapped_class))+"____"+self.S_ID
            if command.startswith("initstringcode"):
                print("initializing function")
                try:
                    base64_encoded_dilled_function = command.split("_")[1]
                    #print(base64_encoded_dilled_function)
                    base64_decoded_dilled_function = base64.decodestring(base64_encoded_dilled_function)
                    #print(base64_decoded_dilled_function)
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
                    
                    
                    print(undilled_function)
                    #print("undilled_function hash",hash(undilled_function))
                    print("base64_decoded_dilled_function hash",hash(base64_decoded_dilled_function))
                    print("base64_encoded_dilled_function hash", hash(base64_encoded_dilled_function))
                    print("undilled_function code hash",hash(undilled_function[0]))
                    
                    
                    #print("has __code__",hasattr(undilled_function,"__code__"))
                    #print(type(undilled_function))
                    #print(locals())
                    if len(undilled_function[1])>0:
                        print("found free vars:")
                        print(undilled_function[1])
    
                        for free_var,closure_val in undilled_function[1]:
                            #import numpy as np                        
                            print(free_var,"=", closure_val)
    #                    print(vars())
    #                    #wrapped_function()
    #                    print(dir(undilled_function.__code__))
    #                    print(undilled_function.__globals__)
    #                    print("A",undilled_function.__code__.co_freevars    )
    #                    print(undilled_function.__code__.co_nlocals)
    #                    print(undilled_function.__code__.co_consts)
    #                    print(undilled_function.__dict__)
    #                    print(undilled_function.__defaults__)
    #                    print(undilled_function.__closure__)
    #                    print(undilled_function.__closure__[0].cell_contents)
    #                    print(undilled_function.__code__.co_cellvars)
    #               print
    #                import inspect
    ##                def blub():
    ##                    pass
    ##                print(inspect.getsource(blub.__code__))
    #                print
    #                print("function:")
    #                try:
    #                    undilled_function[0]
    #                except IOError:
    #                    print()
    #                    print("CANNOT DISPLAY SOURCE CODE")
    #                print("current  working directory")
    #                import os
    #                print(os.getcwd())
                    code_lines = undilled_function[0].splitlines()
                    function_name = code_lines[0].split("(")[0].split("def")[1].strip()
                    leading_spaces = len(code_lines[0].split("def")[0])
                    print(leading_spaces)
                    print(function_name)
                    code_lines[0]=code_lines[0].replace(function_name,"marshalled_function")
                    
                    tuplified_undilled_function = tuplify(undilled_function)
                    from pprint import pprint
                    pprint(tuplified_undilled_function)
                    #hash(([]))
                    #raw_input()
                    module_name = "flaskcom_tmp_"+str(hash(tuplified_undilled_function))
                    function_parameters = ", ".join([free_var[0] for free_var in undilled_function[1]])
                    function_signature = "def marshalled_function("+function_parameters+"):"
                    with open("/tmp/"+module_name+".py", "wb") as f:
                        f.write(function_signature+"\n")
                        for code_line in code_lines[1:]:
                            stripped_code_line = code_line.lstrip()
                            code_line = code_line[min(leading_spaces, len(code_line)-len(stripped_code_line)):]
                            f.write(code_line+"\n")
                            #f.write(undilled_function[0])
                    print(module_name)
                    import os
                    print("i am here",os.getcwd())
                    sys.path.append(os.getcwd())
                    from pprint import pprint
                    pprint( sys.path)
                    
                    import importlib
                    sys.path.append("/tmp/")
                    module = importlib.import_module(module_name)
                    function_arguments = [free_var[1] for free_var in undilled_function[1]]
                    wrapped_object = module.marshalled_function(*function_arguments)
                    #raise
                    
                    
                    #wrapped_object = undilled_function()#
                    self.S_wrapped_class = wrapped_object
                    self.S_ID = base64_encoded_dilled_function[:10]
                    print("initialized",self.S_wrapped_class)
                    return_value =  "RUNNING____"+str(type(self.S_wrapped_class))+"____"+self.S_ID
                except Exception:
                    import traceback
                    tb = traceback.format_exc()
                    return_value = "EXCEPTION____"+tb
            print("returning",return_value)
            return return_value
            
        self.S_app.add_url_rule(rule='/'+"__meta_function__", view_func = meta_handler_function,methods=['POST',])            
        #app.add
        self.S_app.add_url_rule(rule='/'+"__getattr__", view_func = getattr_handler_function,methods=['POST',])
        #app.add_url_rule('/'+"__setattr__","server", setattr_handler_function,methods=['POST',]) 
        self.S_app.add_url_rule(rule='/'+"__setattr__", view_func = setattr_handler_function,methods=['POST',])
        
        self.S_app.add_url_rule(rule='/'+"__call__", view_func = call_handler_function,methods=['POST',])
    
    def S_start(self):
        
        self.S_app.run(host='0.0.0.0',port=self.S_port, debug=False, use_reloader=False, threaded=True)
    
    def S_stop(self):
        self.S_app.shutdown()
    
    def __del__(self):
        self.S_stop()
        

    def __getattr__(self,attr):
        if self.S_verbosity_level<1:
            print("getting attribute:", attr)
        if attr.startswith("S_"):
            return super(Server, self).__getattr__(attr)
        orig_attr = self.S_wrapped_class.__getattribute__(attr)
        if callable(orig_attr):
            def hooked(*args, **kwargs):
                #self.pre()
                result = orig_attr(*args, **kwargs)
                # prevent wrapped_class from becoming unwrapped
                if result == self.S_wrapped_class:
                    return self
                #self.post()
                return result
            return hooked
        else:
            return orig_attr
    
    def __setattr__(self, name, value):
        if not name.startswith("S_"):
            self.S_wrapped_class.__setattr__( name, value)
        else:
            super(Server, self).__setattr__(name, value)

    def pre(self):
        print(">> pre")

    def post(self):
        print("<< post")
