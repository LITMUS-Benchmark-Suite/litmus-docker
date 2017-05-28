# LITMUS
LITMUS is a comprehensive framework, that will serve the academicians, researchers, DMS developers and the organizations who employ DMSs for the efficient consumption of their data, by allowing a choke-point driven performance comparison and analysis of various Data Management Solutions (Graph and RDF-based), with respect to different third-party real and synthetic datasets and queries.

## DMS supported
The following DMS systems are supported currently.

### Graph based DMS
* Orient
* Sparksee
* Neo4J
* TinkerGraph

### RDF based DMS
* Jena
* RDF3X
* Opensource Virtuoso
* 4store

## Parameters Measured
* Execution Time
* Cycles : The number of cycles it takes to execute a task (loading a database for a DMS, or running a particular query for a DMS).
* Instructions : The number of instructions which are executed in the task. 
* Cache references : The total number of cache references which are made during the task.
* Cache misses : The total number of cache misses that happen during the task.
* Bus cycles : The number of bus cycles happening during the execution of the task.
* L1 data cache loads : The total number of data cache loads for L1 cache that happen during the execution of the task.
* L1 data cache load misses : The total number of L1 data cache load misses that happen during the execution of the task.
* L1 data cache stores : The L1 data cache stores that happen during the execution of the task 
* dTLB loads : The data translation lookaside buffer loads that happen during the execution of the task. 
* dTLB load misses : The data Translation lookaside buffer loads misses that happen during the execution of the task.
* dTLB prefetch misses : The data Translation lookaside buffer prefetch misses that happen during the execution of the task.
* LLC loads : The Last level Cache loads that happen during the execution of the task. 
* LLC load misses : The last level cache load misses that happen during the execution of the task.
* LLC stores : The last level cache stores that happen during the execution of the task.
* LLC Prefetches : The last level cache prefetches that happen during the execution of the task.
* Branches : The total number of branches that are encountered during the execution of the task.
* Branch misses : The total number of branches that are  missed in the execution of the task.
* Context switches : The total context switches that happen when the task is executed.
* CPU migrations : The CPU migrations that happen when the task is executed.
* Page faults : The page faults that happen when the task is executed.

## litmus-docker Installation Instructions
A docker container for the Litmus-Benchmark-Suite.

### Install Docker on your system
Install Docker Community Edition (CE). The instructions for the installation process can be found [here](https://docs.docker.com/engine/installation/).


### Instructions
The [Instructions.md](https://github.com/LITMUS-Benchmark-Suite/litmus-docker/blob/master/Instructions.md) file has all the instructions to setup and run the Litmus Benchmark Suite.

### Build the Docker File

```bash
docker build -t litmus:local /path/of/the/repo
```

### Run the container

```bash
docker run --privileged litmus:local
```
We are using the _--privileged_ flag, because we need root access to clear the caches when we run the benchmarking process.


