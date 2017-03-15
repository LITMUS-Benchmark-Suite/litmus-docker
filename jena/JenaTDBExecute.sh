#!/bin/bash

##
# Script to run  a Query on JenaTDB 
#

#Settings
export RDF_Engine=/experiment/jenatdb/bin
export PATH=$PATH:$RDF_Engine/bin:$RDF_Engine/lib

# Input Parameters
#setParamsGetQuery
DB_location = $1; #path where the dataset is located
DB_name=$2; #Graph or database to access
QUERIES_location  = $3; #Path where the benchmark of queries is located
RESULT_file=$4;#Filename where the query output will be  stored

#getQuery & setParamsAlign
for i in `ls $QUERIES_location/*.sparql`; do
    export BASEN=`basename $i .sparql`;
    echo $BASEN;
    date;
    echo $BASEN >> $RESULT_file;
    (time $RDF_Engine/tdbquery --loc=$DB_location/$DB_name --file=$i --time) > /dev/null 2>> $RESULT_file;
done

