from fabric.api import *
from fabric.contrib import files
from fabric.contrib.files import exists, sed
from fabric.colors import green, red, blue
from fabric.contrib import project
import time
import json
# import os
# import zipfile
# import sys
# import pprint
import re

def backup():
    print(green('pulling remote repo...'))
    local('git pull')
    print(green('adding all changes to repo...'))
    local('git add .')
    print(green("enter your comment:"))
    comment = input()
    local('git commit -m "{}"'.format(comment))
    print(green('pushing master...'))
    local('git push -u origin master')

def commit():
    local('git add .')
    local('git commit -m "commit {}"'.format(time.ctime()))
    print(green(
        """
        ********************
        **COMMIT COMPLETE***
        ********************
        """
    ))

def push():
    commit()
    local('git push -u origin master')

def start():
    local('google-chrome http://127.0.0.1:8000/')
    local('python3 manage.py runserver')

def migrate():
    local('python3 manage.py makemigrations --noinput')
    local('python3 manage.py migrate')

def admin():
    local('google-chrome http://127.0.0.1:8000/admin/')