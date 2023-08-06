import os,dill
import inspect
import gzip,pickle
import shelve,os
import importlib,yaml

def get_root():

    #os.environ['HOME']
    return os.getcwd()

def get_current_project():

    with open(get_root() + '/.efunx/metadata', 'rb') as f:
     current_project = dill.load(f)['current_project']

    return current_project


def load_function(module_name,function_name,inputs=None,outputs=None):

    filename = function_name.split('/')[0]
    #load functions from module 
    module = importlib.import_module(module_name + '.' + filename)

    function_name = function_name.split('/')[1]

    func = getattr(module,function_name)   

    add_functions([func],inputs=inputs,outputs=outputs)


def load_npz(filename):

    with gzip.open(filename, 'rb') as f:

          return pickle.load(f)


def get_fun_info(func):

    data = func.__annotations__
    input_variables = []
    output_variables = []
    for key,value in data.items():
      if not key == 'return':
         input_variables.append(value)
      else:
         value = value.replace('(','')
         value = value.replace(')','')
         value = value.split(',')
         output_variables = value

    #In this case we take the parameters
    if len(input_variables) == 0:
        input_variables = list(inspect.signature(func).parameters.keys())

    #Make a function a leaf so it runs
    leaf = False
    if len(output_variables) == 0:
       output_variables = [func.__name__]
       leaf = True

    return {'function':func,'input':input_variables,'output':output_variables,'leaf':leaf}


#def add_data(data,filename):

#   basename = os.environ['HOME'] + '/.efunx'
#   with shelve.open(basename + '/data', 'c',writeback=True) as shelf:
#    for d in data:
#      key = list(d.keys())[0]
#      filename =  filename +  d[key]
#      if filename[-3:] == 'npz':
#        variable = load_npz(filename)
#        shelf[key] = {0:variable}




def add_pipelines(pipelines):

   current_project = get_current_project()

   basename = get_root() + '/.efunx/' + current_project + '/pipelines' 
   with open(basename, 'rb') as f:
     master = dill.load(f)

   for pipeline in pipelines:  
        key = next(iter(pipeline))
        master[key] = pipeline[key].split(',')

   with open(basename, 'wb') as f:
    dill.dump(master,f)


def add_functions(functions,inputs=None,outputs=None):

     current_project = get_current_project()
   
     basename = get_root()+ '/.efunx/' + current_project + '/functions' 
     with open(basename, 'rb') as f:
       master = dill.load(f)

     for func in functions:  
      info =  get_fun_info(func)
      master[func.__name__] = info

     with open(basename, 'wb') as f:
      dill.dump(master,f)

def add_pipeline(name,pipeline):

   current_project = get_current_project()
   basename = get_root() + '/.efunx/' + current_project + '/pipelines' 

   with open(basename, 'rb') as f:
     master = dill.load(f)
   with open(basename, 'wb') as f:
     master[name] =  pipeline
     dill.dump(master,f)

def load_file(filename,module_name):

      stream = open(filename, 'r')
      main = yaml.safe_load(stream)
      #Load functions
      funcs = main['functions']
      for func in funcs:
       load_function(module_name,func)
      #Load pipelines
      if 'workflows' in main.keys():
         add_pipelines(main['workflows']) 


def load_module(module_name):
    """Loads a pip-installed module"""

    module = importlib.import_module(module_name)
    filename = '/'.join(module.__file__.split('/')[:-1]) + '/efunx.yaml'
    if not os.path.isfile(filename):
        print('No filename found')
        quit()
        
    load_file(filename,module_name)



