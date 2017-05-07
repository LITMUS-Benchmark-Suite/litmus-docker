Virtuoso_isql=$1;
RESULT_FILE=$2;
SPARQL_FILE=$3;
/usr/bin/time -a -o $RESULT_FILE -f "%S\t%U\t%e" $Virtuoso_isql 1111 dba dba $SPARQL_FILE> /dev/null 2>> /dev/null;

