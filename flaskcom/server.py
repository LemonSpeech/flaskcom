# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 16:49:05 2018

@author: twiefel
"""

from __future__ import print_function
import sys
from flask import Flask, request
import base64
#import dill
import pickle as dill
PICKLE_PROTOCOL = 2

import traceback
from .dummy_callable import DummyCallable
from .dummy_exception import DummyException
from .dummy_object import DummyObject

from pprint import pprint
import os
import importlib

#users = ["hannes", "martin"]
import flask, flask_login


salt = "i_love_flask"
# Our mock database.
users = {}
class User(flask_login.UserMixin):
    pass


class Server(object):
    def __init__(self, wrapped_class, port, verbosity_level = 0, initial_user = "default_user", initial_password = "default_password"):
        self.wrapped_class = wrapped_class
        self.port = port

        self.app = Flask(__name__)
        self.verbosity_level = verbosity_level
        if self.verbosity_level<1:print("verbosity:",verbosity_level)
        
        #auth
        self.app.secret_key = 'super secret string'  # Change this!
        self.login_manager = flask_login.LoginManager()
        self.login_manager.init_app(self.app)
        
        users[initial_user] = {"password": initial_password}
        if self.verbosity_level<1:
            print("found the following users")
            print(users)


        @self.login_manager.user_loader
        def user_loader(username):
            if username not in users:
                return
        
            user = User()
            user.id = username
            return user
        
        
        @self.login_manager.request_loader
        def request_loader(request):
            username = request.form.get('username')
            if username not in users:
                return
        
            user = User()
            user.id = username
        
            # DO NOT ever store passwords in plaintext and always compare password
            # hashes using constant-time comparison!
            user.is_authenticated = request.form['password'] == users[username]['password']
        
            return user
        
        @self.app.route('/login', methods=['GET', 'POST'])
        def login():
            if self.verbosity_level<1:
                print("getting login request:")
                print(flask.request)
            if flask.request.method == 'GET':
                return '''
                       <form action='login' method='POST'>
                        <input type='text' name='email' id='email' placeholder='email'/>
                        <input type='password' name='password' id='password' placeholder='password'/>
                        <input type='submit' name='submit'/>
                       </form>
                       '''
        
            email = flask.request.form['username']
            
            if self.verbosity_level<1:
                print("a user tries to login:")
                print(email)
                print("the following users are allowed:")
                print(users)
            #stored_password_hash = binascii.hexlify( hashlib.pbkdf2_hmac('sha256',str.encode(users[initial_user]["password"]) , str.encode(salt), 100000))

            provided_password_hash = flask.request.form['password']
            stored_password_hash = users[initial_user]["password"]
            
            if self.verbosity_level<1:
                print("comparing passwords:")
                print("provided pw:",provided_password_hash)
                print("stored pw  :",stored_password_hash)
                print(stored_password_hash == provided_password_hash)
            if  stored_password_hash == provided_password_hash:
                user = User()
                user.id = email
                flask_login.login_user(user)
                return flask.redirect(flask.url_for('protected'))
        
            return 'Bad login'
        
        
        @self.app.route('/protected')
        @flask_login.login_required
        def protected():
            return 'Logged in as: ' + flask_login.current_user.id 


        @self.app.route('/logout')
        def logout():
            flask_login.logout_user()
            return 'Logged out'

        @self.login_manager.unauthorized_handler
        def unauthorized_handler():
            return 'Unauthorized'
        
        @flask_login.login_required
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
            except Exception as err:
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

            pickled_return_values = dill.dumps(return_values, protocol = PICKLE_PROTOCOL)
            return pickled_return_values
        
        @flask_login.login_required
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
                
                    
            except Exception as err:
                print("exception")
                exc_info = sys.exc_info()
                print(type(err))
                print(isinstance(err, Exception))
                print(exc_info)
                return_values = err
                return_values = DummyException()
                exc_info = sys.exc_info()
                traceback.print_exception(*exc_info)



            pickled_return_values = dill.dumps(return_values, protocol = PICKLE_PROTOCOL)
            return pickled_return_values
        
        @flask_login.login_required
        def setattr_handler_function():

            new_data = dill.loads(request.data)
            
            attr = new_data["attr"]
            
            value = new_data["value"]
            if verbosity_level<1:
                print("setting attr",[attr],[value])
            setattr(self.wrapped_class,attr,value)
            
            return "None"
        
        @flask_login.login_required
        def meta_handler_function():
            command = request.data
            
            if self.verbosity_level < 1:print(command)
            command = command.decode("utf-8")
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

                    base64_encoded_dilled_function = command.split("_")[1]
                    if self.verbosity_level < 1:
                        print(command)
                        print(type(base64_encoded_dilled_function))
                    
                    self.ID = base64_encoded_dilled_function[:10]
                    
                    if isinstance(base64_encoded_dilled_function,str):
                        if self.verbosity_level < 1:print("encoding as bytes")
                        base64_encoded_dilled_function = str.encode(base64_encoded_dilled_function)
                    #for py3 this needed to be bytes
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
                        #for py3 this needs to be bytes
                        f.write(str.encode(function_signature+"\n"))
                        for code_line in code_lines[1:]:
                            stripped_code_line = code_line.lstrip()
                            code_line = code_line[min(leading_spaces, len(code_line)-len(stripped_code_line)):]
                            #for py3 this needs to be bytes
                            f.write(str.encode(code_line+"\n"))
                    if self.verbosity_level < 1:
                        print(module_name)
                        print("i am here",os.getcwd())
                        
                    sys.path.append(os.getcwd())
                    if self.verbosity_level < 1:
                        print("current path is:")
                        pprint( sys.path)
                    
                    sys.path.append("/tmp/")
                    module = importlib.import_module(module_name)
                    function_arguments = [free_var[1] for free_var in undilled_function[1]]
                    wrapped_object = module.marshalled_function(*function_arguments)
    
                    self.wrapped_class = wrapped_object

                    
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
        print("shutting down the server, press ENTER")
        #sys.exit(0)
        #self.app.shutdown()
    
    def __del__(self):
        self.stop()
        

