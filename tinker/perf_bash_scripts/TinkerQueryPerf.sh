#This script is to run queries on a graph stored in an XML format, in a Sparksee Database
#The first argument is the location where we want to create a db.
#The second argument is the location of the XML file
#The third argument corresponds to the location of the log file
#The fourth argument corresponds to the location of the gremlin groovy file

#All the queries have to be written in the SparkseeQuery.groovy file itself.

/gremlin-groovy/bin/gremlin.sh -e $4 $1 $2 >> $3

