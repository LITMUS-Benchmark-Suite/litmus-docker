# litmus-docker
A docker container for the Litmus-Benchmark-Suite.

# Install Docker on your system
Install Docker Community Edition (CE). The instructions for the installation process can be found [here](https://docs.docker.com/engine/installation/).

## Build the Docker File

```bash
docker build -t litmus:local /path/of/the/repo
```

## Run the container

```bash
docker run --privileged litmus:local
```
We are using the _--privileged_ flag, because the following command in the scripts needs root access.

```bash
echo 3 > /proc/sys/vm/drop_caches
```

## DMS supported
The following DMS systems are supported currently.
### Graph based DMS
* Orient
* Sparksee
* Neo4J

### RDF based DMS
* Jena
* RDF3X
* Opensource Virtuoso


