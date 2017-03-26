# Instructions

Please follow the following instruction before you build the docker.

## The RDF data files
Please keep all the rdf data files in the directory **rdf_data**. There should be only a single file in the directory.

## The graph data file
There should be a single graph data file which should be present in the directory **graph_data**. It should be in the **Graph_ML** format.

## The SPARQL queries
* All the SPARQL queries for the RDF based DMS should be kept in the **sparql_query** directory. 
* They should have a **.sparql** extension.

## The Gremlin queries
The gremlin queries should be kept in a single file in the **gremlin_query** directory and should have the name **gremlin.groovy**. An example file for the same has been included to help you out about how the query file should exactly look like.
The variable x is your Graph DMS object. And for each query you are supposed to write down the accompanying lines of codes. There are two example queries in the given file. The first query is from lines 1 to 6. The actual query is on line 5.

Once all these procedures have been followed, you can build the docker using the ```docker build``` command.

After the docker is successfully built, you have to run it using the ```docker run``` command.

Sanity checks have been added to make sure that there are no issues with the files, and the program will exit in case of an error.


