#!/bin/bash

##
# Script to run  a Query on ARQ 
#

#Settings
export RDF_Engine=/experiment/arq/bin
export PATH=$PATH:$RDF_Engine/bin:$RDF_Engine/lib

# Input Parameters
#setParamsGetQuery
DB_location = $1; #path where local dataset is located
DB_name=$2; #Graph or local database to access
QUERIES_location  = $3; #Path where the benchmark of queries is located
RESULT_file=$4;#Filename where the query output will be  stored

#getQuery & setParamsAlign
for i in `ls $QUERIES_location/*.sparql`; do
    export BASEN=`basename $i .sparql`;
    echo $BASEN;
    date;
    echo $BASEN >> $ARCHIVO;
    (time $RDF_Engine/arq  --data $DB_location/$DB_name -repeat=1 --time --query $i) > /dev/null 2>> $RESULT_file;
done

