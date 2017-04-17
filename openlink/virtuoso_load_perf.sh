

Virtuoso_isql=$1;
Result_file=$2;

$Virtuoso_isql 1111 dba dba /scripts/virtuoso/prepare.sql> /dev/null 2>> /dev/null;
/usr/bin/time -a -o $Result_file -f "%S\t%U\t%e" $Virtuoso_isql 1111 dba dba /scripts/virtuoso/load.sql> /dev/null 2>> /dev/null;
$Virtuoso_isql 1111 dba dba /scripts/virtuoso/clear.sql> /dev/null 2>> /dev/null;
