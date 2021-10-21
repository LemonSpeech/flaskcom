#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 21 17:01:16 2021

@author: twiefel
"""

print("getting started")
print(__file__)
from shutil import copyfile,copy2
import os
example_folder = os.path.dirname(__file__)+"/../examples/"
print(example_folder)
file_example_remote_object =    "example_remote_object.py"
file_example_server =           "example_server.py"
file_example_client =           "example_client.py"
copy2(example_folder+file_example_remote_object, "./"+file_example_remote_object)
copy2(example_folder+file_example_server,        "./"+file_example_server)
copy2(example_folder+file_example_client,        "./"+file_example_client)
print("copied the following files to this directory:")
print("1: example how to use a remote object - example_remote_object.py")
print("use this as a baseline for a remote object that is started on a server")
print("2: example how to use a server - example_server.py")
print("this can be used as a baseline server that can be run continuously, for example in a tmux terminal")
print("3: example how to use a client - example_client.py")
print("the client uses the server as a remote object")
