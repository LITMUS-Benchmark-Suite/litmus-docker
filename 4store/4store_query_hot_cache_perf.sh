#The first argument is the name of the db
#The second argument is the location of the query file
#The third argument is the location of the result file
query=`less $2`
#echo "'$query'"
/usr/bin/time -a -o $3 -f "%S\t%U\t%e" 4s-query --soft-limit -1 $1 "$query" > /dev/null 2> /dev/null

