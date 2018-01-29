POLAR - Path Of LeAst Resistance - (Work in progress.....)

Introduction
While performing binary analysis of a firmware, I had a scenario where multiple executables were compiled against multiple libraries.
I was looking for a graphical view to understand the relationships between imported and exported symbols and it's usages. 
I didn't find anything that suits my needs. As such, I wrote a very simple parser, which can be useful for other people with the same needs.
The flow is simple:
- Using radare2, generate a list of imported exported symbols
- Parse and insert them into a neo4j graph database.
- If needed, decompile all the usages of a specific symbol, parse the calls and insert them to the graph.


Requirements:
neo4j graph database - https://github.com/neo4j/neo4j
neomodel - pip install neomodel
r2pipe - pip install r2pipe


Usage:
To parse the imports/exports
get_import_export_radare('filename','/path/to/filename')
To decompile a function
getdisassemble_to_function('name_of_the_symbol','filename','/path/to/filename')




Acknowledgements.
Big thanks to Inbar Raz for the support and convincing me to share my simple parser, and to @shiftred and @iiamit for feedback.
