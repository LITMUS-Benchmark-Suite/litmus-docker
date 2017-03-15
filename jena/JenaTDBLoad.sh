#!/bin/bash

##
# Script to load a dataset in JenaTDB

#Settings
export RDF_Engine=/experiment/jenatdb/bin
export PATH=$PATH:$RDF_Engine/bin:$RDF_Engine/lib

# Input Parameters
#setParamsGetQuery
DB_location = $1; #path where the dataset is located
DB_name=$2; #Datagraph 
Dataset_name=$3; #Input Dataset 
RESULT_file=$4;#Filename where the output of the loading process will be stored

#load
time ($RDF_Engine/tdbloader --verbose --loc=$DB_location/$DB_name $Dataset_name) /dev/null 2>> $RESULT_file;
