#The first argument is the name of the database.

4s-backend-setup --node 0 --cluster 1 --segments 4 $1
4s-backend $1

