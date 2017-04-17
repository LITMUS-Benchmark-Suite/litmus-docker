#!/bin/bash
#Settings
export RDF_Engine=/gh-rdf3x/bin

#setParamsGetQuery
DB_location=$1; #path where the dataset is located
DB_name=$2; #Datagraph 
Dataset_name=$3; #Input Dataset 
RESULT_file=$4;#Filename where the output of the loading process will be stored

/usr/bin/time -a -o $RESULT_file -f "%S\t%U\t%e" $RDF_Engine/rdf3xload $DB_location/$DB_name $Dataset_name > /dev/null 2>> /dev/null;
