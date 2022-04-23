#!/usr/bin/env python3
print(f"\n===== Running {__file__} =====\n")
import sys
import os
import inspect
import builtins
import types
import pkgutil

def main():
    if os.path.islink(sys.executable):
        realpath = os.path.realpath(sys.executable)
        symlink = os.path.relpath(realpath, os.path.dirname(sys.executable))
        exec_path = f"{sys.executable} -> {symlink}"
    else:
        exec_path = sys.executable
    print(f"Python executable : {exec_path}")
    print(sys.version)
    print(f"Version [major={sys.version_info.major}, minor={sys.version_info.minor}, micro={sys.version_info.micro}]")
    print()


    print("Imports")
    # sys and builtins are built in modules so they have no path
    print("os module :", os.__file__)
    print("inspect   :", inspect.__file__)
    print("types     :", types.__file__)
    print("pkgutil   :", pkgutil.__file__)
    print()
    
    print("PATH : ")
    print("\t"+"\n\t".join(os.environ["PATH"].split(":")))
    print()
    
    print("PYTHONPATH : ")
    print("\t"+"\n\t".join(sys.path))
    print()

    #builtin_functions = []
    #builtin_constants = []
    #builtin_types = []
    #builtin_exceptions = []
    #other = []
    #for name, obj in builtins.__dict__.items():
    #    if isinstance(obj, types.BuiltinFunctionType):
    #        builtin_functions.append(name)
    #    elif inspect.isclass(obj) and issubclass(obj, BaseException):
    #        builtin_exceptions.append(name)
    #    elif not isinstance(obj, type):
    #        builtin_constants.append(name)
    #    else:
    #        other.append(name)

    #print("Built-in functions: ")
    #print_as_table(builtin_functions)
    #print()

    #print("Built-in exceptions: ")
    #print_as_table(builtin_exceptions)
    #print()
    #
    #print("Built-in non-types (e.g. constants): ")
    #print_as_table(builtin_constants)
    #print()
    #
    #print("Other built-in types: ")
    #print_as_table(other)
    #print()
    #
    #print("Built-in modules: ")
    #print_as_table(sys.builtin_module_names)
    #print()

    #print("Types in \"types\" module")
    #print_as_table([name for name, obj in types.__dict__.items() if isinstance(obj, type)])
    #print()
    #
    ##for tname, tclass in types.__dict__.items():
    ##    if not tname.endswith("Type"):
    ##        continue
    ##    b = [bname for bname, bobj in builtins.__dict__.items() if isinstance(bobj, tclass)]
    ##    print(f"\n{tname} type builtins")
    ##    if not b: continue
    ##    print_as_table(b)
    ##print()

    #print("All non-builtin importable modules: ")
    #from collections import defaultdict
    #modules = defaultdict(lambda : defaultdict(list))
    #for loader, mod_name, ispkg in pkgutil.iter_modules():
    #    modules[loader.path][ispkg].append(mod_name)
    #for path, d1 in modules.items():
    #    print(f">> Path = {path}")
    #    for ispkg, mods in d1.items():
    #        print(f"\t[IsPkg = {ispkg}]")
    #        print_as_table(mods)
    #    print()
    #print()

    ############################################################################
    # Exploring a package from the command line
    ############################################################################
    # help()
    # dir() - dump list of attributes
    # class.__subclasses__()





import math
def print_as_table(ls, n_cols = 0, fill_col_first = True):
    buff = len(max(ls, key=len)) + 1

    if not n_cols:
        # n_cols defaults to max allowed by window width
        window_width = int(os.popen('stty size', 'r').read().split()[1])
        n_cols = window_width // buff
    
    n_rows = math.ceil(len(ls) / n_cols)

    # Build table as 2D list
    table = [[' '*buff]*n_cols for i in range(n_rows)]
    irow = icol = 0;
    for ii, x in enumerate(ls):
        # Increment major axis
        if fill_col_first and ii>0 and ii % n_rows == 0:
            icol += 1;
            irow = 0
        elif not fill_col_first and ii>0 and ii % n_cols == 0:
            irow += 1;
            icol = 0

        # Fill
        table[irow][icol] = f"{x:{buff}}"

        # Increment minor axis
        if fill_col_first:
            irow += 1
        else:
            icol += 1

    
    for ii in range(n_rows):
        for jj in range(n_cols):
            print(f"{table[ii][jj]:{buff}}", end="")
        print()

if __name__ == "__main__":
    main()
