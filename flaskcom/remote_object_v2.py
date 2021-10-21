# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 14:36:42 2018

@author: twiefel
"""
import requests
import json
import dill
from .dummy_callable import DummyCallable
from .dummy_exception import DummyException
import os
import sys
import subprocess

def get_methods_without_import(wrapped_module, wrapped_class):
    import pkgutil
    package = pkgutil.get_loader(wrapped_module)
    #print package.filename
    import ast

    def show_info(functionNode):
        print("Function name:", functionNode.name)
        print("Args:")
        for arg in functionNode.args.args:
            #print arg
            #import pdb; pdb.set_trace()
            #print("\tParameter name:", arg)
            #print ast.dump(arg)
            print arg.id
    
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

current_object_id = 0
default_port = 55000
class RemoteObject(object):
    def __init__(self, port = -1, path_to_virtualenv = "", original_working_directory = ".", flaskcom_path = "../", server = "localhost", wrapped_code = "", wrapped_function = None, complex_datatypes = True, keep_open = False, time_out = 20, debug = False, start_server = True):
        self.ClientWrapper_complex_datatypes = complex_datatypes
        self.ClientWrapper_server = server
        self.ClientWrapper_port = port
        self.ClientWrapper_keep_open = keep_open
        self.ClientWrapper_debug = debug
        self.ClientWrapper_time_out = time_out
        self.ClientWrapper_flaskcom_path = flaskcom_path
        if wrapped_code == "" and wrapped_function == None:
            print "define either wrapped_code or wrapped_function"
            raise NotImplementedError
        if wrapped_code != "" and wrapped_function != None:
            print "define either wrapped_code or wrapped_function, not both!"
            raise NotImplementedError
        if wrapped_code != "":
            self.ClientWrapper_mode = "STRING_MODE"
        if wrapped_function != None:
            self.ClientWrapper_mode = "FUNCTION_MODE"

        global current_object_id
        print "Creating Remote Object with ID",current_object_id


        self.ClientWrapper_object_id = current_object_id
        current_object_id += 1
        
        if self.ClientWrapper_port == -1:
            self.ClientWrapper_port = default_port+self.ClientWrapper_object_id
        #self.ClientWrapper_wrapped_module = wrapped_module
        #self.ClientWrapper_wrapped_class = wrapped_class 
        

                
        #return
        
        
#        for line in wrapped_code.splitlines():
#            line=line.strip()
#            if line.startswith("from"):
#                self.ClientWrapper_wrapped_module = line.split("from ")[1].split(" import ")[0]
#                self.ClientWrapper_wrapped_class = line.split("from ")[1].split(" import ")[1]

        
        if start_server:
            isup = self.ClientWrapper_meta_function("isup") == "True"
            print "server was running",isup
            if not isup:

                #self.ClientWrapper_init_server(path_to_virtualenv = path_to_virtualenv, original_working_directory = original_working_directory, server = server, wrapped_code = wrapped_code, time_out = time_out)
                virtualenv_source_command = self.ClientWrapper_get_virtualenv_command(path_to_virtualenv)
                cd_command = self.ClientWrapper_get_cd_command(original_working_directory)
                shell_command = self.ClientWrapper_get_shell_command(server)
                #geometry_command = self.ClientWrapper_get_geometry_command()
                geometry_command = ""
                if wrapped_code != "":
                    python_command = self.ClientWrapper_get_python_command_for_wrapped_code(wrapped_code,server)
                if wrapped_function != None:
                    python_command = self.ClientWrapper_get_python_command_for_server(wrapped_function,server)
                    #env = None
                debug_command = self.ClientWrapper_get_debug_command()
                #command = ['gnome-terminal'+geometry_command+ ' -x '+shell_command+' " '+virtualenv_source_command+cd_command+python_command+debug_command+'" ' ]
                
                inside_shell_command = virtualenv_source_command + cd_command+python_command+debug_command
                #python_command = "export FLASKCOM_SERVER=bla;echo $FLASKCOM_SERVER"
                inside_shell_command = virtualenv_source_command + cd_command+python_command+debug_command
                print type(r"hallo")
                print [r"sad'asd"]
                command = ["gnome-terminal"+geometry_command+ " -x "+shell_command+" ' "+inside_shell_command+"' " ]
                print command
                print "running in"
                print cd_command
                self.ClientWrapper_start_server(command)
                if wrapped_function != None:
                    self.ClientWrapper_init_server_with_wrapped_function(wrapped_function)

        #attrs = vars(self.ClientWrapper_wrapped_class)
        #print dir(self.ClientWrapper_wrapped_class)
        #print attrs
        #print self.ClientWrapper_wrapped_class.__dict__.items()
        #from types import FunctionType
        
        #def methods(cls):
        #    return [x for x, y in cls.__dict__.items() if type(y) == FunctionType]
        #self.ClientWrapper_methods = methods(self.ClientWrapper_wrapped_class)
        #self.ClientWrapper_methods = get_methods_without_import(self.ClientWrapper_wrapped_module, self.ClientWrapper_wrapped_class)


    def __del__(self):
        if self.ClientWrapper_keep_open:
            print "keeping terminal open"
        else:
            self.ClientWrapper_meta_function("shutdown")
    
    def ClientWrapper_get_virtualenv_command(self,path_to_virtualenv):
        if path_to_virtualenv != "":
            path_to_virtualenv_absolute = os.path.abspath(path_to_virtualenv)
            path_to_virtualenv_absolute = path_to_virtualenv_absolute+"/bin/activate"
            #print path_to_virtualenv_absolute
            if not os.path.exists(path_to_virtualenv_absolute):
                print "virtualenv not found:"
                print path_to_virtualenv_absolute
                raise Exception
        virtualenv_source_command = ""
        if path_to_virtualenv != "":
            virtualenv_source_command = ". "+path_to_virtualenv_absolute+";"
        return virtualenv_source_command
        
    def ClientWrapper_get_cd_command(self,original_working_directory):
        original_working_directory_absolute = os.path.abspath(original_working_directory)
        #print original_working_directory_absolute
        if not os.path.exists(original_working_directory_absolute):
            print "original_working_directory not found:"
            print original_working_directory_absolute
            raise Exception
        cd_command = "cd "+original_working_directory_absolute+";"
        return cd_command
    
    def ClientWrapper_get_shell_command(self,server):
        shell_command = "sh -c"
        if server != "localhost":
            shell_command = 'ssh -t -Y '+server
        return shell_command
    
    def ClientWrapper_get_geometry_command(self):
        x_width_rows = 47
        y_width_rows = 20
        x_width_pixels = 450
        y_width_pixels = 450
        
        obj_id = self.ClientWrapper_object_id % 8
        
        if obj_id < 4:
            x_pos = x_width_pixels*obj_id
            y_pos = 0
        elif obj_id >= 4:
            x_pos = x_width_pixels*(obj_id-4)
            y_pos = y_width_pixels
        else:
            print "not more than 4 terminals supported"
            raise Exception
        
        geometry_command = " --geometry="+str(x_width_rows)+"x"+str(y_width_rows)+"+"+str(x_pos)+"+"+str(y_pos)
        return geometry_command
    
    def ClientWrapper_get_python_command_for_wrapped_code(self, wrapped_code, server):
        python_command = []
        object_name = ""
        for line in wrapped_code.splitlines():
            line=line.strip()
            if line != '':
                print [line]
                
                line = line.replace('"',r'\"')
                line = line.replace("'",r'\"')
    
                print [line]
                if "=" in line:
                    object_name = line.split("=")[0].strip()
                    python_command.append('import sys')
                    python_command.append(r'sys.stdout.write(\"\x1b]2;'+object_name+' @ '+server+r'\x07\")')
                if line.startswith("from"):
                    self.ClientWrapper_wrapped_module = line.split("from ")[1].split(" import ")[0]
                    self.ClientWrapper_wrapped_class = line.split("from ")[1].split(" import ")[1]
                python_command.append(line)
        if object_name == "":
            print "no object instatiated in your code"
            print "the code needs to contain an object instantiation like:"
            print " test_object = ComplexTestClass('hallo')"
            raise Exception
        python_command.append('from flaskcom.server import ServerWrapper')
        python_command.append("s = ServerWrapper("+object_name+","+str(self.ClientWrapper_port)+",complex_datatypes = "+str(self.ClientWrapper_complex_datatypes)+")")   
        python_command.append('s.ServerWrapper_start()')        
        python_command = ";".join(python_command)
        python_command = '"'+python_command+'"'
        command = "python -c "+python_command
        print [command]
        return command

    def ClientWrapper_init_server_with_wrapped_function(self, wrapped_function):
        import dill
        dilled_function = dill.dumps(wrapped_function)
        import base64
        #print dilled_function
        base64_encoded_dilled_function = base64.encodestring(dilled_function)

                
        status = self.ClientWrapper_meta_function("status")
        print "STATUS",status
        if status == "INITIALIZING":
            print "initializing function"
            print type(base64_encoded_dilled_function)
            print base64_encoded_dilled_function[:10],"..."
            
            print wrapped_function
            print "function hash",hash(wrapped_function)
            print "dilled function hash",hash(dilled_function)
            print "base64 dilled function hash", hash(base64_encoded_dilled_function)

            base64_decoded_dilled_function = base64.decodestring(base64_encoded_dilled_function)
            undilled_function = dill.loads(base64_decoded_dilled_function)
            print "base64_decoded_dilled_function hash", hash(base64_encoded_dilled_function)
            print "undilled_function hash",hash(undilled_function)
            print undilled_function

            import inspect
            print 
            print "function:"
            print  inspect.getsource(wrapped_function.__code__)            
            print  inspect.getsource(undilled_function.__code__)     
            #print wrapped_function.__dict__
            print "code equal?",  wrapped_function.__code__.co_code == undilled_function.__code__.co_code
            #print wrapped_function.__code__.co_code
            print "function code hash",hash(wrapped_function.__code__.co_code)
            print "undilled_function code hash",hash(undilled_function.__code__.co_code)
            status = self.ClientWrapper_meta_function("init_"+base64_encoded_dilled_function)
            print status
            
    def ClientWrapper_get_python_command_for_server(self, wrapped_function, server):
        import inspect
        lines = inspect.getsource(wrapped_function).splitlines()
        for line in lines[1:]:
            line = line.strip()
            if line.startswith("return "):
                name = line.split()[1]
        

                #continue
            #print [line]
        #flaskcom_env["FLASKCOM_TERMINAL_NAME"] = name
        #py_command = "python -c 'import sys;sys.path.append(\\\""+self.ClientWrapper_flaskcom_path+"\\\");from flaskcom import function_decoder;function_decoder.start()'"
        print 
        py_command = r'python -c "import sys;sys.path.append(\"'+self.ClientWrapper_flaskcom_path+r'\");from flaskcom import function_decoder;function_decoder.start()"'
        #print [base64_encoded_dilled_function]
        export_command = []
        #export_command.append("export FLASKCOM_WRAPPED_FUNCTION="+base64_encoded_dilled_function)
        export_command.append("export FLASKCOM_PORT="+str(self.ClientWrapper_port))
        export_command.append("export FLASKCOM_SERVER="+server)
        export_command.append("export FLASKCOM_TERMINAL_NAME="+name)
        export_command = ";".join(export_command)
        command  = export_command+";"+py_command

        return command
#        
#        import subprocess, os
#        my_env = os.environ.copy()
#
#        import subprocess
#        subprocess.Popen(whole_command, stdin=subprocess.PIPE, shell=True,env = my_env)
#        #base64_decoded_dilled_function = base64.decodestring(base64_encoded_dilled_function)
#        #print base64_decoded_dilled_function
#        #undilled_function = dill.loads(base64_decoded_dilled_function)
#        #print undilled_function
#        #undilled_function()        
#        
#        wrapped_code = wrapped_function.__code__
#        if hasattr(wrapped_code, "co_freevars"):
#            print "found free vars"
#            print vars()
#            wrapped_function()
#            for var in wrapped_code.co_freevars:
#                print var
#                vars()[var] = var
#            print dir(wrapped_code)
#            print 
#            print "A",wrapped_code.co_freevars
#            print "A",wrapped_code.co_varnames
#            print vars()
#            print locals()
#            def surrounding_func():
#                return wrapped_function
#            print "PICKLING"
#            print wrapped_code
#            import inspect
#            print inspect.getsource(surrounding_func)
#            import dill
#            dilled_function = dill.dumps(wrapped_function)
#            import base64
#            print dilled_function
#            base64_encoded_dilled_function = base64.encodestring(dilled_function)
#            print base64_encoded_dilled_function
#            base64_decoded_dilled_function = base64.decodestring(base64_encoded_dilled_function)
#            print base64_decoded_dilled_function
#            undilled_function = dill.loads(base64_decoded_dilled_function)
#            print undilled_function
#            undilled_function()
#            
#            print "ENCODING TERMINAL"
#            #python_code = []
#            #python_code.append("import dill")
#            #python_code.append("import base64")
#            #python_code.append('base64_encoded_dilled_function = "'+base64_encoded_dilled_function+'"')
#            #python_code.append("base64.decodestring(base64_encoded_dilled_function)")
#            #python_code.append("undilled_function = dill.loads(base64_decoded_dilled_function)")
#            #python_code.append("undilled_function()")
#            #python_code = ";".join(python_code)
#            #pycommand = "python -c '{}'"
#            #print pycommand
#            whole_command = "python -c '\"'\"'from flaskcom import function_decoder'"
#            import subprocess, os
#            my_env = os.environ.copy()
#            my_env["FLASKCOM_WRAPPED_FUNCTION"] = base64_encoded_dilled_function
#            import subprocess
#            subprocess.Popen(whole_command, stdin=subprocess.PIPE, shell=True,env = my_env)
#            
#            #result = dill.loads(r.content)
#            #dill.loads(r.content)
#            #exec(wrapped_code)
#            
#            
        
        import inspect
        lines = inspect.getsource(wrapped_function).splitlines()
    
        for line in lines[1:]:
            line = line.strip()
            if line == '':
                continue
            if line.startswith("return "):
                name = line.split()[1]
                continue
            print [line]
            #exec(line)
        print name
            
            
        print(lines)

        return command
        
    def ClientWrapper_get_debug_command(self): 
        debug_command = ""
        if self.ClientWrapper_debug:
            debug_command = ";$SHELL"    
        return debug_command
        
    def ClientWrapper_start_server(self,command):
        import time
        print "running:"
        print command
        print "checking if remote object is already running:"
        counter = 0
        def check_status(counter):
            isup = False
            if self.ClientWrapper_mode == "STRING_MODE":
                isup = self.ClientWrapper_meta_function("isup") == "True"
            if self.ClientWrapper_mode == "FUNCTION_MODE":
                status = self.ClientWrapper_meta_function("status")
                print "STATUS",status
                if status != "False":
                    isup = True
                
                
            if isup:
                print
                print "remote object is already running, will not create a new one"
                return isup
            if counter == 0:
                print "not running yet",
                counter+=1
            else:
                print ".",
            time.sleep(1)
            return isup
        terminal = subprocess.Popen(command, stdin=subprocess.PIPE, shell=True)
        if self.ClientWrapper_time_out != -1:
            print "will try", self.ClientWrapper_time_out, "times to connect to the remote object"
            for _ in range(self.ClientWrapper_time_out):
                if check_status(counter):
                    return
        else:
            print "will try to connect to the remote object for unlimited time. if this takes too long, kill this process manually."
            while True:
                if check_status(counter):
                    return
        print "raising...."
        raise Exception
            
#    def ClientWrapper_init_server(self, path_to_virtualenv = "", original_working_directory = ".", server = "localhost", wrapped_code = "", time_out = 20):
#        import subprocess
#        import os
#        if self.ClientWrapper_port == -1:
#            self.ClientWrapper_port = default_port+self.ClientWrapper_object_id
#        python_command = []
#        object_name = ""
#        for line in wrapped_code.splitlines():
#            line=line.strip()
#            if line != '':
#                print [line]
#                
#                line = line.replace('"','\\"')
#                line = line.replace("'",'\\"')
#    
#                print [line]
#                if "=" in line:
#                    object_name = line.split("=")[0].strip()
#                    python_command.append('import sys')
#                    python_command.append('sys.stdout.write(\\"\x1b]2;'+object_name+' @ '+server+'\x07\\")')
#                if line.startswith("from"):
#                    self.ClientWrapper_wrapped_module = line.split("from ")[1].split(" import ")[0]
#                    self.ClientWrapper_wrapped_class = line.split("from ")[1].split(" import ")[1]
#                python_command.append(line)
#        if object_name == "":
#            print "no object instatiated in your code"
#            print "the code needs to contain an object instantiation like:"
#            print " test_object = ComplexTestClass('hallo')"
#            raise Exception
#        python_command.append('from flaskcom.server import ServerWrapper')
#        python_command.append("s = ServerWrapper("+object_name+","+str(self.ClientWrapper_port)+",complex_datatypes = "+str(self.ClientWrapper_complex_datatypes)+")")   
#        python_command.append('s.ServerWrapper_start()')        
#        python_command = ";".join(python_command)
#        python_command = "'"+python_command+"'"
#        command = "python -c "+python_command
#        print [command]
#        #raise Exception
#        
#        
#        
#        #command = "gnome-terminal -x python example_server.py"
#        #terminal = subprocess.Popen(command.split(), stdin=subprocess.PIPE) 
#        #terminal = subprocess.Popen(['gnome-terminal -x sh -c \"ssh -Y wtmgws9 \'cd sylviann/srl;source env_flaskcom/bin/activate;cd flaskcom;python example_server.py\'\"' ], stdin=subprocess.PIPE, shell=True)
#        #os.system("gnome-terminal -x sh -c \"ssh -Y wtmgws9 'cd sylviann/srl;source env_flaskcom/bin/activate;cd flaskcom;python example_server.py;$SHELL'\"")
#        #terminal = subprocess.Popen(['xterm'], shell= True, stdin=subprocess.PIPE)
#        if path_to_virtualenv != "":
#            path_to_virtualenv_absolute = os.path.abspath(path_to_virtualenv)
#            path_to_virtualenv_absolute = path_to_virtualenv_absolute+"/bin/activate"
#            #print path_to_virtualenv_absolute
#            if not os.path.exists(path_to_virtualenv_absolute):
#                print "virtualenv not found:"
#                print path_to_virtualenv_absolute
#                raise Exception
#        
#        original_working_directory_absolute = os.path.abspath(original_working_directory)
#        #print original_working_directory_absolute
#        if not os.path.exists(original_working_directory_absolute):
#            print "original_working_directory not found:"
#            print original_working_directory_absolute
#            raise Exception
#
#        isup = self.ClientWrapper_meta_function("isup") == "True"
#        print "server was running",isup
#        if not isup:
#            virtualenv_source_command = ""
#            if path_to_virtualenv != "":
#                virtualenv_source_command = ". "+path_to_virtualenv_absolute+";"
#            cd_command = "cd "+original_working_directory_absolute+";"
#            #py_command = "python example_server.py"
#            py_command = command
#            shell_command = "sh -c"
#            if server != "localhost":
#                shell_command = 'ssh -t -Y '+server
#                
#            x_width_rows = 47
#            y_width_rows = 20
#            x_width_pixels = 450
#            y_width_pixels = 450
#            
#            obj_id = self.ClientWrapper_object_id % 8
#            
#            if obj_id < 4:
#                x_pos = x_width_pixels*obj_id
#                y_pos = 0
#            elif obj_id >= 4:
#                x_pos = x_width_pixels*(obj_id-4)
#                y_pos = y_width_pixels
#            else:
#                print "not more than 4 terminals supported"
#                raise Exception
#            
#            geometry_command = " --geometry "+str(x_width_rows)+"x"+str(y_width_rows)+"+"+str(x_pos)+"+"+str(y_pos)
#            
#            #terminal_termination_command = "shopt | grep huponexit;shopt -s huponexit;shopt | grep huponexit;"
#            #terminal_termination_command = ""
#            #whole_command = ['gnome-terminal -x sh -c \"ssh -Y '+server+' \''+virtualenv_source_command+cd_command+py_command+';$SHELL'+'\'\"' ]
#            #whole_command = ['gnome-terminal -x ssh -Y '+server+' \"'+virtualenv_source_command+cd_command+py_command+';echo keeping shell open;$SHELL'+'\"' ]
#            
#            #whole_command = ['gnome-terminal -x ssh -Y '+server+' " ' +virtualenv_source_command+cd_command+py_command+';echo keeping shell open;$SHELL" ' ]
#            debug_command = ""
#            if self.ClientWrapper_debug:
#                debug_command = ";$SHELL"
#            #use this for debugging to keep the shell open...            
#            whole_command = ['gnome-terminal'+geometry_command+ ' -x '+shell_command+' " '+virtualenv_source_command+cd_command+py_command+debug_command+'" ' ]
#
#            #whole_command = ['gnome-terminal'+geometry_command+ ' -x '+shell_command+' "' +virtualenv_source_command+cd_command+py_command+'" ' ]
#
#            #subprocess.Popen('sh -c "'+py_command+'"', shell=True)
#            #subprocess.Popen(py_command, shell=True)
#            #return
#            import time
#            print "running:"
#            print whole_command
#            terminal = subprocess.Popen(whole_command, stdin=subprocess.PIPE, shell=True)
#            if time_out != -1:
#                print "will try", time_out, "times to connect to the remote object"
#                for _ in range(20):
#                    isup = self.ClientWrapper_meta_function("isup") == "True"
#                    print "checking if remote object is already running:",isup
#                    if isup:
#                        print "remote object is already running, will not create a new one"
#                        return
#                    time.sleep(1)
#            else:
#                print "will try to connect to the remote object for unlimited time. if this takes too long, kill this process manually."
#                while True:
#                    isup = self.ClientWrapper_meta_function("isup") == "True"
#                    print "checking if remote object is already running:",isup
#                    if isup:
#                        print "remote object is already running, will not create a new one"
#                        return
#                    time.sleep(1)
#            raise Exception
#        return        
            
    def ClientWrapper_meta_function(self, payload):
        print "calling ClientWrapper_meta_function",payload[:10],"..."
        try:
            r = requests.post("http://"+self.ClientWrapper_server+":"+str(self.ClientWrapper_port)+"/"+"__meta_function__", data=payload)
            print "CONTENT",r.content
            return r.content
        except:
            print "call",payload,"failed"
            if payload == "isup" or payload == "status":
                return "False"
            else:
                raise
        return "False"
    def __setattr__(self, name, value):
        #print "__setattr__",name,value
        #raw_input()
        if not name.startswith("ClientWrapper_"):
            #print "wrapped object attribute"
            payload = {'attr':name, 'value':value}
            #print payload
            if not self.ClientWrapper_complex_datatypes:
                data = json.dumps(payload)
                r = requests.post("http://"+self.ClientWrapper_server+":"+str(self.ClientWrapper_port)+"/"+"__setattr__", json=data)
            else:
                data = dill.dumps(payload)
                r = requests.post("http://"+self.ClientWrapper_server+":"+str(self.ClientWrapper_port)+"/"+"__setattr__", data=data)
        else:
            super(RemoteObject, self).__setattr__(name, value)


    def __getattr__(self,attr):
        if attr.startswith("ClientWrapper_"):
            print "requesting:",attr
            return super(RemoteObject, self).__getattr__(attr)
            
        payload = {'attr':attr}

        if not self.ClientWrapper_complex_datatypes:
            data = json.dumps(payload)
            r = requests.post("http://"+self.ClientWrapper_server+":"+str(self.ClientWrapper_port)+"/"+"__getattr__", json=data)
            result = r.json()["return_values"]
        else:
            data = dill.dumps(payload)
            r = requests.post("http://"+self.ClientWrapper_server+":"+str(self.ClientWrapper_port)+"/"+"__getattr__", data=data)
            result = dill.loads(r.content)
        
        #print "called __getattr__ with",attr,"received",result
        if isinstance(result, DummyException):
            print result.exception_info
            import sys
            sys.exit()

        
        if not callable(result):
            #print result,"is not callable"
            return result
        
        def hooked(*args, **kwargs):
            payload = {'attr':attr, 'args':args,"kwargs":kwargs}

            if not self.ClientWrapper_complex_datatypes:
                data = json.dumps(payload)
                r = requests.post("http://"+self.ClientWrapper_server+":"+str(self.ClientWrapper_port)+"/"+"__call__", json=data)
                result = r.json()["return_values"]
            else:
                data = dill.dumps(payload)
                r = requests.post("http://"+self.ClientWrapper_server+":"+str(self.ClientWrapper_port)+"/"+"__call__", data=data)
                result = dill.loads(r.content)

            # prevent wrapped_class from becoming unwrapped
            #if type(result) == type(self.ClientWrapper_wrapped_class) and result == self.ClientWrapper_wrapped_class:
            #    return self
            
            if isinstance(result, DummyException):
                print result.exception_info
                import sys
                sys.exit()

            return result

        return hooked


