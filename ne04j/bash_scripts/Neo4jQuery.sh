#This script is to run queries on a graph stored in an XML format, in a Neo4j Database
#The first argument is the number of times which we want to sample the process
#The second argument is the location where we want to create a db.
#The third argument is the location of the XML file
#The fourth argument corresponds to the location of the log file

#All the queries have to be written in the SparkseeQuery.groovy file itself.

../../gremlin-groovy/bin/gremlin.sh -e ../groovy_scripts/Neo4jQuery.groovy $2 $3 $1 >> $4

# Example Run
# ./Neo4j.sh 5 ./HelloWorld.gdb ../../gremlin-groovy/data/graph-example-2.xml logs.txt

