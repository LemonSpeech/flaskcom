# -*- coding: utf-8 -*-
"""
Created on Wed Jan  9 15:09:23 2019

@author: twiefel
"""
from __future__ import print_function
print("function decoder imported")
def start():
    print("starting flaskcom server from decoder function")
    import os

    import sys

    print("Python Version")
    print(sys.version)

    #import flaskcom
    #from pprint import pprint
    #pprint(sys.modules)
    if not "FLASKCOM_SERVER" in os.environ.keys():
        print("no flaskcom server")
        raw_input()
        
    else:
        server = os.environ["FLASKCOM_SERVER"]
        terminal_name = os.environ["FLASKCOM_TERMINAL_NAME"]
        port = os.environ["FLASKCOM_PORT"]
        sys.stdout.write("\x1b]2;"+terminal_name+' @ '+server+"\x07")
#        
#        base64_encoded_dilled_function = os.environ["FLASKCOM_WRAPPED_FUNCTION"]
#        print(base64_encoded_dilled_function)
#        base64_decoded_dilled_function = base64.decodestring(base64_encoded_dilled_function)
#        #print(base64_decoded_dilled_function)
#        undilled_function = dill.loads(base64_decoded_dilled_function)
#        print(undilled_function)
#        wrapped_object = undilled_function()#
    
        initial_user = os.environ["FLASKCOM_INITIAL_USER"]
        initial_password = os.environ["FLASKCOM_INITIAL_PASSWORD"]
        verbosity_level = int(os.environ["FLASKCOM_VERBOSITY"])
        from .dummy_object import DummyObject
        wrapped_object = DummyObject()
        from .server import Server
        print("created object", wrapped_object)
        s = Server(wrapped_object, int(port), initial_user=initial_user,initial_password=initial_password, verbosity_level=verbosity_level)   
        print("created server",s)
        
        s.start()
        print("server stopped")
