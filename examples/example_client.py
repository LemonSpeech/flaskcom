# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 16:50:12 2018

@author: twiefel
"""
import os,sys
os.system('tput reset')
terminal_name = 'CLIENT'
sys.stdout.write("\x1b]2;"+terminal_name+"\x07")

def test_client_wrapper():
    from test_class import TestClass
    
    #we create a test object
    test_object = TestClass(5)
    
    #and to some attribute and method calls
    saved_value = test_object.saved_value
    print "test_object.saved_value",saved_value
    test_object.add_to_saved_value(1)
    saved_value = test_object.saved_value
    print "test_object.saved_value",saved_value
    print test_object.add_to_saved_value(2)
    saved_value = test_object.saved_value
    print "test_object.saved_value",saved_value
    print "test_object.saved_value",saved_value
    saved_value = test_object.get_saved_value()
    print "test_object.get_saved_value()",saved_value
    print "test_object.get_nothing()",[test_object.get_nothing()]
    
    from client import ClientWrapper

    #we create a test object by wrapping the TestClass in a client Wrapper
    #only the port has to be specified.
    #if the server runs on a server, you can specify the address like his:
    #   test_object = ClientWrapper(TestClass, 54010, server='wtmgws9')   
    test_object = ClientWrapper(TestClass, 54010)
    
    #we can do the same manipulations here. 
    #at the moment, only types that can be wrapped in json can be used
    #as arguments or return value
    #if you use non jsonifiable types, the server or client will throw a json exception
    saved_value = test_object.saved_value
    print "test_object.saved_value",saved_value
    test_object.add_to_saved_value(1)
    saved_value = test_object.saved_value
    print "test_object.saved_value",saved_value
    print test_object.add_to_saved_value(2)
    saved_value = test_object.saved_value
    print "test_object.saved_value",saved_value
    print "test_object.saved_value",saved_value
    saved_value = test_object.get_saved_value()
    print "test_object.get_saved_value()",saved_value
    print "test_object.get_nothing()",[test_object.get_nothing()]
    

def test_complex_client_wrapper():
    from complex_test_class import ComplexTestClass
    
    image_name ="/informatik3/wtm/home/twiefel/sylviann/srl/flaskcom/wtmIcon_orig.png"
    #we create a test object
    #test_object = ComplexTestClass()

    #image = test_object.get_image(image_name)
    #print type(image)
    #print image
    
    #test_object.show_image(image, "local image")

    
    from client import ClientWrapper
    test_object = ClientWrapper(ComplexTestClass, 54010, complex_datatypes = True)
    #test_object = ClientWrapper(ComplexTestClass, 54010)
    image = test_object.get_image(image_name)
    print type(image)
    print image    
    
    test_object.show_image(image, "remote image")
    
    raw_input()

def test_complex_client_wrapper_slim():

    
    image_name ="/informatik3/wtm/home/twiefel/sylviann/srl/flaskcom/wtmIcon_orig.png"

    from client import ClientWrapperSlim
    
    test_object = ClientWrapperSlim("complex_test_class", "ComplexTestClass", 54010, complex_datatypes = True)
    #test_object = ClientWrapper(ComplexTestClass, 54010)
    image = test_object.get_image(image_name)
    print type(image)
    print image    
    #test_object.__getattr__("__setattr__")
    test_object.value = "this is a value"
    print test_object.value == "this is a value"
    print hasattr(test_object, "value")
    
    print test_object.value
    #test_object.show_image(image, "remote image")
    
    #raw_input()
    
    
def test_class_wrapping_without_import():
    module_name =  "complex_test_class"
    class_name = "ComplexTestClass"
    from client import get_methods_without_import
    print get_methods_without_import(module_name, class_name)

def get_object_from_wrapped_code(wrapped_code):
    from threading import Thread
    import subprocess
    import os
    #command = "gnome-terminal -x python example_server.py"
    #terminal = subprocess.Popen(command.split(), stdin=subprocess.PIPE) 
    os.system("gnome-terminal -x sh -c \"ssh -Y wtmgws9 'cd sylviann/srl;source env_flaskcom/bin/activate;cd flaskcom;python example_server.py;$SHELL'\"")
    #terminal = subprocess.Popen(['xterm'], shell= True, stdin=subprocess.PIPE)
    import time
    time.sleep(2)
    print "wait"

    terminal.communicate("echo Hello World\n") 
    return
    
    from subprocess import Popen, PIPE

    #terminal = Popen(['xterm', '-e', '/bin/bash'], stdin=PIPE) #Or cat > /dev/null
    os.system("gnome-terminal -x sh -c \"ssh -Y wtmgws9 'cd sylviann/srl;source env_flaskcom/bin/activate;which python;$SHELL'\"")

    
    terminal.communicate("echo Hello World") 
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
    print [commands]
    process = subprocess.Popen('xterm', stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = process.communicate(commands)
    print out
    
def test_remote_server():
    
    wrapped_code="""
    from complex_test_class import ComplexTestClass
    test_object = ComplexTestClass()
    test_object.value = "this is a value"
    print test_object.value == "this is a value"
    print hasattr(test_object, "value")
    """
    
    wrapped_code="""
    from server import ServerWrapper
    from complex_test_class import ComplexTestClass
    test_object = ComplexTestClass()
    test_object = ServerWrapper(test_object,54010,complex_datatypes = True)
    """
    #get_object_from_wrapped_code(wrapped_code)
    print "jo"


    from client import ClientWrapperSlim

    image_name ="/informatik3/wtm/home/twiefel/sylviann/srl/flaskcom/wtmIcon_orig.png"
    
    test_object = ClientWrapperSlim("complex_test_class", "ComplexTestClass", 54010, complex_datatypes = True)
    #test_object = ClientWrapper(ComplexTestClass, 54010)
    print "isup",test_object.ClientWrapper_meta_function("isup")
    print "shutdown",test_object.ClientWrapper_meta_function("shutdown")
    print "isup",test_object.ClientWrapper_meta_function("isup")
    print test_object.port
    image = test_object.get_image(image_name)
    print type(image)
    print image    
    #test_object.__getattr__("__setattr__")
    test_object.value = "this is a value"
    print test_object.value == "this is a value"
    print hasattr(test_object, "value")
    
    print test_object.value    


def main():
    #test_complex_client_wrapper()
    #test_class_wrapping_without_import()
    #test_complex_client_wrapper_slim()
    test_remote_server()
if __name__ == "__main__":
    main()