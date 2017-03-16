#!/bin/bash

##
# Script to run  a Query on JenaTDB 
#

#Settings
export Jena_Engine=/jenatdb/bin
export PATH=$PATH:$Jena_Engine/bin:$Jena_Engine/lib

# Input Parameters
#setParamsGetQuery
DB_location=$1; #path where the dataset is located
DB_name=$2; #Graph or database to access
Dataset_name=$3;
QUERIES_location=$4; #Path where the benchmark of queries is located
RESULT_file=$5;#Filename where the query output will be  stored

$Jena_Engine/tdbloader --verbose --loc=$DB_location/$DB_name $Dataset_name

#getQuery & setParamsAlign
for i in `ls $QUERIES_location/*.sparql`; do
    for j in $(seq 1 1 $6)
    do
        sh -c "sync ; echo 3 > /proc/sys/vm/drop_caches";
        export BASEN=`basename $i .sparql`;
        echo $BASEN;
        date;
        echo $BASEN >> $RESULT_file;
        (time $Jena_Engine/tdbquery --loc=$DB_location/$DB_name --file=$i --time) > /dev/null 2>> $RESULT_file;
    done
done

