# Instructions

Please follow the following instructions to setup and run Litmus Benchmark Suite.


## Step 1: The RDF data file
Please keep all the rdf data files in the directory **rdf_data**. There should be only a single file in the directory. The RDF data file should be in the **ntriples** format.

## Step 2: The graph data file
There should be a single graph data file which should be present in the directory **graph_data**. It should be in the **Graph_ML** format.

## Step 3: The SPARQL queries
* All the SPARQL queries for the RDF based DMS should be kept in the **sparql_query** directory. 
* Each query should have a **.sparql** extension.

## Step 4: The Gremlin queries
* All the Gremlin queries for the Graph based DMS should be kept in the **gremlin_query** directory. 
* They should have a **.gremlin** extension.
* The variable x is your Graph Traversal object. An example query to get a count of vertices would be saved in a file as, 
```bash
x.V().count()
```
## Step 5: Build the Docker

```bash
docker build -t litmus:local /path/of/the/repo
```

## Step 6 : Run the Docker

```bash
docker run --privileged litmus:local
```
We are using the _--privileged_ flag, because the we need root access to clear the cache.

## Step 7 : Run the benchmarking task

The benchmarking task is run using a Python script which can have various arguments. The name of the python script is **run_script.py**.
The following are the options and valid arguments
* -gd GRAPH\_DATAFILE, --graph\_datafile GRAPH\_DATAFILE : The directory where the graphml file has been kept. It would be **graph_data** if you have followed the instructions mentioned above.
* -rd RDF\_DATAFILE, --rdf\_datafile RDF\_DATAFILE : The directory where the ntriples file has been kept. It would be **rdf_data** if you have followed the instructions mentioned above.
* -gq GRAPH\_QUERIES, --graph\_queries GRAPH\_QUERIES : The location of all the gremlin queries. It would be **gremlin_query** if you have followed the instructions mentioned above.
* -rq RDF\_QUERIES, --rdf\_queries RDF\_QUERIES : The location of the SPARQL queries. It would be **sparql_query** if you have followed the instructions mentioned above.

* -v, --verbose : Verbose
* -a, --all : Run the benchmarking task for all the DMS.
* -g GRAPH, --graph GRAPH : Pass a string with the names of Graph Based DMS seperated by commas. (eg. "orient,sparksee,neo4j,tinker")
* -r RDF, --rdf RDF : Pass a string with the names of RDF Based DMS seperated by commas. (eg. "jena,4store,virtuoso,rdf3x")
* -ba BENCHMARK\_ACTIONS, --benchmark\_actions BENCHMARK\_ACTIONS :Pass a string with the actions to be carried out for benchmarking. ( Eg. "warm\_cache,cold\_cache,load" )
* -n RUNS, --runs RUNS : Number of times, the experiment should be conducted

## Step 8 : Generating the plots.
The plots are generated after the benchmarking task has been completed using the **plot_script.py** script.

The following are the arguments that can be passed.
* -pg PERF\_GRAPH, --perf\_graph PERF\_GRAPH : Pass the value **temp_graph.csv** if you want seperate plots for only the Graph Based DMSs for perf parameters.
* -pr PERF\_RDF, --perf\_rdf PERF\_RDF : Pass the value **temp_rdf.csv** if you want seperate plots for only the RDF Based DMSs for perf parameters.
* -cr COMBINED\_CSV, --combined\_csv COMBINED\_CSV : Pass the value **combined_perf.csv** to have the perf parameters for both the Graph Based and RDF based DMSs in a single plot.
* -pf PLOT\_FOR, --plot\_for PLOT\_FOR : The benchmarking actions for which we need to plot. (eg. "load,query\_hot,query\_cold")
* -lg LOAD\_GRAPH\_CSV, --load\_graph\_csv LOAD\_GRAPH\_CSV : Pass the value **graph.load.logs** if you want seperate plots for only the Graph Based DMSs for the Execution Time, for the action of loading a Dataset.
* -qg QUERY\_GRAPH\_CSV, --query\_graph\_csv QUERY\_GRAPH\_CSV : Pass the value **graph.query.logs** if you want seperate plots for only the Graph Based DMSs for the Execution Time, for the benchmarking action of running queries.
* -lr LOAD\_RDF\_CSV, --load\_rdf\_csv LOAD\_RDF\_CSV : Pass the value **rdf.load.logs** if you want seperate plots for only the RDF Based DMSs for the Execution Time, for the action of loading a Dataset.
* -qr QUERY\_RDF\_CSV, --query\_rdf\_csv QUERY\_RDF\_CSV : Pass the value **rdf.query.logs** if you want seperate plots for only the RDF Based DMSs for the Execution Time, for the benchmarking action of running queries.
* -lc LOAD\_COMBINED\_CSV, --load\_combined\_csv LOAD\_COMBINED\_CSV : Pass the value **combined.load.logs**  if you want plots for Graph Based and RDF based DMSs for the Execution Time, for the benchmarking action of loading a datafile.
* -qc QUERY_COMBINED_CSV, --query_combined_csv QUERY_COMBINED_CSV : Pass the value **combined.query.logs** if you want plots for Graph Based and RDF based DMSs for the Execution Time, for the benchmarking action of running queries.
* -pp PLOT\_PARAMETERS, --plot\_parameters PLOT\_PARAMETERS : Pass a comma seperated string of the perf parameters which you want to plot. The list of plot parameters is mentioned in the appendix. 
* -df DESTINATION\_FOLDER, --destination\_folder DESTINATION\_FOLDER : The folder where all the plots and corresponding tables should be saved.


## Step 9 : Copying the data from the Docker to your PC

* Find the container id of the Docker Container using the following command
```bash
docker ps -a --no-trunc 
```

* Copy the entire directory using the command
```bash
docker cp container_id:/path/to/directory/in/previous/step /path/on/your/machine
```



# Appendix
### List of Perf parameters for the plotting script.
* cycles
* instructions 
* cache-references 
* cache-misses
* bus-cycles
* L1-dcache-loads
* L1-dcache-load-misses
* L1-dcache-stores
* dTLB-loads
* dTLB-load-misses
* LLC-loads
* LLC-load-misses
* LLC-stores
* branches
* branch-misses
* context-switches
* cpu-migrations
* page-faults



