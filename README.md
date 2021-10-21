# Flaskcom

Flaskcom is used to create remote objects in python.
The objects can be created easily out of your code base.
It is useful to connect modules, let computationally expensive 
parts run on a more powerful server with minimum effort.
Also, a client server architecture is provided

## how to setup:

open a terminal and navigate to your project.
if you don't have a project yet create one:
 
```bash
mkdir example_flaskcom
cd example_flaskcom
```
create a virtual environment
```bash
virtualenv env3 -p /usr/bin/python3.8
source env3/bin/activate
``` 

get the latest flaskcom:
```bash
pip install git+https://github.com/LemonSpeech/flaskcom.git
``` 
You also need to install flaskcom in the virtual environment on the server

get the examples:
```bash
python -m flaskcom.getting_started
```
This will copy the example files to the current directory.
Make them run and use them as a baseline for your project.
