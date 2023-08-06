
<img src="efunx.png" alt="drawing" width="500"/>


# efunx

`efunx` is a Python-based software for graph-based data persistence. It has the following features:

* Disk-caching hashable data 
* Workflow caching, i.e. end-to-end data optimization rather than at the single-function level.
* Automatic workflow identification via annotated data
* Definition of priorities paths in case of workflow ambiguities
* Loading a set of functions/workflows from pip-installed Python modules.
* Thread-safe (tested with `mpi4py`)

## Install

`efunx` is on the `pypi` repository, and relies on `mpi` libraries

```bash
apt-get update
apt-get install build-essential libopenmpi-dev libgmsh-dev
pip install --upgrade --no-cache efunx
```


To start using `efunx`, we need to initialize it

```bash
efunx init
```

## Caching

The main purpose of `efunx` is caching, i.e. reusing functions' outputs whenever possible. To cache a function, we simply use the decorator `efunx`

```python
from efunx import efunx,get

@efunx
def add(a,b):
    return a + b

get('add',debug=True)(a=1,b=2)
```
In this case, we simply have the `add` function. To compute a variable, we use the function `get` along with the variable's name. By default, the name of the output is the name of the function itself (more on this below). We use `debug=True` in order to inspect the actual operations being executed

```bash
WORKFLOW add
RUN  add
3
```
In this case, we see that the workflow is simply `add`. If we now run the above script again, we have
```bash
WORKFLOW add
LOAD add
3
```
The function `add` is not executed this time since the inputs are the same. It is also possible to declare only a subset of variables, provided the missing ones have been previously computed. In our case, we have

```python
@efunx
def add(a,b):
    return a + b

get('add',debug=True)(a=2)
```

```bash
WORKFLOW add
LOAD b
LOAD add
4
```

We note that inputs and outputs can be generic Python, hashable dictionaries.

Let's now change the source code of `add`, while keeping the inputs the same

```python
@efunx
def add(a,b):
    print(' ')
    return a + b

get('add',debug=True)(a=1,a=2)
```

```bash
WORKFLOW add
RUN  add
3
```

`add` is executed again, triggered by the change in the undelying code. This disk persistency is achieved by hashing the combination of inputs and source code of `add`. In most cases, however, we might want to run a function anyway; common cases include the change of imported libraries or in the Python version. To override caching mechanisms, we pass the option `developing="sum"` to the `get` call. We can also pass a list of functions' names. 


## Variable tags
In the example above, we have implicitly assigned the tags `a` and `b` to the inputs and `add` to the output. However, in some cases, and expecially when we have multiple outputs, we may want to tag them directly. To do so, we use annotations 

```python

def f(a:'x',b:'y')->'z,u':
    print(' ')
    return a + b,a-b

get('u',debug=True)(a=1,b=2)
```

```bash
WORKFLOW f
RUN  f
-1
```

## Function composition
The above syntax can also be used to compose functions

```python
@efunx
def f1(a,b)->'c':
    return a + b

@efunx
def f2(c,d):
    return c-d

get('f2',debug=True)(a=1,b=2,d=3)
```

```bash
WORKFLOW f
RUN  f1
RUN  f2
0
```

`efunx` will automatically detect the workflow based on the variables' tags. Here, the argument of the composed function are `a`, `b` and `d`. In this regard, we can see a composition simply as an effective function. The main strength of `efunx` comes when caching workflows. In this case, if we change the value of one variable, e.g. `d`, only the affected subgraph will be recomputed. This has clear benefits over cases where caching is applied at a single-function level, in that it may spare several variable loadings.

In most cases, workflows are not unique; for example when one needs to choose between two models with the same input and output tags. In this case, we can either add the keyword-value option `workflow=['f1','f2']` or, when two possible workflows are identical except for a relatively few functions, specify a priority list; to do so, we use the option `priority = ["f1"]`.

## Importing Modules

The `efunx` decorators are responsable for serializing functions, whenever possible; that is, it may be possible to use and compose functions defined elsewhere. For example it is posssible to import functions from an external module. To serve this purpose, `efunx` provides the command
```bash
efunx load module_name
```
Currently, only pip-installed modules are supported. On the module side, functions can be made available by craeting a `yaml` file with the following syntax

```yaml
---
  functions:
   - file1/function1
   - file1/function2
   - file2/function3
   - ....
  workflows:
   - p1    : function1,function3,function2
   - p2    : function1,function3
   - ...
```
where suggested worflows are specified as well. In this case, we specify a workflow with `workflow=p1`. Finally, private lists of functions/workflows can be loaded directly with

```bash
efunx load_file absolute_file_path
```

## Example

Here we use `efunx` to perform nanoscale heat transport calculations, using the software [OpenBTE](https://openbte.readthedocs.io/en/latest/). Assuming we have `OpenBTE` installed, we begin with

```bash
efunx init
efunx load openbte
efunx list
```
```bash
FUNCTIONS
almabte2openbte :  options_almabte -> rta
rta2DSym :  rta,options_material -> material
rta3D :  rta,options_material -> material
gray2D :  options_material -> material
geometry :  options_geometry -> geometry
first_guess :  geometry,material,options_first_guess -> temperatures
solve_rta :  geometry,material,temperatures,options_solve_rta -> solver
kappa_mode_2DSym :  material,rta,solver -> kappa_mode
database :  database_material -> rta
kappa_mode_3D :  material,rta,solver -> kappa_mode
plot_kappa_mode :  kappa_mode -> plot_kappa_mode
suppression :  solver,material,options_suppression -> suppression
plot_suppression :  suppression -> plot_suppression
plot_angular_suppression :  suppression -> plot_angular_suppression
vtu :  material,solver,geometry,options_vtu -> vtu
plot_results :  solver,geometry,material,options_maps -> plot_results
 
PIPELINES
kappa2DSym :  database -> rta2DSym -> geometry -> first_guess -> solve_rta -> kappa_mode_2DSym
kappa3D :  almabte2openbte -> rta3D -> geometry -> first_guess -> solve_rta -> kappa_mode_3D
kappa2dGray :  gray2D -> geometry -> first_guess -> solve_rta
```


Then, for convenience we use one of the proposed pipelines

```python
from efunx import get


init_data = {'options_geometry'   :         {'lx':10,'porosity':0.1,'step':2,'lz':0},\
             'database_material'  :         'rta_Si_300'}

data = get('kappa_mode',workflow='kappa2DSym',debug=True)(**init_data)
```


```bash
WORKFLOW database -> rta2DSym -> geometry -> first_guess -> solve_rta -> kappa_mode_2DSym
RUN  database
RUN  rta2DSym
RUN  geometry
RUN  first_guess
RUN  solve_rta

      Iter    Thermal Conductivity [W/m/K]      Error 
 -----------------------------------------------------------
       1               1.7203E+01             6.0141E+00
       2               1.0912E+01             5.7644E-01
       3               1.2789E+01             1.4673E-01
       4               1.1965E+01             6.8898E-02
       5               1.2192E+01             1.8674E-02
       6               1.2081E+01             9.1976E-03
       7               1.2107E+01             2.1654E-03
       8               1.2092E+01             1.2864E-03
       9               1.2094E+01             2.2294E-04
 -----------------------------------------------------------
RUN  kappa_mode_2DSym
```

## Author

Giuseppe Romano (romanog@mit.edu)













