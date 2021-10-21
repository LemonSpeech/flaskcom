# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 12:15:20 2019

@author: twiefel
"""
if __name__ == "__main__":
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.dirname(os.path.abspath(__file__))+"/.."))
    
    
    from flaskcom import function_decoder
    function_decoder.start()
