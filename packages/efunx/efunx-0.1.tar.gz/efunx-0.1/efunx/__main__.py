import sys
import os,dill
from termcolor import colored, cprint 
import inspect
import os
import shutil
import shelve
from termcolor import colored
import importlib
from .registry import *

def start_project(name):

      folder = get_root() + '/.efunx'

      
      if os.path.exists(folder + '/' + name):
          shutil.rmtree(folder + '/' + name)

      os.makedirs(folder + '/' + name)
      basename = folder + '/' + name + '/functions'
      with open(basename, 'wb') as f:
       dill.dump({},f)

      basename = folder + '/' + name + '/pipelines'
      with open(basename, 'wb') as f:
       dill.dump({},f)

      basename = folder + '/' + name + '/data'
      with shelve.open(basename, 'c',writeback=True) as shelf:
            shelf = {}

      basename = folder + '/' + name + '/_state'
      with shelve.open(basename, 'c',writeback=True) as shelf:
            shelf = {}

      #basename = folder + '/' + name + '/data'
      #with open(basename, 'wb') as f:
      # dill.dump({},f)

def set_project(name):

      basename = get_root() + '/.efunx/metadata'
      with open(basename, 'rb') as f:
        data = dill.load(f)
        data['current_project'] = name

      with open(basename, 'wb') as f:
        dill.dump(data,f)


def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]


    if args[0] == 'clear':

      name = 'global'
      folder = get_root() + '/.efunx'
      basename = folder + '/' + name + '/data'
      with shelve.open(basename, 'c',writeback=True) as shelf:
            shelf = {}

      basename = folder + '/' + name + '/_state'
      with shelve.open(basename, 'c',writeback=True) as shelf:
            shelf = {}



    if args[0] == 'init':
      #INIT REGISTRY LOCALLY  

      folder = get_root() + '/.efunx'
      if os.path.exists(folder):
          shutil.rmtree(folder)
      os.makedirs(folder)
      #init metadata 
      basename = get_root() + '/.efunx/metadata'
      with open(basename, 'wb') as f:
        dill.dump({},f)

      #Start global project
      start_project('global')
      set_project('global')
      print(" ")
      print(colored('Init Efunx','blue'))
      print(" ")


    #if args[0] == 'start':
    # project_name =  args[1]
    # start_project(project_name)
    # set_project(project_name)
    # print(" ")
    # print(colored('Started project ' + project_name,'blue'))
    # print(" ")

     
     #global project

    if args[0] == 'load':

       load_module(args[1]) 

    if args[0] == 'load_file':

       load_file(args[1]) 

    if args[0] == 'list':

      #Show functions 
      print(' ')
      print(colored('FUNCTIONS','blue'))
      current_project = get_current_project()  
      basename = get_root() + '/.efunx/' + current_project + '/functions' 
      with open(basename, 'rb') as f:
       data = dill.load(f)
       for key,value in data.items():
           inputs  = ','.join([i for i in value['input']])
           outputs = ','.join([i for i in value['output']])
           print(colored(key,'green'),': ',inputs,'->',outputs) 

      #Show pipelines 
      print(' ')
      print(colored('WORKFLOWS','blue'))
      basename = get_root() + '/.efunx/' + current_project + '/pipelines' 
      with open(basename, 'rb') as f:
       data = dill.load(f)
       for key,value in data.items():
        wf = ' -> '.join([str(i) for i in value])
        print(colored(key,'green'),': ',wf) 


      #print(' ')
      #print(colored('DATA','blue'))
      #basename = os.environ['HOME'] + '/.efunx'
      #with shelve.open(basename + '/data', 'c',writeback=True) as shelf:
      #    for key in shelf.keys(): 
      #        print(key)
      



if __name__ == "__main__":
    sys.exit(main())
