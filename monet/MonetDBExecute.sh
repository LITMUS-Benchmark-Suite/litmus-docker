#!/bin/bash

##
# Script to run  a Query on MoneDB
#

#Settings
export RDF_Engine=/usr/local/bin/

# Input Parameters
#setParamsGetQuery
DB_location = $1; #path where the dataset is located
DB_name=$2; #Graph or database to access
QUERIES_location  = $3; #Path where the benchmark of queries is located
RESULT_file=$4;#Filename where the query output will be  stored

# USERNAME INTO .monetdb
#getQuery & setParamsAlign
for i in `ls $QUERIES_location/*.sql`; do
    export BASEN=`basename $i .sql`;
    sh -c "sync ; echo 3 > /proc/sys/vm/drop_caches";
    echo "------- FLUSHING CACHE -------" >> $RESULT_file;
    echo $BASEN;
    for k in `seq $5`; do
        echo $k;
    date;
    echo $BASEN >> $RESULT_file;
    echo $k >> $RESULT_file;
# execute
   time ($RDF_Engine/mclient -lsql -d$DB_location/$DB_name -s"$i") > /dev/null 2>> $RESULT_file;
   
done
