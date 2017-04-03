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
Dataset_name=$3; #Input Dataset 
QUERIES_location=$4; #Path where the benchmark of queries is located
RESULT_FILE=$5; #Filename where the query output will be  stored
NO_OF_RUNS=$6;

#Loading the database
$RDF_Engine/rdf3xload $DB_location/$DB_name $Dataset_name 
echo "Inside RDF Execute";
#getQuery & setParamsAlign
for i in `ls $QUERIES_location/*.sparql`; do
    export BASEN=`basename $i .sparql`;

    echo "***********" >> $RESULT_FILE;
    echo $BASEN >> $RESULT_FILE;    
    #echo "------- FLUSHING CACHE -------" >> $RESULT_file;
    echo $BASEN;
    
    for k in `seq $6`; do
        sync ; 
        echo $k;
        #echo $k >> $RESULT_file;
        # execute
        /usr/bin/time -a -o $RESULT_FILE -f "%S\t%U\t%e" $RDF_Engine/rdf3xquery $DB_location/$DB_name $i > /dev/null 2>> /dev/null;
    done
done
