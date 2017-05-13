# The first argument is the name of the db
# The second argument is the location of the northwind file
# The third argument is the location of the result file
/usr/bin/time -a -o $3 -f "%S\t%U\t%e" 4s-import $1 --format ntriples $2 > /dev/null 2> /dev/null
