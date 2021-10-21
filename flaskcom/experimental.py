# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 14:03:26 2018

@author: twiefel
"""
from __future__ import print_function


def get_object_from_wrapped_code(wrapped_code):
    from threading import Thread
    import subprocess
    import os
    #command = "gnome-terminal -x python example_server.py"
    #terminal = subprocess.Popen(command.split(), stdin=subprocess.PIPE) 
    terminal = subprocess.Popen(['gnome-terminal -x sh -c \"ssh -Y wtmgws9 \'cd sylviann/srl;source env_flaskcom/bin/activate;cd flaskcom;python example_server.py\'\"' ], stdin=subprocess.PIPE, shell=True)
    #os.system("gnome-terminal -x sh -c \"ssh -Y wtmgws9 'cd sylviann/srl;source env_flaskcom/bin/activate;cd flaskcom;python example_server.py;$SHELL'\"")
    #terminal = subprocess.Popen(['xterm'], shell= True, stdin=subprocess.PIPE)
    import time
    time.sleep(10)
    print("wait")

    terminal.communicate("echo Hello World\n") 
    return
    
    from subprocess import Popen, PIPE

    #terminal = Popen(['xterm', '-e', '/bin/bash'], stdin=PIPE) #Or cat > /dev/null
    #os.system("gnome-terminal -x sh -c \"ssh -Y wtmgws9 'cd sylviann/srl;source env_flaskcom/bin/activate;which python;$SHELL'\"")
    terminal = Popen(['gnome-terminal', '-x', 'sh' '-c',"ssh -Y wtmgws9 'cd sylviann/srl;source env_flaskcom/bin/activate;which python;$SHELL'" ], stdin=PIPE)
    
    #terminal.communicate("echo Hello World") 
    return    
    
    
    from subprocess import Popen, PIPE
    
    terminal = Popen(['xterm', '-e', 'cat'], stdin=PIPE) #Or cat > /dev/null
    terminal.stdin.write("Information".encode())    
    return
    import os
    from subprocess import Popen, PIPE
    import time
    
    PIPE_PATH = "/tmp/my_pipe"
    
    if not os.path.exists(PIPE_PATH):
        os.mkfifo(PIPE_PATH)
    
    Popen(['xterm', '-e', 'tail -f %s' % PIPE_PATH])
    
    
    for _ in range(5):
        with open(PIPE_PATH, "w") as p:
            p.write("echo Hello world!\n")
            time.sleep(1)    
    return
    
    
    
    python_command = []
    for line in wrapped_code.splitlines():
        line=line.strip()
        if line != '':
            python_command.append(line)
    python_command = "\n".join(python_command)
    python_command = "'"+python_command+"'"
    import subprocess
    commands = "python -c "+python_command
    print([commands])
    process = subprocess.Popen('xterm', stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = process.communicate(commands)
    print(out)

def get_command_from_wrapped_code(wrapped_code):
    python_command = []
    for line in wrapped_code.splitlines():
        line=line.strip()
        if line != '':
            python_command.append(line)
    python_command = "\n".join(python_command)
    python_command = "'"+python_command+"'"
    command = "python -c "+python_command
    return command
    
def start_server(path_to_virtualenv = "", original_working_directory = ".", server = "localhost", wrapped_code = ""):
    from threading import Thread
    import subprocess
    import os
    
    python_command = []
    for line in wrapped_code.splitlines():
        line=line.strip()
        if line != '':
            print([line])
            
            line = line.replace('"','\\"')
            line = line.replace("'",'\\"')

            print([line])
            python_command.append(line)
    python_command = ";".join(python_command)
    python_command = "'"+python_command+"'"
    command = "python -c "+python_command
    print([command])
    #raise Exception
    
    
    
    #command = "gnome-terminal -x python example_server.py"
    #terminal = subprocess.Popen(command.split(), stdin=subprocess.PIPE) 
    #terminal = subprocess.Popen(['gnome-terminal -x sh -c \"ssh -Y wtmgws9 \'cd sylviann/srl;source env_flaskcom/bin/activate;cd flaskcom;python example_server.py\'\"' ], stdin=subprocess.PIPE, shell=True)
    #os.system("gnome-terminal -x sh -c \"ssh -Y wtmgws9 'cd sylviann/srl;source env_flaskcom/bin/activate;cd flaskcom;python example_server.py;$SHELL'\"")
    #terminal = subprocess.Popen(['xterm'], shell= True, stdin=subprocess.PIPE)
    import time
    path_to_virtualenv_absolute = os.path.abspath(path_to_virtualenv)
    path_to_virtualenv_absolute = path_to_virtualenv_absolute+"/bin/activate"
    #print(path_to_virtualenv_absolute)
    if not os.path.exists(path_to_virtualenv_absolute):
        print("virtualenv not found:")
        print(path_to_virtualenv_absolute)
        raise Exception
    
    original_working_directory_absolute = os.path.abspath(original_working_directory)
    #print(original_working_directory_absolute)
    if not os.path.exists(original_working_directory_absolute):
        print("original_working_directory not found:")
        print(original_working_directory_absolute)
        raise Exception
    from client import ClientWrapperSlim
    test_object = ClientWrapperSlim("complex_test_class", "ComplexTestClass", 54010, complex_datatypes = True, server=server)
    
    isup = test_object.ClientWrapper_meta_function("isup") == "True"
    print("server was running",isup)
    if not isup:
        virtualenv_source_command = ""
        if path_to_virtualenv != "":
            virtualenv_source_command = "source "+path_to_virtualenv_absolute+";"
        cd_command = "cd "+original_working_directory_absolute+";"
        py_command = "python example_server.py"
        py_command = command
        #whole_command = ['gnome-terminal -x sh -c \"ssh -Y '+server+' \''+virtualenv_source_command+cd_command+py_command+';$SHELL'+'\'\"' ]
        #whole_command = ['gnome-terminal -x ssh -Y '+server+' \"'+virtualenv_source_command+cd_command+py_command+';echo keeping shell open;$SHELL'+'\"' ]
        
        whole_command = ['gnome-terminal -x ssh -Y '+server+' " ' +virtualenv_source_command+cd_command+py_command+';echo keeping shell open;$SHELL" ' ]
        
        var1 = "s"
        var2 = "t"
        #subprocess.Popen('sh -c "'+py_command+'"', shell=True)
        #subprocess.Popen(py_command, shell=True)
        #return
        print("running:")
        print(whole_command)
        terminal = subprocess.Popen(whole_command, stdin=subprocess.PIPE, shell=True)
        for _ in range(20):
            isup = test_object.ClientWrapper_meta_function("isup") == "True"
            print("checking isup:",isup)
            if isup:
                return test_object
            time.sleep(1)
        raise Exception
    return test_object
    #time.sleep(10)
def test_remote_server():
    
    wrapped_code="""
    from complex_test_class import ComplexTestClass
    test_object = ComplexTestClass()
    test_object.value = "this is a value"
    print(test_object.value == "this is a value")
    print(hasattr(test_object, "value"))
    """
    
    wrapped_code="""
    from server import ServerWrapper
    from complex_test_class import ComplexTestClass
    test_object = ComplexTestClass('hallo')
    test_object = ServerWrapper(test_object,54010,complex_datatypes = True)
    """
    #get_object_from_wrapped_code(wrapped_code)
    print("jo")
    #test_object = start_server(path_to_virtualenv = "../env_flaskcom", original_working_directory=".",server="wtmgws9")
    test_object = start_server(path_to_virtualenv = "../env_flaskcom", original_working_directory=".",server="wtmgws9", wrapped_code= wrapped_code)
    print("isup",test_object.ClientWrapper_meta_function("isup"))
    print("shutdown",test_object.ClientWrapper_meta_function("shutdown"))
    print("isup",test_object.ClientWrapper_meta_function("isup"))
    return

    from client import ClientWrapperSlim

    image_name ="/informatik3/wtm/home/twiefel/sylviann/srl/flaskcom/wtmIcon_orig.png"
    
    test_object = ClientWrapperSlim("complex_test_class", "ComplexTestClass", 54010, complex_datatypes = True, server="wtmgws9")
    #test_object = ClientWrapper(ComplexTestClass, 54010)
    print("isup",test_object.ClientWrapper_meta_function("isup"))
    print("shutdown",test_object.ClientWrapper_meta_function("shutdown"))
    print("isup",test_object.ClientWrapper_meta_function("isup"))
    print(test_object.port)
    image = test_object.get_image(image_name)
    print(type(image))
    print(image    )
    #test_object.__getattr__("__setattr__")
    test_object.value = "this is a value"
    print(test_object.value == "this is a value")
    print(hasattr(test_object, "value"))
    
    print(test_object.value    )

def test_remote_object():
    
    wrapped_code="""
    from complex_test_class import ComplexTestClass
    test_object = ComplexTestClass('hallo')
    """
    from remote_object import RemoteObject
    test_object = RemoteObject(port = 54010,
                               path_to_virtualenv = "../env_flaskcom", 
                               original_working_directory=".",
                               server="wtmgws9", 
                               wrapped_code = wrapped_code,
                               keep_open = True
                               )
                               
                               
    image_name ="/informatik3/wtm/home/twiefel/sylviann/srl/flaskcom/wtmIcon_orig.png"
    image = test_object.get_image(image_name)
    print(type(image))
    #print(image    )

    test_object.value = "this is a value"
    print(test_object.value == "this is a value")
    print(hasattr(test_object, "value"))
    
    print(test_object.value    )

    print("isup",test_object.ClientWrapper_meta_function("isup"))
    raw_input("press enter to shutdown the remote object terminal")
    print("shutdown",test_object.ClientWrapper_meta_function("shutdown"))
    print("isup",test_object.ClientWrapper_meta_function("isup"))

def test_multiple_remote_objects():
    wrapped_code="""
    from flaskcom.complex_test_class import ComplexTestClass
    test_object = ComplexTestClass('hallo')
    """
    from flaskcom.remote_object import RemoteObject

    test_objects = []
    
    for i in range(2):
        test_object = RemoteObject(wrapped_code = wrapped_code,
                                   path_to_virtualenv = "./env_flaskcom", 
                                   keep_open = True
                                   )
        test_objects.append(test_object)
    
    for test_object in test_objects:
        test_object.value = "this is a value"
        print(test_object.value == "this is a value")
    
    raw_input("press enter to shutdown the remote object terminal")
    for test_object in test_objects:
        print("shutdown",test_object.ClientWrapper_meta_function("shutdown"))
        print("isup",test_object.ClientWrapper_meta_function("isup"))


def test_remote_object_with_closing():
    remote_object_with_closing("localhost")
    remote_object_with_closing("wtmgws9")

def remote_object_with_closing(server):
    #original initalization code:
    from flaskcom.complex_test_class import ComplexTestClass
    test_object = ComplexTestClass('hallo')
    
    #do some stuff with the object
    test_object.value = "this is a value"
    print(test_object.value == "this is a value")
    filename = "./flaskcom/wtmIcon_orig.png"
    image = test_object.get_image(filename)
    print(type(image))
    
    #wrap the original initialization code in a multiline string
    wrapped_code="""
    from flaskcom.complex_test_class import ComplexTestClass
    test_object = ComplexTestClass('hallo')
    """
    
    #initialize the test_object using a RemoteObject
    from flaskcom.remote_object import RemoteObject
    test_object = RemoteObject(wrapped_code = wrapped_code, keep_open=True, server = server)
    
    test_object.value = "this is a value"
    print(test_object.value == "this is a value")
    filename = "./flaskcom/wtmIcon_orig.png"
    image = test_object.get_image(filename)
    print(type(image))
    
    raw_input("press enter to shutdown the program")
    print("isup",test_object.ClientWrapper_meta_function("isup")    )
    print("shutdown",test_object.ClientWrapper_meta_function("shutdown"))
    print("isup",test_object.ClientWrapper_meta_function("isup"))
    print
def main():
    #test_complex_client_wrapper()
    #test_class_wrapping_without_import()
    #test_complex_client_wrapper_slim()
    #test_remote_server()
    test_remote_object_with_closing()
if __name__ == "__main__":
    main()
