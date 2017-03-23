Virtuoso_isql=$1;
Result_file=$2;
Query_location=$3;

$Virtuoso_isql 1111 dba dba clear.sql> /dev/null 2>> /dev/null;
$Virtuoso_isql 1111 dba dba prepare.sql> /dev/null 2>> /dev/null;
$Virtuoso_isql 1111 dba dba load.sql> /dev/null 2>> /dev/null;


for i in `ls $Query_location/*.sparql`; do
    export BASEN=`basename $i .sparql`;

    echo "***********" >> $RESULT_FILE;
    echo $BASEN >> $RESULT_file;    
    #echo "------- FLUSHING CACHE -------" >> $RESULT_file;
    echo $BASEN;
    for k in `seq $4`; do
        sh -c "sync ; echo 3 > /proc/sys/vm/drop_caches";        
        echo $k;
        #echo $k >> $RESULT_file;
        # execute
        /usr/bin/time -a -o $RESULT_file -f "%S\t%U\t%e" $Virtuoso_isql 1111 dba dba $i> /dev/null 2>> /dev/null;
    done
done
