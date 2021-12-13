#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 24 15:28:17 2021

@author: twiefel
"""

import flask_login
from pathlib import Path


def get_user_directory():
    current_path = str(Path().resolve())
    Path(current_path + "/user_data/" + flask_login.current_user.id ).mkdir(parents=True, exist_ok=True)
    return current_path + "/user_data/" + flask_login.current_user.id 