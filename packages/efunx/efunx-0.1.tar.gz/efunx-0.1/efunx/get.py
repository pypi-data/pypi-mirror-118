from .efunx import *
import sys,os
import functools

def get(f,debug=False,functions=None,show_graph=False,store_functions=True,workflow=None,priority=None,developing={},parallel=[],dev_all=False):
     
    if not type(priority) == list: priority = [priority]
    def wrapper(*argv,**kargv):

     #if not type(argv) == int:   
     #     if len(argv) > 0 :kargv.update(argv[0]) #In case some data is not passed as a reference

     cm = engine(debug=debug,functions=functions,store_functions=store_functions,priority=priority,developing=developing,parallel=parallel,dev_all=dev_all)

     return cm.compute(f,init_variables=kargv,show_graph=show_graph,workflow=workflow)

    return wrapper



