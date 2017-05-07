#!/bin/bash

##
# Script to load a dataset in JenaTDB
export Jena_Engine=/apache-jena-3.2.0/bin
export PATH=$PATH:$Jena_Engine/bin:$Jena_Engine/lib

DB_location=$1; #path where the dataset is located
DB_name=$2; #Datagraph 
Dataset_name=$3; #Input Dataset 
RESULT_file=$4;#Filename where the output of the loading process will be stored

#load
#/usr/bin/time -a -o $RESULT_file -f "%S\t%U\t%e" /apache-jena-3.2.0/bin/tdbloader --verbose --loc=$DB_location/$DB_name $Dataset_name > /dev/null 2>> /dev/null;

/usr/bin/time -a -o $RESULT_file -f "%S\t%U\t%e" /apache-jena-3.2.0/bin/tdbloader2 --loc=$DB_location/$DB_name $Dataset_name

