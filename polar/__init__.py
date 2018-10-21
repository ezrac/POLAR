<<<<<<< HEAD:polar/__init__.py
import re
import os
import sys
from os import path
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

# Radare 2 bindings in python
import r2pipe

# This is the DATABASE URL for the visualization
from neomodel import config
from neomodel import StringProperty, RelationshipTo, StructuredNode, RelationshipFrom

__version__ = 0.1


# Define an Object that stores the Symbol Properties.
# A symbol can either be Used, Provided or Imported.

class Symbol(StructuredNode):
    name = StringProperty(required=True)
    user = RelationshipFrom('File', 'uses')
    provider = RelationshipFrom('File', 'provides')


# Define an Object that stores the File Properties.
# A file has a path, hash, name and can use or provide symbols
class File(StructuredNode):
    name = StringProperty(unique_index=True)
    path = StringProperty()
    hash = StringProperty()
    uses = RelationshipTo('Symbol', 'uses')
    provides = RelationshipTo('Symbol', 'provides')


# Every function should have a name, and it's defined at a specific File
# A function includes (as a property) the decompilation (optionally)
class Function(StructuredNode):
    name = StringProperty(required=True)
    decompilation = StringProperty()
    imports_symbol = RelationshipFrom('Symbol', 'imports')
    defined_at = RelationshipFrom('File', 'defines')


# First parameter is the filename (the string that is stored, second argument is the path)
# Were we will perform the activities

def get_import_export_radare(filename, path):
    # We define the node or get it if already exists, for further operations.
    filenode = File.get_or_create({'name': filename})[0]
    # By using r2, we open the file
    r2 = r2pipe.open(path)
    # And *a*nalyze the *f*unctions
    r2.cmd('af')
    # and get *i*nformation, on the *i*mports in a *j*son format
    # parsing it with the json parser ( cmdj )
    imports = r2.cmdj('iij')
    # get *i*nformation, on the *e*xports in a *j*son format
    # parsing it with the json parser ( cmdj )
    exports = r2.cmdj('iEj')

    for symbolimport in imports:
        # Dirty hack....
        if not symbolimport['type'] == 'NOTYPE':
            # We define the node or get it if already exists, for further operations.
            importedsymbol = Symbol.get_or_create({'name': symbolimport['name']})[0]
            # We create a user relationship on the file we defined previously
            importedsymbol.user.connect(filenode)

    for symbolexport in exports:
        # Dirty hack...
        if not symbolexport['size'] == 0:
            symbol = Symbol.get_or_create({'name': symbolexport['name']})[0]
            # We create a provider relationship on the file we defined previously
            symbol.provider.connect(filenode)


def getdisassemble_to_function(function_name, filename, path):
    filenode = File.get_or_create({'name': filename})[0]
    r2 = r2pipe.open(path)
    r2.cmd("aaa")
    # e anal.jmptbl = true
    # e anal.hasnext = true
    function_calls = r2.cmd("axt @@ " + function_name).split('\n')
    for call in function_calls:
        if "[call]" in call.split(" ")[2]:
            if "(nofunc)" in call.split(" ")[0]:
                dissasembly = r2.cmd("pd @ " + call.split(" ")[1] + " -10")
                re.findall("bl\s(?:sym\.imp|sub)\.(.+?)\\s", dissasembly)
            else:
                dissasembly = r2.cmd("pdf @@ " + call.split(" ")[0])
                re.findall("bl\s(?:sym\.imp|sub)\.(.+?)\\s", dissasembly)
                my_function = Function.get_or_create({'name': call.split(" ")[0], 'decompilation': dissasembly})[0]
                # filenode.defines.connect(function)
                for call in re.findall("bl\s(?:sym\.imp|sub)\.(.+?)\\s", dissasembly):
                    symbol = Symbol.get_or_create({'name': call})[0]
                    my_function.imports_symbol.connect(symbol)
                    my_function.defined_at.connect(filenode)


def parse(db_url, directories):
    config.DATABASE_URL = db_url
    for directory in directories:
        for dir_path, dir_names, file_names in os.walk(directory):
            for file_name in file_names:
                full_path = path.abspath(path.join(dir_path, file_name))
                get_import_export_radare(path.basename(full_path), full_path)


def parse_main(args=None):
    if args is None:
        args = sys.argv[1:]

    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-v", "--version", action="version", version="%(prog)s {ver}".format(ver=__version__))
    parser.add_argument("-db", "--neo4j-database",
                        help="neo4j database url",
                        dest="db_url",
                        default="bolt://neo4j:neo4j@localhost:7687")

    parser.add_argument("-d", "--directories",
                        help="Directory to parse",
                        required=True,
                        nargs='+')
    sys_args = vars(parser.parse_args(args=args))

    parse(**sys_args)


