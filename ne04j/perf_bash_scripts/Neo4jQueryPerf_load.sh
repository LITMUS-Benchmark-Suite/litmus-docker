#This script is to load a graph stored in an XML format, in a Neo4j Database
#The first argument is the location where we want to create a db.
#The second argument is the location of the XML file
#The third argument corresponds to the location of the log file

#/gremlin-groovy/bin/gremlin.sh -e /scripts/neo4j/Neo4jQueryPerf_load.groovy $1 $2 >> $3
/gremlin-groovy/bin/gremlin.sh -e /scripts/neo4j/Neo4jQueryPerf_load.groovy $1 $2 >> $3
