from __future__ import annotations
import dill as pickle
import functools
import os
import numpy as np
import codecs
from deepdiff import DeepDiff,DeepHash
import sys
import networkx as nx
import dill
import matplotlib.pylab as plt
from networkx.drawing.nx_agraph import write_dot, graphviz_layout
from inspect import getmembers, isfunction
import importlib
import os
from termcolor import colored
from .registry import *
import shelve
import yaml
import inspect
from mpi4py import MPI

comm = MPI.COMM_WORLD
def print_safe(text):

    if comm.rank == 0:
        print(text)

def print_command(cmd,text):
    if comm.rank == 0:    
     print(colored(cmd,'green') + text)


def load_from_file(filename):
 """Load functions and pipelines from files"""

 #import functions
 module = importlib.import_module(filename)

 #import functions
 for i in getmembers(module,isfunction):
      if len(i[1].__annotations__) > 0:
         registry(i[1]) 
 
#Functions that tells if a function is in development mode
#def dev(func):
#    func.dev = dev
#    add_functions([func])
#    @functools.wraps(func)
#    def wrapper(*args, **kwargs):
#        return func(*args, **kwargs)
#    wrapper.dev = True
#    return wrapper


def efunx(func):
 """efunx decorator"""
 if comm.rank == 0:   
  add_functions([func])
 comm.Barrier() 

 @functools.wraps(func)
 def wrapper(*argv,**kwargs):

        return func(*args, **kwargs)

 return wrapper

def compare_dict(var1,var2):
     """compare hashable data for caching"""
    
     return DeepHash(var1)[var1] == DeepHash(var2)[var2]


