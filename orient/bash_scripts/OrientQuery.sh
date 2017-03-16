#This script is to run queries on a graph stored in an XML format, in a Sparksee Database
#The first argument is the number of times which we want to sample the process
#The second argument is the location of the database
#The third argument is the location of the GraphML file
#The fourth argument is the location of the groovy script
#The fifth argument corresponds to the location of the log file

#All the queries have to be written in the OrientQuery.groovy file itself.

cd /orientdb/bin && sudo ./gremlin.sh -e  $4\ $2\ $3\ $1 >> $5

