#!/bin/bash
#Settings
export RDF_Engine=/experiment/rdf3x/bin

#setParamsGetQuery
DB_location = $1; #path where the dataset is located
DB_name=$2; #Datagraph 
Dataset_name=$3; #Input Dataset 
RESULT_file=$4;#Filename where the output of the loading process will be stored

#load
time ($RDF_Engine/rdf3xload $DB_location/$DB_name $DB_location/$Dataset_name) > /dev/null 2>> $RESULT_file;
