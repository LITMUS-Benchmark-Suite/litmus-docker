#!/bin/bash

##
# Script to run  a Query on RDF3X 
#

#Settings
export RDF_Engine=/gh-rdf3x/bin

# Input Parameters
#setParamsGetQuery
DB_location=$1; #path where the dataset is located
DB_name=$2; #Graph or database to access
RESULT_FILE=$3; #Filename where the query output will be  stored
SPARQL_FILE=$4;

/usr/bin/time -a -o $RESULT_FILE -f "%S\t%U\t%e" $RDF_Engine/rdf3xquery $DB_location/$DB_name $SPARQL_FILE > /dev/null 2>> /dev/null;
