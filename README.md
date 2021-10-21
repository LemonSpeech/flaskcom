# Flaskcom

## how to setup:

open a terminal and navigate to your project.
if you don't have a project yet create one:
 
```bash
mkdir example_flaskcom
cd example_flaskcom
```

get the latest flaskcom:
```bash
git clone https://git.informatik.uni-hamburg.de/twiefel/flaskcom/
``` 
set up a virtualenv if you need one for you project or take an existing one
```bash
virtualenv env_flaskcom
source env_flaskcom/bin/activate
``` 
install flaskcom dependencies:
```bash
pip install -r flaskcom/requirements.txt
```

get the example:
```bash 
cp flaskcom/example_remote_object.py .
```

run example 
```bash 
python example_remote_object.py
```

## example
this can be used to start with your own project
the code can be found in example_remote_object.py

```python
#this is an example how to create a remote object
#the function example_local() shows the original code
def example_remote():
    print
    print "----------------------"
    print "running example_remote"
    
    outside_variable = "B" #this variable is initialized in the main program
    
    #this function is run by the remote terminal
    #put all code inside that is needed to initialize your remote object
    def wrapped_function():
        print "starting wrapped function"

        from flaskcom.complex_test_class import ComplexTestClass
        print outside_variable # this variable is used by the remote terminal and therefore copied over.
        #you shouldn't refer to big objects here, as they have to be copied via socket.
        #Better only use thinks you really need, or initialize big objects within this function.
        
        inside_variable = outside_variable
        
        print "inside_variable:",inside_variable
        
        test_object = ComplexTestClass('hallo') #initialize the object you want to use
        
        print "end wrapped function"
        return test_object #return it
    
    #import the RemoteObject
    from flaskcom.remote_object import RemoteObject
    
    #wrap it around the function
    #returns an object that can be used like the object initialized in the wrapped function,
    #here: test_object = ComplexTestClass('hallo')
    test_object = RemoteObject(wrapped_function = wrapped_function, #the function that initializes the remote object
                               path_to_virtualenv = "./env_flaskcom", #a virtualenv can loaded before exectuting the code in the remote terminal.
                               server = "wtmgws9", #the remote object is running on another computer
                               original_working_directory = ".", #a working directory can be specified, which can be used to search for the code
                               keep_open = True, #the remote object can be kept open, when the program is exectuted the next time, it will use the open remote object instead of creating a new one
                               time_out = -1, #the time to wait for the remote terminal to start, -1 means forever
                               flaskcom_path = "../", #if flaskcom is not inside the searchpath, set a path to a folder containing flaskcom
                               debug = True) #keeps the terminal open even if an error occurs
    
    print "doing the object stuff"
    
    #do some stuff with the object
    test_object.value = "this is a value"
    print test_object.value == "this is a value"
    filename = "./flaskcom/wtmIcon_orig.png"
    image = test_object.get_image(filename)
    print "type(image):",type(image)    
    print "test_object.value:",test_object.value
    print type(test_object)
    print "thats it"

#the original code, that was modified to use a remote object in example_remote()
def example_local():
    print
    print "----------------------"
    print "running example_local"
    
    outside_variable = "B" #this variable is initialized in the main program
    
    #this function is run to initialize the object
    def wrapped_function():
        print "starting wrapped function"

        from flaskcom.complex_test_class import ComplexTestClass
        print outside_variable 
        inside_variable = outside_variable
        
        print "inside_variable:",inside_variable
        
        test_object = ComplexTestClass('hallo') #initialize the object you want to use
        
        print "end wrapped function"
        return test_object #return it
    
    #initialize the object with the function. This part is replaced later to initialize the romote object
    test_object = wrapped_function()
    
    print "doing the object stuff"
    
    #do some stuff with the object
    test_object.value = "this is a value"
    print test_object.value == "this is a value"
    filename = "./flaskcom/wtmIcon_orig.png"
    image = test_object.get_image(filename)
    print "type(image):",type(image)    
    print "test_object.value:",test_object.value
    print type(test_object)
    print "thats it"
    


if __name__ == "__main__":
    example_remote()
    example_local()
```


## older examples (may not work any longer)

the examples create one or more remote objects. Use this as a start for your own project.
```python
#original initalization code:
from flaskcom.complex_test_class import ComplexTestClass
test_object = ComplexTestClass('hallo')

#do some stuff with the object
test_object.value = "this is a value"
print test_object.value == "this is a value"
filename = "./flaskcom/wtmIcon_orig.png"
image = test_object.get_image(filename)
print type(image)

#wrap the original initialization code in a multiline string
wrapped_code="""
from flaskcom.complex_test_class import ComplexTestClass
test_object = ComplexTestClass('hallo')
"""

#initialize the test_object using a RemoteObject
from flaskcom.remote_object import RemoteObject
test_object = RemoteObject(wrapped_code = wrapped_code)

#do some stuff with the remote object
test_object.value = "this is a value"
print test_object.value == "this is a value"
filename = "./flaskcom/wtmIcon_orig.png"
image = test_object.get_image(filename)
print type(image)

raw_input("press enter to shutdown the program")
```

an example creating multiple remote objects:
```python
#again, wrap the code
wrapped_code="""
from flaskcom.complex_test_class import ComplexTestClass
test_object = ComplexTestClass('hallo')
"""    
#create multiple objects with adanced parameters
from flaskcom.remote_object import RemoteObject
test_objects = []
for i in range(2):
    test_object = RemoteObject(wrapped_code = wrapped_code,
                               path_to_virtualenv = "./env_flaskcom", #now, a virtualenv is loaded before exectuting the code.
                               server = "wtmgws9", #the remote object is running on another computer
                               original_working_directory = ".", #a working directory can be specified, which can be used to search for the code
                               keep_open = True) #the remote object can be kept open, when the program is exectuted the next time, it will use the open remote object instead of creating a new one
    test_objects.append(test_object)

#do some stuff with remote the objects
for idx,test_object in enumerate(test_objects):
    test_object.value = "this is a value in test_object "+str(idx)
    print test_object.value

raw_input("press enter to shutdown the program")

#if the remoteobject was started with parameter keep_open= True, it can be shutdown manually:
for test_object in test_objects:
    print "shutdown:", test_object.ClientWrapper_meta_function("shutdown")
    print "isup:", test_object.ClientWrapper_meta_function("isup")
```