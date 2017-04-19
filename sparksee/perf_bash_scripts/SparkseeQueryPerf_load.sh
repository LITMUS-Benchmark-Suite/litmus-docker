#This script is to load a graph stored in an XML format, in a Sparksee Database
#The first argument is the location where we want to create a db.
#The second argument is the location of the XML file

/gremlin-groovy/bin/gremlin.sh -e /scripts/sparksee/SparkseeQueryPerf_load.groovy $1 $2
