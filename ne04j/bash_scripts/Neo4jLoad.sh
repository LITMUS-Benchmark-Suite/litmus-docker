#This script is to load a graph stored in an XML format, in a Neo4j Database
#The first argument is the number of times which we want to sample the process
#The second argument is the location where we want to create a db.
#The third argument is the location of the XML file
#The fourth argument corresponds to the location of the log file

for i in $(seq 1 1 $1)
do
    sh -c "sync ; echo 3 > /proc/sys/vm/drop_caches";
	echo "Run Number:$i"
#	echo "Run Number:$i" >> $4
	/gremlin-groovy/bin/gremlin.sh -e /scripts/neo4j/Neo4jLoad.groovy $2 $3 >> $4
done

# Example Run
# ./Neo4jLoad.sh 5 ./HelloWorld.gdb ../../gremlin-groovy/data/graph-example-2.xml logs.txt

