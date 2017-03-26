#!/bin/bash

##
# Script to load a dataset in JenaTDB

#Settings
export Jena_Engine=/apache-jena-3.2.0/bin
export PATH=$PATH:$Jena_Engine/bin:$Jena_Engine/lib

# Input Parameters
#setParamsGetQuery
DB_location=$1; #path where the dataset is located
DB_name=$2; #Datagraph 
Dataset_name=$3; #Input Dataset 
RESULT_file=$4;#Filename where the output of the loading process will be stored

#load
for i in $(seq 1 1 $5)
do
    sh -c "sync ; echo 3 > /proc/sys/vm/drop_caches";
    /usr/bin/time -a -o $RESULT_file -f "%S\t%U\t%e" $Jena_Engine/tdbloader --verbose --loc=$DB_location/$DB_name $Dataset_name /dev/null 2>> /dev/null;
done
