FROM ubuntu:16.04

MAINTAINER Yashwant Keswani <yashwant.keswani@gmail.com>

# Install packages.
RUN apt-get update && apt-get install -y \
            git \
            make \
            gcc-4.7 \
            build-essential g++ \
            python3 \
            default-jre \
            default-jdk \
            unzip \
            wget \
     && apt-get clean

# Install gh-rdf3x and clean up
RUN git clone https://github.com/gh-rdf3x/gh-rdf3x.git \
    && cd gh-rdf3x \
    && make

# Install Openlink Virtuoso
# RUN apt-get update && apt-get install -y openssl
# RUN git clone https://github.com/openlink/virtuoso-opensource \
  #  && cd virtuoso-opensource \
  #  && ./autogen.sh \
  #  && ./configure \
  #  && make \
  #  && make install

# Install Gremlin Groovy for sparksee
RUN wget http://www.tinkerpop.com/downloads/gremlin/gremlin-groovy-2.6.0.zip
RUN unzip gremlin-groovy-2.6.0.zip
RUN mv gremlin-groovy-2.6.0 gremlin-groovy

# Install Orient
RUN wget https://orientdb.com/download.php?file=orientdb-community-2.1.3.tar.gz
RUN tar -xf download.php?file=orientdb-community-2.1.3.tar.gz -C /
RUN mv /orientdb-community-2.1.3 /orientdb


# Install Apache Jena
RUN wget http://mirror.fibergrid.in/apache/jena/binaries/apache-jena-3.2.0.zip
RUN unzip apache-jena-3.2.0.zip

#Installing open link virtuoso
RUN apt-get install -y build-essential debhelper autotools-dev autoconf automake unzip wget net-tools git libtool flex bison gperf gawk m4 libssl-dev libreadline-dev libreadline-dev openssl 
RUN git clone https://github.com/openlink/virtuoso-opensource.git \
        && cd virtuoso-opensource \
        && ./autogen.sh \
        && ./configure \
        && make && make install 


RUN apt-get install -y time

RUN apt-get install -y linux-tools-4.4.0-53-generic

RUN apt-get install -y software-properties-common

#RUN add-apt-repository -y ppa:webupd8team/java 
#RUN apt-get update 
#RUN apt-get i-y nstall oracle-java8-installer
#RUN apt-get install oracle-java8-set-default

# create directory for gh-rdf3x logs
RUN mkdir /var/log/rdf3x

# create directory for sparkee logs
RUN mkdir /var/log/sparksee

# create directory for orient logs
RUN mkdir /var/log/orient

# create directory for neo4j logs
RUN mkdir /var/log/neo4j

# create directory for monet logs
RUN mkdir /var/log/monet

# create directory for jena logs
RUN mkdir /var/log/jena

# create directory for arq logs
RUN mkdir /var/log/arq

# create directory for tinker logs
RUN mkdir /var/log/tinker

# create directory for virtuoso logs
RUN mkdir /var/log/virtuoso


# create directory and add data
RUN mkdir graph_data
ADD ./data/* /graph_data/


# create a general directory for all scripts
RUN mkdir scripts

#create directory for Tinker
RUN mkdir scripts/tinker/
ADD ./tinker/* /scripts/tinker/


#create directory for sparksee
RUN mkdir scripts/sparksee/
ADD ./sparksee/* /scripts/sparksee/

#Create directory for rdf3x
RUN mkdir scripts/rdf3x/
ADD ./rdf3x/* /scripts/rdf3x/

#Create directory for orient
RUN mkdir scripts/orient/
ADD ./orient/* /scripts/orient/

#Create directory for neo4j
RUN mkdir scripts/neo4j/
ADD ./ne04j/* /scripts/neo4j/

#Create directory for jena
RUN mkdir scripts/jena/
ADD ./jena/* /scripts/jena/




#Create directory for virtuoso
RUN mkdir scripts/virtuoso/
ADD ./openlink/* /scripts/virtuoso/



#Copy all the graph_files
#RUN mkdir /graph_data
ADD ./graph_data/* /graph_data/

#Copy all the rdf_files
RUN mkdir /rdf_data
ADD ./rdf_data/* /rdf_data/

#Copy all the sparql queries
RUN mkdir /sparql_query
ADD ./sparql_query/* /sparql_query/

#Copy all the gremlin queries
RUN mkdir /gremlin_query
ADD ./gremlin_query/* /gremlin_query/

# create folder for gremlin query for perf
RUN mkdir /gremlin_query_perf

# copying all the scripts
ADD ./hello_world.py ./
ADD ./run_script.py ./


CMD python3 run_script.py -g -n 3 -gd /graph_data -rd /rdf_data -gq /gremlin_query -rq /sparql_query && cat temp_graph.csv graph.load.logs graph.query.logs
#&& cat temp_rdf.csv && python3 plot_script.py && ls -lh /plots/* && ls -lh /tables/*
#CMD ls /apache-jena-3.2.0/bin/*
#CMD touch /var/log/tinker/load_log_perf.log.1 && perf stat -o /var/log/tinker/load_log_perf.log.1 --append -e cycles,instructions,cache-references,cache-misses,bus-cycles -a /scripts/tinker/TinkerLoadPerf.sh /tmp/tinker.gdb /graph_data/graph-example-1.xml /var/log/tinker/load_logs.log && cat /var/log/tinker/load_log_perf.log.1
