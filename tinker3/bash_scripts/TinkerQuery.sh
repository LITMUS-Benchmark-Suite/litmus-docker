#This script is to run queries on a graph stored in an XML format, in a Sparksee Database
#The first argument is the number of times which we want to sample the process
#The second argument is the location of the properties file.
#The third argument corresponds to the location of the log file
#The fourth argument corresponds to the location of the gremlin groovy file

#All the queries have to be written in the SparkseeQuery.groovy file itself.

/gremlin-groovy-3/bin/gremlin.sh -e $4 $2 $1 >> $3
# Example Run
# ./TinkerQuery.sh 5 ./HelloWorld.gdb ../../gremlin-groovy/data/graph-example-2.xml logs.txt

