#This script is to run queries on a graph stored in an XML format, in a Sparksee Database
#The second argument corresponds to the location of the log file
#The first argument corresponds to the location of the gremlin groovy file

#All the queries have to be written in the SparkseeQuery.groovy file itself.

/gremlin-groovy/bin/gremlin.sh -e $1 >> $2
