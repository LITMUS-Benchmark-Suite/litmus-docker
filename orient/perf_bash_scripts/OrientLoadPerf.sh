#This script is to load a graph stored in an XML format, in a Sparksee Database
#The first argument is the name of the database in the memory
#The second argument corresponds to the location of the graphml file.
#The third argument corresponds to the location of the groovy script.
#The fourth argument corresponds to the location of the log file

cd /orientdb/bin && ./gremlin.sh -e  $3\ $1\ $2>> $4

# Example Run
#./OrientLoad.sh demo /home/yashwant/BTP/dms-scripts/utilities/out1.ml /home/yashwant/BTP/dms-scripts/orient/groovy_scripts/OrientLoad.groovy /home/yashwant/logs.txt
