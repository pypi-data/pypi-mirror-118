'''
Made by Jv Kyle Eclarin

Borrows heavily from pathlib, os, shutil, and glob
'''

import os as _os
import sys as _sys
import shutil as _shutil
import inspect as _inspect
from glob import glob as _glob
from pathlib import Path as _Path
from copy import deepcopy as _deepcopy
from importlib.machinery import SourceFileLoader as _SourceFileLoader



# find path of the file doing the importing
filedir = None

for frame in _inspect.stack()[1:]:
    if frame.filename[0] != '<':
        filedir = frame.filename
        break
if filedir == None:
    # Returns cwd for interactive terminals
    # filedir = _os.getcwd()
    filedir = str(_Path.cwd())


class getpath(str):
    '''
# IMPORTING

from getpaths import getpath


# USING CURRENT FILE PATH

current_dir = getpath() # current file's path


# USER-SPECIFIED PATH

custom_dir = getpath('a','b',custom=True)
print(custom_dir)
# /a/b


# ADD FILES

custom_dir/'example.txt'
# /a/b/example.txt

custom_dir.add('/a/example.txt')
# /a/b/example.txt


#  GO UP THE DIRECTORY

custom_dir = getpath('a','b',custom=True)

custom_dir/'..'
# /a

custom_dir.add('..')
# /a

custom_dir.up(1)
# /a


# LIST EXISTING FILES AND FOLDERS

custom_dir.ls()
# /a/b/example.txt
# throws error if path does not exist

    '''
    def __new__(cls, *args, custom=False, start_at_root=True):

        if custom:
            paths = []
        else:
            paths = [_os.path.dirname(filedir)]

        for arguments in args:
            if arguments == '..':
                paths[0] = _os.path.split(paths[0])[0]
            else:
                paths.append(arguments)
        
        
        path = _os.sep.join(paths)

        # get rid of accidental doubling
        if custom:
            double = _os.path.sep + _os.path.sep
            while double in path:
                path = path.replace(double, _os.path.sep)
                
        if start_at_root == True:
            if path[0] != _os.path.sep:
                path = _os.path.sep + path

        return str.__new__(cls, path)
    
    def __init(self):
        super().__init__(self)
    
    def add(self, *args):
        return self.__truediv__(*args)
    
    def __truediv__(self, *args):
        # same as add
        current_path = _deepcopy(self.__str__())

        paths = [current_path]
        
        for arguments in args:
            # convert arguments to 
            if type(arguments) != type(str()):
                try:
                    arguments = str(arguments)
                except:
                    print('path could not be converting to a string')
                    raise TypeError

            if arguments == '..':
                paths[0] = _os.path.split(paths[0])[0]
            else:
                paths.append(arguments)
        
        path = _os.sep.join(paths)
        return getpath(path, custom=True)
    
    def ls(self, *args, full=False):
        '''
        same as os.listdir()

        if full=True, then this returns a list of absolute paths
        '''
        paths = args
        
        path = _os.sep.join([self.__str__(), _os.sep.join(paths)])

        files_and_stuff = _os.listdir(path)
        
        if full == True:
            return [getpath(path, custom=True) for path in files_and_stuff]
        else:
            return files_and_stuff
    
    def find(self, path, *args, **kwargs):
        '''
        same as glob.glob()
        '''
        files_and_stuff = _glob(_os.path.join(self.__str__(), path), *args, **kwargs)
        return [getpath(path, custom=True) for path in files_and_stuff]
    
    def isfile(self):
        return _os.path.isfile(self.__str__())
    
    def isdir(self):
        return _os.path.isdir(self.__str__())
    
    def exists(self):
        '''
        returns 
        same as os.path.exists()
        '''
        return _os.path.exists(self.__str__())
    
    def copyfile(self, destination, **kwargs):
        '''
        copies current path if current path is a file to destination
        same as shutil.copyfile
        '''
        assert _os.path.isfile(self.__str__()) == True
        _shutil.copyfile(self.__str__(), destination, **kwargs)
    
    def copydir(self, destination, **kwargs):
        '''
        copies current path if current path is a file to destination
        same as shutil.copyfile
        '''
        assert _os.path.isdir(self.__str__()) == True
        _shutil.copy(self.__str__(), destination, **kwargs)
    
    def move(self, destination, **kwargs):
        '''
        moves current path to destination
        '''
        assert _os.path.exists(self.__str__()) == True
        _shutil.move(self.__str__(), destination, **kwargs) 
    
    def mkdir(self, **kwargs):
        '''
        same as os.makedirs()
        '''
        assert _os.path.isdir(self.__str__()) == True
        _os.makedirs(self.__str__(), **kwargs)
    
    def rmdir(self, **kwargs):
        '''
        same as os.rmdir()
        '''
        assert _os.path.isdir(self.__str__()) == True
        _os.rmdir(self.__str__(), **kwargs)
    
    def mkfile(self,  data='', *args, **kwargs):
        with open(self.__str__(), *args, **kwargs) as file_handler:
            file_handler.write(data)
    
    def rmfile(self, **kwargs):
        assert _os.path.isdir(self.__str__()) == True
        _os.remove(self.__str__(), **kwargs)
    
    def write(self, *args, **kwargs):
        self.mkfile(*args, **kwargs)
    
    def read(self, *args, **kwargs):
        assert _os.path.isfile(self.__str__()) == True
        with open(self.__str__(), *args, **kwargs) as file_handler:
            file_handler.read(data)
    
    def readfast(self, name='', *args, **kwargs):
        '''
        generator for reading large files quickly
        does not open entire file, but yields it one line at a time
        '''
        
        assert _os.path.isfile(self.__str__()) == True

        with open(self.__str__(), *args, **kwargs) as file_handler:
            for line in file_handler:
                yield line
        
    def up(self, num, *args):
        paths = []
        for arguments in args:
            paths.append(arguments)
        
        path = _os.sep.join([self.__str__(), _os.sep.join(paths)])

        times_up = ['..' for i in range(num+1)]
        return getpath(path, *times_up, custom=True)
    
    def splitpath(self, full=False):
        '''
        same as os.path.split
        if full=True, returns list of strings
        '''
        path = _os.path.split(self.__str__())
        if full == True:
            return self.__str__().split(os.path.sep)
        else:
            return [getpath(path[0], custom=True), path[1]]
    


def importfile(path):
    '''
    same as importlib.util.SourceFileLoader()
    returns file functions, classes, and global variables from a python file
    '''
    path = getpath(path, custom=True)
    assert _os.path.isfile(path) == True

    file_handler = _SourceFileLoader(*path.splitpath())
    return file_handler



class importdir:
    '''
    imports .py files from directory
    '''
    def __init__(self, path):
        assert _os.path.isdir(path) == True
        path = getpath(path, custom=True)

        python_files = path.find('*.py')
        if len(python_files) == 0:
            return

        for python_file in python_files:
            name = python_file.splitpath()[1][:-3]
            try:
                setattr(self, name, importfile(python_file))
            except:
                print('was not able to to load modules from', python_file)



cwd = getpath(str(_Path.cwd()), custom=True)
filedir = getpath(filedir, custom=True)