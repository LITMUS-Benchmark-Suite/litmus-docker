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



# create directory for gh-rdf3x logs
RUN mkdir /var/log/gh-rdf3x

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



# create directory and add data
RUN mkdir graph_data
ADD ./data/* /graph_data/


# create a general directory for all scripts
RUN mkdir scripts

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


# copying all the scripts
ADD ./hello_world.py ./
ADD ./run_script.py ./

#CMD ls 
CMD python3 run_script.py 
