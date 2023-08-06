'''
IDE

Custom ide for usefulpy.
This IDE allows you to access previous inputs and outputs easily.
This IDE also gives access to entire usefulpy library.

Most important functions:
   ide: start ide

LICENSE PLATAFORMS and INSTALLATION:
This is a section of usefulpy. See usefulpy.__init__ and usefulpy license
file

RELEASE NOTES:
0
 0.0
  Version 0.0.0:
   Custom ide for usefulpy.
'''

__version__ = '0.0.0'
__author__ = 'Augustin Garcia'

from . import usefulpy_syntax
from .namespace_management import usefulpy_namespace_globals
#import time
import traceback

def _output(object, count):
    if object is None: return
    print(f'Out[{count}] : ', repr(object), sep = '')
    print()

def _input(count):
    input_ = input(f'In [{count}] : ').rstrip()
    while not input_:
        print()
        input_ = input(f'In [{count}] : ').rstrip()
    if input_.endswith(':'):
        empty = ' '*(len(str(count))+3)+'-- : '
        next_line = input(empty).rstrip()
        while next_line:
            input_+= '\n'+next_line
            next_line = input(empty).rstrip()
    return input_
    

def _quit():
    ide.quit = True

def ide(namespace = None):
    ide.quit = False
    if namespace is None: namespace = {}
    namespace = {**namespace, **usefulpy_namespace_globals}
    original = namespace.copy()
    In = []
    Out = {}
    addedOuts = {}
    if 'In' not in namespace: namespace['In'] = In
    if 'Out' not in namespace: namespace['Out'] = Out
    namespace['quit'] = _quit
    count = 0
    while not ide.quit:
        try:
            input_ = _input(count)
            
            corrected_input = usefulpy_syntax._usefulpy_correct_syntax(input_, namespace['__defaults__']['#a'])
            try:
                try:
                    old_1 = namespace['_']
                    old__1 = namespace['__']
                except: pass

                output = eval(corrected_input, namespace)
                print()
                if output is None: count += 1; In.append(input_); continue
                _output(output, count)
                Out[count] = output
                namespace[f'_{count}'] = output
                addedOuts[f'_{count}'] = output
                try:
                    namespace['_'] = output
                    namespace['__'] = old_1
                    namespace['___'] = old__1
                except: pass
                In.append(input_)
                count += 1
                continue
            except: pass
            try:
                exec(corrected_input, namespace)
                print()
            except BaseException as err:
                print()
                traceback.print_exc() ##raise seperately later
                Out[count] = err
                namespace[f'_{count}'] = err
                addedOuts[f'_{count}'] = err
                print()
            In.append(input_)
            count += 1
            continue
        except:
            print()
            traceback.print_exc()
            print()
    usefulpy_syntax.namespace_management.keep_unique(namespace, original)
    usefulpy_syntax.namespace_management.keep_unique(namespace, addedOuts)
    try:
        del namespace['_']
        del namespace['__']
        del namespace['___']
    except: pass
    del namespace['In']
    del namespace['Out']
    del namespace['quit']
    return namespace

ide.quit = False

if __name__ == '__main__':
    ide()
