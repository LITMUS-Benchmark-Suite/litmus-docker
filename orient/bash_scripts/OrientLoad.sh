#This script is to load a graph stored in an XML format, in a Sparksee Database
#The first argument is the number of times which we want to sample the process
#The second argument is the name of the database in the memory
#The third argument corresponds to the location of the GraphML File.
#The fourth argument corresponds to the location of the groovy script.
#The fifth argument corresponds to the location of the log file


for i in $(seq 1 1 $1)
do
    sh -c "sync ; echo 3 > /proc/sys/vm/drop_caches";
	echo "Run Number:$i"
#	echo "Run Number:$i" >> $5

	cd /orientdb/bin && sudo ./gremlin.sh -e  $4\ $2\ $3>> $5
done

# Example Run
#./OrientLoad.sh 5 demo /home/yashwant/BTP/dms-scripts/utilities/out1.ml /home/yashwant/BTP/dms-scripts/orient/groovy_scripts/OrientLoad.groovy /home/yashwant/logs.txt
