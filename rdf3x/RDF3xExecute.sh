#!/bin/bash

##
# Script to run  a Query on RDF3X 
#

#Settings
export RDF_Engine=/experiment/rdf3x/bin

# Input Parameters
#setParamsGetQuery
DB_location = $1; #path where the dataset is located
DB_name=$2; #Graph or database to access
QUERIES_location  = $3; #Path where the benchmark of queries is located
RESULT_file=$4;#Filename where the query output will be  stored

#getQuery & setParamsAlign
for i in `ls $QUERIES_location/*.sparql`; do
    export BASEN=`basename $i .sparql`;
    sh -c "sync ; echo 3 > /proc/sys/vm/drop_caches";
    echo "------- FLUSHING CACHE -------" >> $RESULT_file;
    echo $BASEN;
    for k in `seq $5`; do
        echo $k;
    date;
    echo $BASEN >> $RESULT_file;
    echo $k >> $RESULT_file;
# execute
    time ($RDF_Engine/rdf3xquery $DB_location/$DB_name $i) > /dev/null 2>> $RESULT_file;

done