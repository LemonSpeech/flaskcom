# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 11:47:19 2019

@author: twiefel
"""
from __future__ import print_function
import os
import subprocess
#import dill
import pickle as dill
PICKLE_PROTOCOL = 2

import base64
import inspect
import time
import binascii
import hashlib
import sys
import traceback
class Marshaller(object):
    def __init__(self, verbosity_level,user,password,session,server,port):
        self.verbosity_level = verbosity_level
        self.user = user
        self.password = password
        self.session = session
        self.server=server
        
        self.port = port
        self.salt = "i_love_flask"
    
    def authenticate(self):
        r= None
        
        if self.verbosity_level<1:print("authenticating")
        authenticated = False
        url = "http://"+self.server+":"+str(self.port)+"/"+"login"
        if self.verbosity_level<1:print("url:",url)
        try:
            
            login_data = {"username":self.user,"password": binascii.hexlify( hashlib.pbkdf2_hmac('sha256',str.encode(self.password) , str.encode(self.salt), 100000)) }
            r = self.session.post(url, data=login_data)
            if self.verbosity_level<1:print(r)
            if self.verbosity_level<1:print(r.content)
            authenticated = True
        except Exception as err:
            if self.verbosity_level<1:
                print ("connection was refused when authenticating, maybe server is not running")
    
                print (err)
                #print(err)
                #exc_info = sys.exc_info()
                #traceback.print_exception(*exc_info)
                print("not authenticated")
        
        if self.verbosity_level<1:print ("authenticated:",authenticated)
        return authenticated
    def get_source_command(self, source_commands):
        source_command = []
        for line in source_commands.splitlines():
            line=line.strip()
            if line != "":
                source_command.append(line)
        if len(source_command) == 0:
            return ""
        source_command = ";".join(source_command)+";"
        if self.verbosity_level<1: print(source_command)
    
        return source_command
    
    def get_virtualenv_command(self, path_to_virtualenv, server_adress):
        if path_to_virtualenv != "":
            path_to_virtualenv_absolute = os.path.abspath(path_to_virtualenv)
            path_to_virtualenv_absolute = path_to_virtualenv_absolute+"/bin/activate"
            #print(path_to_virtualenv_absolute)
            # If we have a remote adress given as localhost, we look locally for the folder
            if not self.__check_remote_for_file(abs_file_path=path_to_virtualenv_absolute, server_adress=server_adress):

                print("virtualenv not found:")
                print(path_to_virtualenv_absolute)
                raise Exception
        virtualenv_source_command = ""
        if path_to_virtualenv != "":
            virtualenv_source_command = ". "+path_to_virtualenv_absolute+";"
        return virtualenv_source_command
        
    def get_cd_command(self, original_working_directory, server_adress):
        original_working_directory_absolute = os.path.abspath(original_working_directory)
        #print(original_working_directory_absolute)
        if not self.__check_remote_for_directory(abs_dir_path=original_working_directory_absolute, server_adress=server_adress):
            print("original_working_directory not found:")
            print(original_working_directory_absolute)
            raise Exception
    
        cd_command = "cd "+original_working_directory_absolute+";"
        return cd_command
    
    def get_shell_command(self, server):
        shell_command = "sh -c"
        if server != "localhost":
            shell_command = 'ssh -t -Y '+server
        return shell_command
    
    def get_geometry_command(self, object_id):
        x_width_rows = 47
        y_width_rows = 20
        x_width_pixels = 450
        y_width_pixels = 450
        
        obj_id = object_id % 8
        
        if obj_id < 4:
            x_pos = x_width_pixels*obj_id
            y_pos = 0
        elif obj_id >= 4:
            x_pos = x_width_pixels*(obj_id-4)
            y_pos = y_width_pixels
        else:
            print("not more than 4 terminals supported")
            raise Exception
        
        geometry_command = " --geometry="+str(x_width_rows)+"x"+str(y_width_rows)+"+"+str(x_pos)+"+"+str(y_pos)
        return geometry_command
    
    def get_python_command_for_wrapped_code(self, wrapped_code, server, port):
        python_command = []
        object_name = ""
        wrapped_module = ""
        wrapped_class = ""
        for line in wrapped_code.splitlines():
            line=line.strip()
            if line != '':
                
                #print([line])
                
                line = line.replace('"',r'\"')
                line = line.replace("'",r'\"')
    
                #print([line])
                if "=" in line:
                    object_name = line.split("=")[0].strip()
                    python_command.append('import sys')
                    python_command.append(r'sys.stdout.write(\"\x1b]2;'+object_name+' @ '+server+r'\x07\")')
                if line.startswith("from"):
                    wrapped_module = line.split("from ")[1].split(" import ")[0]
                    wrapped_class = line.split("from ")[1].split(" import ")[1]
                python_command.append(line)
        if object_name == "":
            print("no object instantiated in your code")
            print("the code needs to contain an object instantiation like:")
            print(" test_object = ComplexTestClass('hallo')")
            raise Exception
        python_command.append('from flaskcom.server import ServerWrapper')
        python_command.append("s = ServerWrapper("+object_name+","+str(port)+")")   
        python_command.append('s.ServerWrapper_start()')        
        python_command = ";".join(python_command)
        python_command = '"'+python_command+'"'
        command = "python -c "+python_command
        #print([command])
        return command,wrapped_module,wrapped_class
    
    
    def init_server_with_wrapped_function_raw(self, wrapped_function, meta_function):
        import inspect
        string_code = inspect.getsource(wrapped_function.__code__)
        free_vars = []
        if hasattr(wrapped_function.__code__, "co_freevars") and len(wrapped_function.__code__.co_freevars)>0:
            if self.verbosity_level<1: 
                print("found free vars:")
                print(wrapped_function.__code__.co_freevars)
            for free_var,closure_val in zip(wrapped_function.__code__.co_freevars,wrapped_function.__closure__):
                #import numpy as np                        
                if self.verbosity_level<1: 
                    print(free_var,"=", closure_val.cell_contents)
                free_vars.append((free_var,closure_val.cell_contents))
            if self.verbosity_level<1: 
                print(     )
        function_raw = (string_code,tuple(free_vars))

        dilled_function = dill.dumps(function_raw, protocol = PICKLE_PROTOCOL)
        base64_encoded_dilled_function = base64.encodestring(dilled_function)
                    
        status = meta_function("status")

        if self.verbosity_level<1: print("STATUS",status)
        if status == "INITIALIZING":
            if self.verbosity_level<1: 
                print("initializing function")
                print(type(base64_encoded_dilled_function))
                print(base64_encoded_dilled_function[:10],"...")
                
                print(function_raw)
                #print("function hash",hash(function_raw))
                print("dilled function hash",hash(dilled_function))
                print("base64 dilled function hash", hash(base64_encoded_dilled_function))
        
                base64_decoded_dilled_function = base64.decodestring(base64_encoded_dilled_function)
                undilled_function = dill.loads(base64_decoded_dilled_function)
                print("base64_decoded_dilled_function hash", hash(base64_encoded_dilled_function))
                #print("undilled_function hash",hash(undilled_function))
                print(undilled_function)
        

                print()
                print("function:")
                print( function_raw[0]           )
                print( undilled_function[0]        )
                #print(wrapped_function.__dict__)
                print("code equal?",  function_raw[0] == undilled_function[0]  )
                #print(wrapped_function.__code__.co_code)
                print("function code hash",hash(function_raw[0]))
                print("undilled_function code hash",hash(undilled_function[0]))
            status = meta_function("initstringcode_"+base64_encoded_dilled_function.decode("utf-8"))
            
            if self.verbosity_level<1: print("status:", status)
            
    def get_python_command_for_server(self, wrapped_function, server, port, flaskcom_path):

        lines = inspect.getsource(wrapped_function).splitlines()
        for line in lines[1:]:
            line = line.strip()
            if line.startswith("return "):
                name = line.split()[1]

        py_command = r'python -c "import sys;sys.path.append(\"'+flaskcom_path+r'\");from flaskcom import function_decoder;function_decoder.start()"'

        export_command = []
        export_command.append("export FLASKCOM_PORT="+str(port))
        export_command.append("export FLASKCOM_SERVER="+server)
        export_command.append("export FLASKCOM_TERMINAL_NAME="+name)
        export_command = ";".join(export_command)
        command  = export_command+";"+py_command
    
        return command

    
    def get_python_command_for_server_in_file(self, wrapped_function, server, port, flaskcom_path, original_working_directory, path_to_virtualenv, initial_user, initial_password):
        import inspect
        lines = inspect.getsource(wrapped_function).splitlines()
        for line in lines[1:]:
            line = line.strip()
            if line.startswith("return "):
                name = line.split()[1]

        export_command = []

        verified_flaskcom_path = ""
        if self.verbosity_level<1:
            print("trying to find flaskcom on the remote server")
            print("searching in flaskcom path: ",flaskcom_path)
        if flaskcom_path=="":
            print("flaskcom path was not specified")
        elif not self.__check_remote_for_directory(flaskcom_path, server):
            print("flaskcom path does not exist")
            print("please check if the flaskcom path is correct")
            raise Exception
        elif self.__check_remote_for_file(flaskcom_path+"/flaskcom/remote_object.py", server):
            
            verified_flaskcom_path = os.path.abspath(flaskcom_path+"/flaskcom/")
            if self.verbosity_level<1:print("flaskcom found at", verified_flaskcom_path)
        elif self.__check_remote_for_file(flaskcom_path+"/remote_object.py", server):
            verified_flaskcom_path = os.path.abspath(flaskcom_path)
            if self.verbosity_level<1:print("flaskcom found at", verified_flaskcom_path)
        else:
            if self.verbosity_level<1:
                print("flaskcom not found in flaskcom path")
            # raise Exception
        if verified_flaskcom_path == "":
            if self.verbosity_level<1: print("searching in working directory: ",original_working_directory)
            if original_working_directory=="":
                print("working directory path was not specified")
            elif not self.__check_remote_for_directory(original_working_directory, server):
                print("working directory does not exist")
                print("please check if the working directory is correct")
                raise Exception
            elif self.__check_remote_for_directory(original_working_directory+"/flaskcom/remote_object.py", server):
                verified_flaskcom_path = os.path.abspath(flaskcom_path+"/flaskcom/")
                print("flaskcom found at", verified_flaskcom_path)
            elif self.__check_remote_for_file(original_working_directory+"/remote_object.py", server):
                verified_flaskcom_path = os.path.abspath(flaskcom_path)
                print("flaskcom found at", verified_flaskcom_path)
            else:
                print("flaskcom not found in working directory")
    
                # raise Exception

        py_command = "python -m flaskcom.start_server"

        export_command.append("export FLASKCOM_PORT="+str(port))
        export_command.append("export FLASKCOM_SERVER="+server)
        export_command.append("export FLASKCOM_TERMINAL_NAME="+name)
        export_command.append("export FLASKCOM_INITIAL_USER="+initial_user)
        password = binascii.hexlify( hashlib.pbkdf2_hmac('sha256',str.encode(initial_password), str.encode(self.salt), 100000))
        export_command.append("export FLASKCOM_INITIAL_PASSWORD="+ password.decode("utf-8"))
        export_command.append("export FLASKCOM_VERBOSITY="+str(self.verbosity_level))

        
        
        export_command = ";".join(export_command)
        command  = export_command+";"+py_command
    
        return command
        
        import inspect
        lines = inspect.getsource(wrapped_function).splitlines()
    
        for line in lines[1:]:
            line = line.strip()
            if line == '':
                continue
            if line.startswith("return "):
                name = line.split()[1]
                continue
            if self.verbosity_level<1: print([line])
            #exec(line)
        if self.verbosity_level<1:print(name)
        if self.verbosity_level<1:print(lines)
    
        return command
        
    def get_debug_command(self, debug): 
        debug_command = ""
        if debug:
            debug_command = ";$SHELL"    
        return debug_command
        
    def start_server_terminal(self, command, meta_function, time_out):

        if self.verbosity_level<1:
            print("running:")
            print(command)
            print("checking if remote object is already running:")
        counter = 0
        def check_status(counter):
            if self.verbosity_level<1: print("checking status")
            isup = False
            status = meta_function("status")
            if self.verbosity_level<1: print("STATUS",status)
            if status != "down":
                isup = True

            if isup:
                if self.verbosity_level<1:
                    print
                    print("remote object is already running, will not create a new one")
                return isup
            if counter == 0:
                if self.verbosity_level<1: print("not running yet",)
                counter+=1
            else:
                if self.verbosity_level<1: print(".",)
            time.sleep(1)
            return isup
        terminal = subprocess.Popen(command, stdin=subprocess.PIPE, shell=True)
        if time_out != -1:
            if self.verbosity_level<1:print("will try", time_out, "times to connect to the remote object")
            for _ in range(time_out):
                if check_status(counter):
                    return
        else:
            if self.verbosity_level<1:print("will try to connect to the remote object for unlimited time. if this takes too long, kill this process manually.")
            while True:
                if check_status(counter):
                    return
        if self.verbosity_level<1:print("raising....")
        raise Exception
     
    
    def __check_remote_for_file(self, abs_file_path, server_adress):
        """
        Checks if the file is accessible on the remote-server.
        """
        if server_adress == 'localhost':
            return os.path.exists(abs_file_path)
        else:
            command_str = "if [ -f {} ]; then echo True; else echo False; fi".format(abs_file_path)
            responses = subprocess.check_output(['ssh',
                                                 server_adress,
                                                 command_str],
                                                universal_newlines=True,)
            response = responses.splitlines()[-1]
            return "True" == response.strip()
    
    
    def __check_remote_for_directory(self, abs_dir_path, server_adress):
        """
        Checks if the directory is accessible from the remote server.
        """
        if server_adress == 'localhost':
            return os.path.exists(abs_dir_path)
        else:
            command_str = "if [ -d {} ]; then echo True; else echo False; fi".format(abs_dir_path)
            responses = subprocess.check_output(['ssh',
                                                 server_adress,
                                                 command_str],
                                                universal_newlines=True,)
            response = responses.splitlines()[-1]
            return "True" == response.strip()