class engine(object):

    def __init__(self,functions = None,debug=False,store_functions = True,priority=[],developing=[],parallel=[],dev_all=False):

        self.funcs = {}
        self.debug = debug
        self.store_functions = store_functions
        self.output_channels = {}
        self.output_channels_map = {}
        self.input_channels = {}
        self.dev = {d:True for d in developing} 
        self.dev_all = dev_all
        self.master_data = {}
        self.priority=priority
        self.cached = {}
        self.shared = {}
        self.versions = {}
        self.parallel = parallel
        self.developing = {}

        #Set the cache based on the current project
        basename = get_root() + '/.efunx/metadata'
        with open(basename, 'rb') as f:
            self.current_project = dill.load(f)['current_project']

        self.cache = get_root() + '/.efunx/'+ self.current_project  
        #---------------

        #Load global projects
        basename = get_root() + '/.efunx/global/functions' 
        with open(basename, 'rb') as f:
            self.master = dill.load(f)

        #Add functions---
        for key,value in self.master.items():
            self.__add_function(value)
            self.shared[key]     = True

    #def add_parallel(self,funcs):

    #    for fun in funcs:
    #        self.shared[fun] = False


    def plot_graph(self):
         """Plot workflow""" 
    
         G = nx.DiGraph()

         #Add nodes---
         for i in self.run:
           G.add_node(i)

         #Add edges---
         nm = len(self.run)
         for i in range(nm):
          for j in range(nm)[i+1:]:
           
              if any([item in self.output_channels_map[self.run[i]] for item in self.input_channels[self.run[j]]]):
                  G.add_edge(self.run[i],self.run[j]) 

         subax1 = plt.subplot(111)  

         pos = graphviz_layout(G, prog='dot')
         nx.draw(G,with_labels=True,pos=pos)

         plt.show()


    def __add_function(self,data,shared=True):
        """Add a function"""
        
        func            = data['function']
        input_channels  = data['input']
        output_channels = data['output']

        #Update function  
        self.funcs.update({func.__name__:func})

        #Developing
        if hasattr(func,'dev'):
           self.developing[func.__name__] = True
        else:   
            if func.__name__ in self.dev.keys():
              self.developing[func.__name__] = True
            else:  
              self.developing[func.__name__] = self.dev_all
        if data['leaf']:self.developing[func.__name__] = True      

        #Developing
        self.shared[func.__name__] = shared

        #Update output channel 
        for channel in output_channels:
            if channel in self.output_channels.keys():
              if func.__name__ in self.priority:  #This is the case when we select which function to use
                self.output_channels.update({channel:func.__name__})
            else:   
                self.output_channels.update({channel:func.__name__})

        #Update input channels
        self.input_channels.update({func.__name__:input_channels})

        #Update output channels
        self.output_channels_map.update({func.__name__:output_channels})
       
        for channel in input_channels:  
            self.cached[channel] = False
            #self.recompute[channel] = False

        for channel in output_channels: 
            self.cached[channel] = False
            #self.recompute[channel] = False


    def save_variable(self,key,variable):

         data = None
         if comm.rank == 0:
          with shelve.open(self.cache + '/data', 'c',writeback=True) as shelf:
             #retrieve current version
             if key in shelf.keys():
              version = len(shelf[key])   
              shelf[key].update({version:variable})
             else: 
              version = 0   
              shelf[key] = {version:variable}
             data = [version]   
         return comm.bcast(data,root=0)[0]
 
    def save_pipeline(self,key,variable):

         with shelve.open(self.cache + '/pipeline', 'c',writeback=True) as shelf:
            shelf[key] = variable

    def load_workflow(self,key):

          with open(self.cache + '/pipelines', 'rb') as f:
            return dill.load(f)[key]

    def load_variable(self,key,version=-1):
         
         if not key in self.master_data.keys(): #we avoid double loading
             with shelve.open(self.cache + '/data', 'r') as shelf:
                    

                    if key in shelf.keys():
                     if version == -1: version = len(shelf[key])-1
                     data =  shelf[key][version]
                     print_command('LOAD ',key)
                     return data
                    else: 
                     return {}

         return self.master_data[key]


    def check_against_cache(self,channel,value):
        
        data = None
        if comm.rank == 0:
         with shelve.open(self.cache + '/data', 'c',writeback=True) as shelf:

            if channel in shelf.keys():
              present = False  
              for version_tentative,cached in shelf[channel].items():
                  if compare_dict(value,cached):
                      version = version_tentative #key stored and version matsh
                      present = True
              if not present: #The stored and version does not match
               version = len(shelf[channel])   
               shelf[channel].update({version:value})        
            else: 
               version = 0 
               shelf[channel] = {version:value}
            
            data = [version] 
        
        return comm.bcast(data,root=0)[0]
             


    def print_log(self,text,color='white'):

        if self.debug : print(colored(text,color=color))

    def run_function(self,func_name):

       state  = self.get_cached_state(func_name)
       comm.Barrier()
       if not state == None:
          for channel in self.output_channels_map[func_name]:
              self.versions[channel] = state[channel] #Cached

       else:

         input_data = []
         
         for channel in self.input_channels[func_name]:
             self.master_data[channel] = self.load_variable(channel) #To avoid double loading

             input_data.append(self.master_data[channel])

         print_command('RUN  ',func_name)
         output_data = self.funcs[func_name](*input_data)

         if not type(output_data) == list: output_data = [output_data]

         output_data = {self.output_channels_map[func_name][n]:value   for n,value in enumerate(output_data) }#from list to dics

         self.master_data.update(output_data) #add new values in memory

         for key,variable in output_data.items():
              self.versions[key] = self.save_variable(key,variable) #save for later use 

         self.save_function_state(func_name)


    def get_cached_state(self,func_name):
 
        #Hash input and function's code---
       state = None
       if comm.rank == 0:
        input_versions =[]
        for channel in self.input_channels[func_name]:
          input_versions.append(self.versions.setdefault(channel,0))
        input_versions.append(inspect.getsource(self.funcs[func_name]))
        #------------

        key = dill.dumps(input_versions)

        with shelve.open(self.cache + '/_state', 'c',writeback=True) as shelf:
            if not func_name in shelf.keys():
               state =  None
            else:
               if key in shelf[func_name].keys():
                   state = {self.output_channels_map[func_name][n]:i for n,i in enumerate(shelf[func_name][key])}
               else: state =  None

       return comm.bcast(state,root=0)

               
               


    def save_function_state(self,func_name):
       """save the function state"""
       if comm.rank == 0:
        input_versions =[]
        for channel in self.input_channels[func_name]:
          input_versions.append(self.versions[channel])
        input_versions.append(inspect.getsource(self.funcs[func_name]))


        output_versions =[]
        for channel in self.output_channels_map[func_name]:
          output_versions.append(self.versions[channel])

        #print(input_versions,output_versions,func_name)
        with shelve.open(self.cache + '/_state', 'c',writeback=True) as shelf:
            if func_name in shelf.keys():
             shelf[func_name].update({dill.dumps(input_versions):output_versions})
            else: 
             shelf[func_name] = {dill.dumps(input_versions):output_versions}
       comm.Barrier()

   
    def compute_automatic_workflow(self,final_channels):

       self.run = []
       def get_child(channels):

           for variable in channels:
               if variable in self.output_channels.keys():
                func_name = self.output_channels[variable]
                if func_name in self.run: self.run.remove(func_name) #delete duplicates
                self.run.insert(0,func_name)
                channels = self.input_channels[func_name]
                get_child(channels)

       get_child(final_channels)


    def compute(self,final_channels,leaf=False,show_graph = False,init_variables = {},workflow=None):

       #update to a list if need be 
       if not type(final_channels) == list: final_channels = [final_channels]

       #Compute workflow---
       if workflow==None:
           self.compute_automatic_workflow(final_channels)
       elif type(workflow) == list:
           self.run = workflow
       elif type(workflow) == str:
           self.run = self.load_workflow(workflow)
       #------------

       #Build graph---
       if show_graph: self.plot_graph()
       wf = ' -> '.join([str(i) for i in self.run])
       print_command('WORKFLOW ',wf)
       #-------------------

       #Handle init variables for caching
       for key,value in init_variables.items():
           version = self.check_against_cache(key,value)
           self.versions[key] = version
       self.master_data.update(init_variables)
       comm.Barrier()

       #Run the code---
       for n,func_name in enumerate(self.run):
           self.run_function(func_name)
       
       #If none of the variables have been loaded, we load just the final_channels
       for channel in final_channels:
         if not channel in self.master_data.keys():
          self.master_data[channel] = self.load_variable(channel,version=self.versions[channel])


       final_output = []
       for channel in final_channels:
           if compare_dict(self.master_data[channel],{'dummy':np.asarray([-1],np.int32)}):
              final_output.append(None) # in case of leaves
           else:   
              final_output.append(self.master_data[channel])

       if len(final_output) == 1: final_output = final_output[0]

       return final_output



