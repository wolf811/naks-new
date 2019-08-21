from fabric.api import *
from fabric.contrib import files
from fabric.contrib.files import exists, sed
from fabric.colors import green, red, blue
from fabric.contrib import project
# import time
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