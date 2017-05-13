#!/bin/bash

##
# Script to run  a Query on JenaTDB 
#

#Settings
export Jena_Engine=/apache-jena-3.2.0/bin
export PATH=$PATH:$Jena_Engine/bin:$Jena_Engine/lib

# Input Parameters
#setParamsGetQuery
DB_location=$1; #path where the dataset is located
DB_name=$2; #Graph or database to access
RESULT_file=$3;#Filename where the query output will be  stored
SPARQL_FILE=$4;

#/usr/bin/time -a -o $RESULT_file -f "%S\t%U\t%e" $Jena_Engine/tdbquery --time --loc=$DB_location/$DB_name --file=$SPARQL_FILE > /jena_hot_cache_result 2> /jena_hot_cache;
/usr/bin/time -a -o $RESULT_file -f "%S\t%U\t%e" $Jena_Engine/tdbquery --time --loc=$DB_location/$DB_name --file=$SPARQL_FILE  2> /jena_hot_cache;