def disassemble(db_url, function_tuples):
    config.DATABASE_URL = db_url
    for function_tuple in function_tuples:
        function_name, file_path = function_tuple.rsplit(':', 1)
        full_path = path.abspath(file_path)
        getdisassemble_to_function(function_name, path.basename(full_path), full_path)


def disassemble_main(args=None):
    if args is None:
        args = sys.argv[1:]

    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-v", "--version", action="version", version="%(prog)s {ver}".format(ver=__version__))
    parser.add_argument("-db", "--neo4j-database",
                        help="neo4j database url",
                        dest="db_url",
                        default="bolt://neo4j:neo4j@localhost:7687")

    parser.add_argument("-f", "--function-tuples",
                        help="file:function tuples",
                        required=True,
                        nargs='+')
    sys_args = vars(parser.parse_args(args=args))

    disassemble(**sys_args)
=======
from neomodel import config
# This is the DATABASE URL for the visualization
config.DATABASE_URL = 'bolt://neo4j:neo4j@localhost:7687'
from neomodel import StringProperty, RelationshipTo, StructuredNode, RelationshipFrom
import re
# Radare 2 bindings in python
import r2pipe





# Define an Object that stores the Symbol Properties.
# A symbol can either be Used, Provided or Imported.

class Symbol(StructuredNode):
    name = StringProperty(required=True)
    user = RelationshipFrom('File', 'uses')
    provider = RelationshipFrom('File', 'provides')

# Define an Object that stores the File Properties.
# A file has a path, hash, name and can use or provide symbols
class File(StructuredNode):
    name = StringProperty(unique_index=True)
    path = StringProperty()
    hash = StringProperty()
    uses = RelationshipTo('Symbol', 'uses')
    provides = RelationshipTo('Symbol', 'provides')

# Every function should have a name, and it's defined at a specific File
# A function includes (as a property) the decompilation (optionally)
class Function(StructuredNode):
    name = StringProperty(required=True)
    decompilation = StringProperty()
    imports_symbol = RelationshipTo('Symbol','imports')
    defined_at = RelationshipFrom('File','defines')



# First parameter is the filename (the string that is stored, second argument is the path)
# Were we will perform the activities

def get_import_export_radare(filename, path):
    # We define the node or get it if already exists, for further operations.
    filenode = File.get_or_create({'name': filename})[0]
    # By using r2, we open the file
    r2 = r2pipe.open(path)
    # And *a*nalyze the *f*unctions
    r2.cmd('af')
    # and get *i*nformation, on the *i*mports in a *j*son format
    # parsing it with the json parser ( cmdj )
    imports = r2.cmdj('iij')
    # get *i*nformation, on the *e*xports in a *j*son format
    # parsing it with the json parser ( cmdj )
    exports = r2.cmdj('iEj')

    for symbolimport in imports:
        #Dirty hack....
        if not symbolimport['type'] == 'NOTYPE':
            # We define the node or get it if already exists, for further operations.
            importedsymbol = Symbol.get_or_create({'name': symbolimport['name']})[0]
            # We create a user relationship on the file we defined previously
            importedsymbol.user.connect(filenode)



    for symbolexport in exports:
        #Dirty hack...
        if not symbolexport['size'] == 0:
            symbol = Symbol.get_or_create({'name': symbolexport['name']})[0]
            # We create a provider relationship on the file we defined previously
            symbol.provider.connect(filenode)



def getdisassemble_to_function(function_name, filename, path):
    filenode = File.get_or_create({'name': filename})[0]
    r2 = r2pipe.open(path)
    r2.cmd("aaa")
    #e anal.jmptbl = true
    #e anal.hasnext = true
    function_calls = r2.cmd("axt @@ "+function_name).split('\n')
    for call in function_calls:
        if "[call]" in call.split(" ")[2]:
            if "(nofunc)" in call.split(" ")[0]:
                dissasembly = r2.cmd("pd @ " +call.split(" ")[1]+" -10")
                re.findall("bl\s(?:sym\.imp|sub)\.(.+?)\\s", dissasembly)
            else:
                dissasembly = r2.cmd("pdf @@ " + call.split(" ")[0])
                re.findall("bl\s(?:sym\.imp|sub)\.(.+?)\\s", dissasembly)
                my_function = Function.get_or_create({'name':call.split(" ")[0], 'decompilation': dissasembly})[0]
                # filenode.defines.connect(function)
                for call in re.findall("bl\s(?:sym\.imp|sub)\.(.+?)\\s", dissasembly):
                    symbol = Symbol.get_or_create({'name':call})[0]
                    my_function.imports_symbol.connect(symbol)
                    my_function.defined_at.connect(filenode)

>>>>>>> master:parser.py
