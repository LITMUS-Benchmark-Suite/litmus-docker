#!/bin/bash
#Settings
export RDF_Engine=/gh-rdf3x/bin

#setParamsGetQuery
runs=$1;
DB_location=$2; #path where the dataset is located
DB_name=$3; #Datagraph 
Dataset_name=$4; #Input Dataset 
RESULT_file=$5;#Filename where the output of the loading process will be stored

echo "Inside RDF LOAD";
#load
for i in $(seq 1 1 $1)
do
    sync ; 
    echo 3 > /proc/sys/vm/drop_caches;
    /usr/bin/time -a -o $RESULT_file -f "%S\t%U\t%e" $RDF_Engine/rdf3xload $DB_location/$DB_name $Dataset_name > /dev/null 2>> /dev/null;
done
