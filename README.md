# POLAR - Path Of LeAst Resistance - (Work in progress.....)

## Introduction
While performing binary analysis of a firmware, I had a scenario where multiple executables were compiled against multiple libraries.
I was looking for a graphical view to understand the relationships between imported and exported symbols and it's usages. 
I didn't find anything that suits my needs. As such, I wrote a very simple parser, which can be useful for other people with the same needs.
The flow is simple:
- Using radare2, generate a list of imported exported symbols
- Parse and insert them into a neo4j graph database.
- If needed, decompile all the usages of a specific symbol, parse the calls and insert them to the graph.
- python3

## Requirements:
- neo4j graph database - https://github.com/neo4j/neo4j
- neomodel - pip install neomodel
- r2pipe - pip install r2pipe


## Usage:
- To parse the imports/exports
-- get_import_export_radare('filename','/path/to/filename')
- To decompile a function
-- getdisassemble_to_function('name_of_the_symbol','filename','/path/to/filename')




## Acknowledgements.

Big thanks to @inbarraz for the support and convincing me to share my simple parser, and to @shiftred and @iiamit for feedback.



## Example usage

### Simple Command Injection Example
1) Download an old firmware version for a known vulnerable router, for example:
https://www.netgear.com/support/product/R7000#Firmware%20Version%201.0.0.96%20(North%20America%20Only)
2) Mount the squashfs image.
3) Run Polar over the lib, sbin, usr


```from os import listdir
from os.path import isfile, join, islink
directories = ['/_R7000-V1.0.0.96_1.0.15.chk.extracted/squashfs-root/lib/' ,'/_R7000-V1.0.0.96_1.0.15.chk.extracted/squashfs-root/sbin/' ,'/_R7000-V1.0.0.96_1.0.15.chk.extracted/squashfs-root/usr/bin/' , '/_R7000-V1.0.0.96_1.0.15.chk.extracted/squashfs-root/usr/lib/', '/_R7000-V1.0.0.96_1.0.15.chk.extracted/squashfs-root/usr/sbin/']
for directory in directories:
	onlyfiles = [f for f in listdir(directory) if isfile(join(directory, f)) and not islink(join(directory, f))]
	for file in onlyfiles:
	     get_import_export_radare(file,directory+file)
```
4) Identify which files are calling to system, using a cyperQL query:

`MATCH p = (n:Symbol{name:'system'})-[r:uses]-() RETURN p`

![Alt text](screenshots/Screenshot1.png?raw=true "Screenshot 1")
5) Decompile all the calls to system from the file httpd (for example):

`getdisassemble_to_function('system','acos_service','/_R7000-V1.0.0.96_1.0.15.chk.extracted/squashfs-root/usr/sbin/httpd')`

6) Make a cypherql query and expand the node:

`MATCH p=(File{name:'httpd'})-[r:defines]->() RETURN p`

![Alt text](screenshots/Screenshot2.png?raw=true "Screenshot 2")
7) Take a look at the decompile and profit :-)
![Alt text](screenshots/Screenshot3.png?raw=true "Screenshot 3")
8) Or do complex queries, for example, whenever you have sprintf and system:

`MATCH p=(File{name:'httpd'})-[r:defines]->()<-[q:imports]-(Symbol{name:'sprintf'}) return p limit 100`

![Alt text](screenshots/Screenshot4.png?raw=true "Screenshot 4")