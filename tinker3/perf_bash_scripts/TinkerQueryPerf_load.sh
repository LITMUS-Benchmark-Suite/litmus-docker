#This script is to load a graph stored in an XML format, in a Sparksee Database
#The first argument is the location of the property file.
#The second argument is the location of the Graphml file
#The third argument corresponds to the location of the log file

/gremlin-groovy-3/bin/gremlin.sh -e /scripts/tinker3/TinkerQueryPerf_load.groovy $1 $2 >> $3;


