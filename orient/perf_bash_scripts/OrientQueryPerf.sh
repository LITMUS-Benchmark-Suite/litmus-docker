#This script is to run queries on a graph stored in an XML format, in a Sparksee Database
#The first argument is the location of the database
#The second argument is the location of the groovy script
#The third argument corresponds to the location of the log file

#All the queries have to be written in the OrientQuery.groovy file itself.

cd /orientdb/bin && ./gremlin.sh -e  $2\ $1>> $3

