import argparse
import os
import glob
import sys
import time
import logging
import subprocess
import re

logging.basicConfig(filename = "Litmus_Benchmark_log.log", level = logging.INFO)
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

graph_based = ['g_sparksee', 'g_orient', 'g_neo4j', 'g_tinker' ]

rdf_based = ['r_rdf3x', 'r_monet', 'r_jena', 'r_arq', 'r_virtuoso' ]


#maps the DMS with the directories of their log files.
directory_maps = { \
    'g_sparksee':'sparksee', \
    'g_orient' : 'orient', \
    'g_neo4j' : 'neo4j', \
    'g_tinker' : 'tinker', \
    'r_rdf3x' : 'rdf3x', \
    'r_monet' : 'monet', \
    'r_jena' : 'jena', \
    'r_arq' : 'arq', \
    'r_virtuoso' : 'virtuoso'
    }

#maps the DMS with the directories where the queries exist.
query_directory_maps = { \
    'g_sparksee':'/gremlin_query_perf', \
    'g_orient' : '/gremlin_query_perf', \
    'g_neo4j' : '/gremlin_query_perf', \
    'g_tinker' : '/gremlin_query_perf', \
    'r_rdf3x' : '/sparql_query', \
    'r_jena' : '/jena_queries', \
    'r_virtuoso' : '/virtuoso_queries'
    }

#maps the DMS with the extension of their queries.
query_extension_maps = { \
    'g_sparksee':'/sparsee_*.groovy', \
    'g_orient' : '/orient_*.groovy', \
    'g_neo4j' : '/neo4j_*.groovy', \
    'g_tinker' : '/tinker_*.groovy', \
    'r_rdf3x' : '/*.sparql', \
    'r_jena' : '/*.sparql', \
    'r_virtuoso' : '/*.sparql'
    }

def gather_data_graph_dms(dms):
    #Gather the data and put it in a csv format
    """This function is used to process the log files for a rdf based dms and 
    returns the data in form of a tuple of two lists.
    dms : is the name of the Data Management Solution."""     
    logger.info("Inside the gather_data_graph_dms for %s" % (dms))
    csv_load = []

    logger.info("Opening the load_logs.log file for %s" % (dms))
    file_handler = open("/var/log/%s/load_logs.log" % (directory_maps[dms]), "r")
    all_lines = file_handler.readlines()
    file_handler.close()
    run_id = 1
    logger.info("Succesfuly opened and read the load_logs.log file for %s" % (dms))

    for each in all_lines:
        try:
            csv_load.append([directory_maps[dms], str(run_id), "load", str(int(each.strip()))])
            run_id+=1
        except Exception as e:
            print(e)

    logger.info("Succesfuly processed the load_logs.log file for %s" % (dms))

    #for each in csv_load:
    #    print(",".join(each))

    logger.info("Opening the query_cold_logs.log file for %s" % (dms))
    file_handler = open("/var/log/%s/query_cold_logs.log" % (directory_maps[dms]), "r")
    all_lines = file_handler.readlines()[5:]
    file_handler.close()
    logger.info("Succesfuly opened and read the query_cold_logs.log file for %s" % (dms))

    run_id = 0
    csv_query = []
    flag = True
    for each in all_lines:
        if each[0]=="#":
            run_id+=1
            flag = True
            continue;
        if flag:
            if "Query" not in each:
                continue
            query_no = each.split("Query ")[1].split("=")[0]
            flag = False
        else:
            try:
                csv_query.append([directory_maps[dms], str(run_id), "query_cold",\
                 str(query_no), str(int(each.strip()))])
                flag = True
            except Exception as e:
                print(e)
    logger.info("Succesfuly processed the query_cold_logs.log file for %s" % (dms))



    
    logger.info("Opening the query_hot_logs.log file for %s" % (dms))
    file_handler = open("/var/log/%s/query_hot_logs.log" % (directory_maps[dms]), "r")
    all_lines = file_handler.readlines()[5:]
    file_handler.close()
    logger.info("Succesfuly opened and read the query_hot_logs.log file for %s" % (dms))
    run_id = 0
    flag = True
    for each in all_lines:
        if each[0]=="#":
            run_id+=1
            flag = True
            continue;
        if flag:
            if "Query" not in each:
                continue
            query_no = each.split("Query ")[1].split("=")[0]
            flag = False
        else:
            try:
                csv_query.append([directory_maps[dms], str(run_id), "query_hot",\
                 str(query_no), str(int(each.strip()))])
                flag = True
            except Exception as e:
                print(e)
    logger.info("Succesfuly processed the query_hot_logs.log file for %s" % (dms))


    
    #for each in csv_query:
    #    print(",".join(each))
    return (csv_load, csv_query)

def gather_data_rdf_dms(dms):
    #Gather the data and put it in a csv format
    """This function is used to process the log files for a rdf based dms and 
    returns the data in form of a tuple of two lists.
    dms : is the name of the Data Management Solution.""" 
    logger.info("Inside the gather_data_rdf_dms for %s" % (dms))

    csv_load = []

    logger.info("Opening the load_logs.log file for %s" % (dms))

    file_handler = open("/var/log/%s/load_logs.log" % (directory_maps[dms]), "r")
    all_lines = file_handler.readlines()
    file_handler.close()
    logger.info("Succesfuly opened and read the load_logs.log file for %s" % (dms))

    run_id = 1
    for each in all_lines:
        csv_load.append([directory_maps[dms], str(run_id), "load", \
            each.strip().split("\t")[2]])
        run_id+=1

    logger.info("Succesfuly processed the load_logs.log file for %s" % (dms))


    csv_query = []


    logger.info("Opening the query_cold_logs.log file for %s" % (dms))
    file_handler = open("/var/log/%s/query_cold_logs.log" % (directory_maps[dms]), "r")
    all_lines = file_handler.readlines()
    file_handler.close()
    logger.info("Succesfuly opened and read the query_cold_logs.log file for %s" % (dms))


    run_id = 0
    query_name = ""
    name_flag = True
    for each in all_lines:
        if each[0]=="*":
            run_id = 0
            name_flag = True
            continue;
        if name_flag:
            query_name = each.strip()
            name_flag = False
        else:
            run_id+=1
            csv_query.append([directory_maps[dms], str(run_id), "query_cold", query_name, \
                    each.strip().split("\t")[2]])

    logger.info("Succesfuly processed the query_cold_logs.log file for %s" % (dms))
    

    logger.info("Opening the query_hot_logs.log file for %s" % (dms))
    file_handler = open("/var/log/%s/query_hot_logs.log" % (directory_maps[dms]), "r")
    all_lines = file_handler.readlines()
    file_handler.close()
    logger.info("Succesfuly opened and read the query_hot_logs.log file for %s" % (dms))


    run_id = 0
    query_name = ""
    name_flag = True
    for each in all_lines:
        if each[0]=="*":
            run_id = 0
            name_flag = True
            continue;
        if name_flag:
            query_name = each.strip()
            name_flag = False
        else:
            run_id+=1
            csv_query.append([directory_maps[dms], str(run_id), "query_hot", query_name, \
                    each.strip().split("\t")[2]])

    logger.info("Succesfuly processed the query_hot_logs.log file for %s" % (dms))
        
    for each in csv_load:
        print(",".join(each))
    for each in csv_query:
        print(",".join(each))

    return (csv_load, csv_query)

def create_csv_from_logs(filename_load, filename_query, list_of_dbs, graph_dms):
    """This function creates a combined csv file which has the data 
    about all the graph based dms or rdf based dms.
    filename_load : name of the file where the loading time data is stored.
    filename_query : name of the file where the query time data is stored.
    list_of_dbs : where all the dbs which need to be processed are stored
    graph_dms : True if it it graph based DMS, False if it is RDF based DMS"""
    load_logs = []
    query_logs = []
    for each in list_of_dbs:
        load, query = None, None    
        if graph_dms:
            load, query = gather_data_graph_dms(each)
        else:
            load, query = gather_data_rdf_dms(each)
        load_logs = load_logs + load
        query_logs = query_logs + query
    load_handler = open(filename_load, "w")
    load_handler.write("dms,run_id,load_type,time\n")
    for each in load_logs:
        load_handler.write(",".join(each) + "\n")
    load_handler.close()

    query_handler = open(filename_query, "w")
    query_handler.write("dms,run_id,query_type,query_id,time\n")
    for each in query_logs:
        query_handler.write(",".join(each) + "\n")
    query_handler.close()


def run_perf(command, log_file, clear_cache = False, prelogue = None, epilogue = None):
    """This function is the heart of the code. It is used to run the perf commands. Since 
    the perf commands has a lot of parameters, and the hardware counters are limited, we break
    the entire runs into four runs, and store them in four different log files and then combine the results.
    command : The command which needs to be run.
    log_file : The name of the base log file. Each perf sub command will have a different log_file.
    clear_cache : Whether we need to clear the cache after every perf sub command.
    prelogue : Which needs to be run before the command.
    epilogue : which needs to be run after the command.
    """

    clear_cache_command = "echo 3 > /proc/sys/vm/drop_caches"

    #perf1, perf2, perf3 and perf4 are the four perf sub commands
    perf1 = "perf stat -o %s --append -e cycles,instructions,cache-references,cache-misses,bus-cycles -a %s" % (log_file+".1", command)
    perf2 = "perf stat -o %s --append -e L1-dcache-loads,L1-dcache-load-misses,L1-dcache-stores,dTLB-loads,dTLB-load-misses,dTLB-prefetch-misses -a %s" % (log_file + ".2", command)
    perf3 = "perf stat -o %s --append -e LLC-loads,LLC-load-misses,LLC-stores,LLC-prefetches -a %s" % (log_file + ".3", command)
    perf4 = "perf stat -o %s --append -e branches,branch-misses,context-switches,cpu-migrations,page-faults -a %s" % (log_file + ".4", command)

    logger.info("Perf Command 1: %s " %(perf1))
    logger.info("Perf Command 2: %s " %(perf2))
    logger.info("Perf Command 3: %s " %(perf3))
    logger.info("Perf Command 4: %s " %(perf4))

    if clear_cache:
        subprocess.call(clear_cache_command, shell = True)
    if prelogue:
        subprocess.call(prelogue, shell = True)
    print("*****", perf1, "*****")
    subprocess.call(perf1, shell = True)
    if epilogue:
        subprocess.call(epilogue, shell = True)
    print("FInished perf1")

    sys.stdout.flush()
    if clear_cache:
        subprocess.call(clear_cache_command, shell = True)
    if prelogue:
        subprocess.call(prelogue, shell = True)
    print("*****", perf2, "*****")
    subprocess.call(perf2, shell = True)
    if epilogue:
        subprocess.call(epilogue, shell = True)
    print("FInished perf2")
    sys.stdout.flush()

    if clear_cache:
        subprocess.call(clear_cache_command, shell = True)
    if prelogue:
        subprocess.call(prelogue, shell = True)
    print("*****", perf3, "*****")
    subprocess.call(perf3, shell = True)
    if epilogue:
        subprocess.call(epilogue, shell = True)
    print("Finished Perf3")
    sys.stdout.flush()

    if clear_cache:
        subprocess.call(clear_cache_command, shell = True)
    if prelogue:
        subprocess.call(prelogue, shell = True)
    print("*****", perf4, "*****")
    subprocess.call(perf4, shell = True)
    if epilogue:
        subprocess.call(epilogue, shell = True)
    sys.stdout.flush()

def g_sparksee_with_perf(runs, xmlFile):
    """This function is used to run the sparksee DMS with perf tool.
    runs : THe number of runs
    xmlFile : The location of the graphml File.
    """
    logger.info("*"*80)
    logger.info("Running the scripts for the Sparksee DMS With Perf")
    logger.info("Data File = %s, Runs = %s" % (xmlFile, runs))

    
    logger.info("Running the command to load the databse")
    for each in range(runs):
        #Loading the database
        load_command = "/scripts/sparksee/SparkseeLoadPerf.sh /tmp/sparksee_load.gdb %s /var/log/sparksee/load_logs.log" % (xmlFile) 
        run_perf(load_command, "/var/log/sparksee/load_log_perf.log", clear_cache = True)
        command = "rm -r /tmp/*"
        subprocess.call(command, shell = True)    
        print("Finished running the load command")

        #Querying the database

    load_command = "/scripts/sparksee/SparkseeQueryPerf_load.sh /tmp/sparksee_perf.gdb %s" % (xmlFile)
    subprocess.call(load_command, shell = True)

    logger.info("Running the queries on hot cache for sparksee DMS")
    all_queries = glob.glob("/gremlin_query_perf/sparksee_*");
    for each in range(runs):
        command = 'echo "################Run %d################" >> %s' % (each, "/var/log/sparksee/query_hot_logs.log")
        subprocess.call(command, shell = True)
        for each_query in all_queries:
            name_of_query = "_".join(each_query.split("/")[-1].split(".")[0].split("_")[1:])
            print(name_of_query, "****************")
            hot_query_command = "/scripts/sparksee/SparkseeQueryPerf.sh %s /var/log/sparksee/query_hot_logs.log" % (each_query)
            run_perf(hot_query_command, "/var/log/sparksee/query_hot_logs_perf.log.%s" %(name_of_query))

    all_queries = glob.glob("/gremlin_query_perf/sparksee_*");

    logger.info("Running the queries on cold cache for sparksee DMS")
    for each in range(runs):
        command = 'echo "################Run %d################" >> %s' % (each, "/var/log/sparksee/query_cold_logs.log")
        subprocess.call(command, shell = True)
        for each_query in all_queries:
            name_of_query = "_".join(each_query.split("/")[-1].split(".")[0].split("_")[1:])
            cold_query_command = "/scripts/sparksee/SparkseeQueryPerf.sh %s /var/log/sparksee/query_cold_logs.log" % (each_query)
            run_perf(cold_query_command, "/var/log/sparksee/query_cold_logs_perf.log.%s" %(name_of_query), clear_cache = True)

        print("Finished running the cold query command")


    
def g_sparksee(runs, xmlFile):
    """This function is used to run the sparksee DMS without perf tool.
    runs : THe number of runs
    xmlFile : The location of the graphml File.
    """
    logger.info("*"*80)
    logger.info("Running the scripts for the Sparksee DMS")
    logger.info("Data File = %s, Runs = %s" % (xmlFile, runs))
    logger.info("Running the command : /scripts/sparksee/SparkseeLoad.sh %s \
    /tmp/sparksee.gdb %s \
    /var/log/sparksee/load_logs.log" % (runs, xmlFile))
    
    
    #Loading the database
    os.system("/scripts/sparksee/SparkseeLoad.sh %s \
    /tmp/sparksee.gdb %s \
    /var/log/sparksee/load_logs.log" % (runs, xmlFile))

    logger.info("Running the command : /scripts/sparksee/SparkseeQuery.sh %s \
    /tmp/HelloWorld.gdb.sparksee.cold %s \
    /var/log/sparksee/query_cold_logs.log /scripts/sparksee/SparkseeQueryCold.groovy" % (runs, xmlFile))

    #Querying the database
    os.system("/scripts/sparksee/SparkseeQuery.sh %s \
    /tmp/HelloWorld.gdb.sparksee.cold %s \
    /var/log/sparksee/query_cold_logs.log /scripts/sparksee/SparkseeQueryCold.groovy" % (runs, xmlFile))

    logger.info("Running the command : /scripts/sparksee/SparkseeQuery.sh %s \
    /tmp/HelloWorld.gdb.sparksee.hot %s \
    /var/log/sparksee/query_hot_logs.log /scripts/sparksee/SparkseeQueryHot.groovy" % (runs, xmlFile))

    os.system("/scripts/sparksee/SparkseeQuery.sh %s \
    /tmp/HelloWorld.gdb.sparksee.hot %s \
    /var/log/sparksee/query_hot_logs.log /scripts/sparksee/SparkseeQueryHot.groovy" % (runs, xmlFile))

    #logger.info("Gathering the info and putting it in a csv file")
    #Gather the data and put it in a csv format
    #gather_data_graph_dms("g_sparksee")
    logger.info("*"*80)

def g_tinker_with_perf(runs, xmlFile):
    """This function is used to run the TinkerGraph DMS with perf tool.
    runs : THe number of runs
    xmlFile : The location of the graphml File.
    """

    logger.info("*"*80)
    logger.info("Running the scripts for the TinkerGraph DMS With Perf")
    logger.info("Data File = %s, Runs = %s" % (xmlFile, runs))

    logger.info("Running the command to load the databse")
    for each in range(runs):
        #Loading the database
        load_command = "/scripts/tinker/TinkerLoadPerf.sh /tmp/tinker.gdb %s /var/log/tinker/load_logs.log" % (xmlFile)
        #print(load_command)
        run_perf(load_command, "/var/log/tinker/load_log_perf.log", clear_cache = True)

        print("Finished running the load command")

        #Querying the database

    load_command = "/scripts/tinker/TinkerQueryPerf_load.sh /tmp/tinker_perf %s /dev/null" % (xmlFile)
    subprocess.call(load_command, shell = True)

    all_queries = glob.glob("/gremlin_query_perf/tinker_*");

    logger.info("Running the queries on TinkerGraph on cold cache")

    for each in range(runs):
        command = 'echo "################Run %d################" >> %s' % (each, "/var/log/tinker/query_cold_logs.log")
        subprocess.call(command, shell = True)
        for each_query in all_queries:
            name_of_query = "_".join(each_query.split("/")[-1].split(".")[0].split("_")[1:])
            cold_query_command = "/scripts/tinker/TinkerQueryPerf.sh %s /var/log/tinker/query_cold_logs.log" % (each_query)
            run_perf(cold_query_command, "/var/log/tinker/query_cold_logs_perf.log.%s" %(name_of_query), clear_cache = True)

        print("Finished running the cold query command")


    all_queries = glob.glob("/gremlin_query_perf/tinker_*");
    logger.info("Running the queries on TinkerGraph on hot cache")

    for each in range(runs):
        command = 'echo "################Run %d################" >> %s' % (each, "/var/log/tinker/query_hot_logs.log")
        subprocess.call(command, shell = True)
        for each_query in all_queries:
            name_of_query = "_".join(each_query.split("/")[-1].split(".")[0].split("_")[1:])
            print(name_of_query, "****************")
            hot_query_command = "/scripts/tinker/TinkerQueryPerf.sh %s /var/log/tinker/query_hot_logs.log" % (each_query)
            run_perf(hot_query_command, "/var/log/tinker/query_hot_logs_perf.log.%s" %(name_of_query))


    logger.info("*"*80)

def g_tinker(runs, xmlFile):
    """This function is used to run the TinkerGraph DMS without perf tool.
    runs : THe number of runs
    xmlFile : The location of the graphml File.
    """

    logger.info("*"*80)
    logger.info("Running the scripts for the TinkerGraph DMS")
    logger.info("Data File = %s, Runs = %s" % (xmlFile, runs))
    logger.info("Running the command : /scripts/tinker/TinkerLoad.sh %s \
    /tmp/tinker.gdb %s \
    /var/log/tinker/load_logs.log" % (runs, xmlFile))
    
    
    #Loading the database
    os.system("/scripts/tinker/TinkerLoad.sh %s \
    /tmp/tinker.gdb %s \
    /var/log/tinker/load_logs.log" % (runs, xmlFile))

    logger.info("Running the command : /scripts/tinker/TinkerQuery.sh %s \
    /tmp/HelloWorld.gdb.tinker.cold %s \
    /var/log/tinker/query_cold_logs.log /scripts/tinker/TinkerQueryCold.groovy" % (runs, xmlFile))

    #Querying the database
    os.system("/scripts/tinker/TinkerQuery.sh %s \
    /tmp/HelloWorld.gdb.tinker.cold %s \
    /var/log/tinker/query_cold_logs.log /scripts/tinker/TinkerQueryCold.groovy" % (runs, xmlFile))

    logger.info("Running the command : /scripts/tinker/TinkerQuery.sh %s \
    /tmp/HelloWorld.gdb.tinker.hot %s \
    /var/log/tinker/query_hot_logs.log /scripts/tinker/TinkerQueryHot.groovy" % (runs, xmlFile))

    os.system("/scripts/tinker/TinkerQuery.sh %s \
    /tmp/HelloWorld.gdb.tinker.hot %s \
    /var/log/tinker/query_hot_logs.log /scripts/tinker/TinkerQueryHot.groovy" % (runs, xmlFile))

    logger.info("Gathering the info and putting it in a csv file")
    #Gather the data and put it in a csv format
    #gather_data_graph_dms("g_tinker")
    logger.info("*"*80)


def r_rdf3x(runs, queryLocations, dataFile):
    """This function is used to run the RDF3x DMS without perf tool.
    runs : THe number of runs
    queryLocations : The directories which has the SPARQL queries for RDF3x
    dataFile : The location of the datafile.
    """

    logger.info("*"*80)
    logger.info("Running the scripts for the RDF3x DMS")
    logger.info("Runs = %s, queryLocations = %s, dataFile = %s" % (runs, queryLocations, dataFile))

    logger.info("Running the command : /scripts/rdf3x/RDF3xLoad.sh %s /tmp rdf3x_graph \
    %s /var/log/rdf3x/load_logs.log" % (runs, dataFile))

    #Loading the database
    os.system("/scripts/rdf3x/RDF3xLoad.sh %s /tmp rdf3x_graph \
    %s /var/log/rdf3x/load_logs.log" % (runs, dataFile)) 
    
    logger.info("Running the command : /scripts/rdf3x/RDF3xExecuteColdCache.sh /tmp rdf3x_graph_cold \
    %s %s /var/log/rdf3x/query_cold_logs.log %s" % (dataFile, queryLocations, runs))

    #Querying the database
    os.system("/scripts/rdf3x/RDF3xExecuteColdCache.sh /tmp rdf3x_graph_cold \
    %s %s /var/log/rdf3x/query_cold_logs.log %s" % (dataFile, queryLocations, runs))


    logger.info("Running the command : /scripts/rdf3x/RDF3xExecuteHotCache.sh /tmp rdf3x_graph_hot \
    %s %s /var/log/rdf3x/query_cold_logs.log %s" % (dataFile, queryLocations, runs))

    #Querying the database
    os.system("/scripts/rdf3x/RDF3xExecuteHotCache.sh /tmp rdf3x_graph_hot \
    %s %s /var/log/rdf3x/query_hot_logs.log %s" % (dataFile, queryLocations, runs)) 
    
    #logger.info("Gathering the info and putting it in a csv file")        
    #gather_data_rdf_dms("r_rdf3x")
    logger.info("*"*80)


def r_rdf3x_with_perf(runs, queryLocations, dataFile):
    """This function is used to run the RDF3x DMS with perf tool.
    runs : THe number of runs
    queryLocations : The directories which has the SPARQL queries for RDF3x
    dataFile : The location of the datafile.
    """

    logger.info("*"*80)
    logger.info("Running the scripts for the RDF3x DMS with perf")
    logger.info("Runs = %s, queryLocations = %s, dataFile = %s" % (runs, queryLocations, dataFile))

    logger.info("Running the command : /scripts/rdf3x/RDF3xLoadPerf.sh %s /tmp rdf3x_graph \
    %s /var/log/rdf3x/load_logs.log" % (runs, dataFile))

    #Loading the database
    for each in range(runs):
        load_command = "/scripts/rdf3x/RDF3xLoadPerf.sh /tmp rdf3x_graph_%s %s /var/log/rdf3x/load_logs.log" % (str(each), dataFile) 
        run_perf(load_command, "/var/log/rdf3x/load_log_perf.log", clear_cache = True)

    subprocess.call("rm -r /tmp/*", shell = True)

    load_command = "/scripts/rdf3x/RDF3xLoadPerf.sh /tmp rdf3x_graph %s /dev/null" % (dataFile)
    subprocess.call(load_command, shell = True)


    m = glob.glob(queryLocations + "/*.sparql")
    for each_command in m:
        name_of_file = each_command.split("/")[-1].split(".")[0]
        subprocess.call("echo %s >> /var/log/rdf3x/query_cold_logs.log" % (name_of_file), shell = True)
        for each in range(runs):
            query_command = "/scripts/rdf3x/RDF3xExecuteColdCachePerf.sh /tmp rdf3x_graph /var/log/rdf3x/query_cold_logs.log %s" % (each_command)
            run_perf(query_command, "/var/log/rdf3x/cold_query_log_perf.log.%s" %(name_of_file), clear_cache = True)
    
    m = glob.glob(queryLocations + "/*.sparql")
    for each_command in m:
        name_of_file = each_command.split("/")[-1].split(".")[0]
        subprocess.call("echo %s >> /var/log/rdf3x/query_hot_logs.log" % (name_of_file), shell = True)
        for each in range(runs):
            query_command = "/scripts/rdf3x/RDF3xExecuteHotCachePerf.sh /tmp rdf3x_graph /var/log/rdf3x/query_hot_logs.log %s" % (each_command)
            run_perf(query_command, "/var/log/rdf3x/hot_query_log_perf.log.%s" %(name_of_file))


def g_orient_with_perf(runs, xmlFile):
    """This function is used to run the Orient DMS with perf tool.
    runs : THe number of runs
    xmlFile : The location of the graphml File.
    """

    logger.info("*"*80)
    logger.info("Running the scripts for the Orient DMS With Perf")
    logger.info("Data File = %s, Runs = %s" % (xmlFile, runs))

    logger.info("Running the load scripts for the Orient DMS")
    for each in range(runs):
        #Loading the database
        load_command = "/scripts/orient/OrientLoadPerf.sh /tmp/orient_load.gdb %s /scripts/orient/OrientLoadPerf.groovy /var/log/orient/load_logs.log" % (xmlFile)
        run_perf(load_command, "/var/log/orient/load_log_perf.log", clear_cache = True)


    load_command = "/scripts/orient/OrientLoadPerf.sh /orient_perf %s /scripts/orient/OrientQueryPerf_load.groovy /dev/null" % (xmlFile)
    subprocess.call(load_command, shell = True)


    all_queries = glob.glob("/gremlin_query_perf/orient_*");
    logger.info("Running the queries for the Orient DMS on cold cache")    
    for each in range(runs):
        command = 'echo "################Run %d################" >> %s' % (each, "/var/log/orient/query_cold_logs.log")
        subprocess.call(command, shell = True)
        for each_query in all_queries:
            name_of_query = "_".join(each_query.split("/")[-1].split(".")[0].split("_")[1:])
            print(name_of_query, "****************")
            cold_query_command = "/scripts/orient/OrientQueryPerf.sh /tmp/orient_perf %s /var/log/orient/query_cold_logs.log" % (each_query)
            run_perf(cold_query_command, "/var/log/orient/query_cold_logs_perf.log.%s"%(name_of_query), clear_cache = True)


    all_queries = glob.glob("/gremlin_query_perf/orient_*");
    logger.info("Running the queries for the Orient DMS on hot cache")
    for each in range(runs):
        command = 'echo "################Run %d################" >> %s' % (each, "/var/log/orient/query_hot_logs.log")
        subprocess.call(command, shell = True)
        for each_query in all_queries:
            name_of_query = "_".join(each_query.split("/")[-1].split(".")[0].split("_")[1:])
            print(name_of_query, "****************")
            hot_query_command = "/scripts/orient/OrientQueryPerf.sh /tmp/orient_perf %s /var/log/orient/query_hot_logs.log" % (each_query)
            run_perf(hot_query_command, "/var/log/orient/query_hot_logs_perf.log.%s"%(name_of_query))

    logger.info("*"*80)

def g_orient(runs, xmlFile):
    """This function is used to run the Orient DMS without perf tool.
    runs : THe number of runs
    xmlFile : The location of the graphml File.
    """

    logger.info("*"*80)
    logger.info("Running the scripts for the Orient DMS")
    logger.info("Data File = %s, Runs = %s" % (xmlFile, runs))
    logger.info("Running the command : /scripts/orient/OrientLoad.sh %s \
    /tmp/orient_load.gdb %s /scripts/orient/OrientLoad.groovy \
    /var/log/orient/load_logs.log" % (runs, xmlFile))

    #Loading the database
    os.system("/scripts/orient/OrientLoad.sh %s \
    /tmp/orient_load.gdb %s /scripts/orient/OrientLoad.groovy \
    /var/log/orient/load_logs.log" % (runs, xmlFile))

    logger.info("Running the command : /scripts/orient/OrientQuery.sh %s \
    /tmp/orient_query_cold.gdb %s /scripts/orient/OrientQueryCold.groovy \
    /var/log/orient/query_cold_logs.log" % (runs, xmlFile))

    #Querying the database
    os.system("/scripts/orient/OrientQuery.sh %s \
    /tmp/orient_query_cold.gdb %s /scripts/orient/OrientQueryCold.groovy \
    /var/log/orient/query_cold_logs.log" % (runs, xmlFile))

    logger.info("Running the command : /scripts/orient/OrientQuery.sh %s \
    /tmp/orient_query_hot.gdb %s /scripts/orient/OrientQueryHot.groovy \
    /var/log/orient/query_hot_logs.log" % (runs, xmlFile))

    os.system("/scripts/orient/OrientQuery.sh %s \
    /tmp/orient_query_hot.gdb %s /scripts/orient/OrientQueryHot.groovy \
    /var/log/orient/query_hot_logs.log" % (runs, xmlFile))



    #logger.info("Gathering the info and putting it in a csv file")
    #gather_data_graph_dms("g_orient")
    logger.info("*"*80)


def g_neo4j_with_perf(runs, xmlFile):
    """This function is used to run the Neo4jGraph DMS with perf tool.
    runs : THe number of runs
    xmlFile : The location of the graphml File.
    """

    logger.info("*"*80)
    logger.info("Running the scripts for the Neo4j DMS With Perf")
    logger.info("Data File = %s, Runs = %s" % (xmlFile, runs))

    logger.info("Running the load scripts for the Neo4j DMS ")
    for each in range(runs):
        #Loading the database
        load_command = "/scripts/neo4j/Neo4jLoadPerf.sh /tmp/neo4j_load.gdb %s /var/log/neo4j/load_logs.log" % (xmlFile) 
        run_perf(load_command, "/var/log/neo4j/load_log_perf.log", clear_cache = True)

        print("Finished running the load command")

        #Querying the database

    load_command = "/scripts/neo4j/Neo4jQueryPerf_load.sh /tmp/neo4j_perf %s /dev/null" % (xmlFile)
    subprocess.call(load_command, shell = True)

    logger.info("Running the queries for the Neo4j DMS on cold cache")
    all_queries = glob.glob("/gremlin_query_perf/neo4j_*");
    for each in range(runs):
        command = 'echo "################Run %d################" >> %s' % (each, "/var/log/neo4j/query_cold_logs.log")
        subprocess.call(command, shell = True)
        for each_query in all_queries:
            name_of_query = "_".join(each_query.split("/")[-1].split(".")[0].split("_")[1:])
            cold_query_command = "/scripts/neo4j/Neo4jQueryPerf.sh %s /var/log/neo4j/query_cold_logs.log" % (each_query)
            run_perf(cold_query_command, "/var/log/neo4j/query_cold_logs_perf.log.%s" %(name_of_query), clear_cache = True)

        print("Finished running the cold query command")




    logger.info("Running the queries for the Neo4j DMS on hot cache")
    all_queries = glob.glob("/gremlin_query_perf/neo4j_*");
    for each in range(runs):
        command = 'echo "################Run %d################" >> %s' % (each, "/var/log/neo4j/query_hot_logs.log")
        subprocess.call(command, shell = True)
        for each_query in all_queries:
            name_of_query = "_".join(each_query.split("/")[-1].split(".")[0].split("_")[1:])
            print(name_of_query, "****************")
            hot_query_command = "/scripts/neo4j/Neo4jQueryPerf.sh %s /var/log/neo4j/query_hot_logs.log" % (each_query)
            run_perf(hot_query_command, "/var/log/neo4j/query_hot_logs_perf.log.%s" %(name_of_query))




    logger.info("*"*80)



def g_neo4j(runs, xmlFile):
    """This function is used to run the Neo4jGraph DMS without perf tool.
    runs : THe number of runs
    xmlFile : The location of the graphml File.
    """

    logger.info("*"*80)
    logger.info("Running the scripts for the Neo4j DMS")
    logger.info("Data File = %s, Runs = %s" % (xmlFile, runs))
    logger.info("Running the command : /scripts/neo4j/Neo4jLoad.sh %s \
    /tmp/neo4j_load.gdb %s \
    /var/log/neo4j/load_logs.log" % (runs, xmlFile))

    #Loading the database
    os.system("/scripts/neo4j/Neo4jLoad.sh %s \
    /tmp/neo4j_load.gdb %s \
    /var/log/neo4j/load_logs.log" % (runs, xmlFile))

    logger.info("Running the command : /scripts/neo4j/Neo4jQuery.sh %s \
    /tmp/neo4j_Query.gdb.cold %s \
    /var/log/neo4j/query_cold_logs.log /scripts/neo4j/Neo4jQueryCold.groovy" % (runs, xmlFile))

    #Querying the database
    os.system("/scripts/neo4j/Neo4jQuery.sh %s \
    /tmp/neo4j_Query.gdb.cold %s \
    /var/log/neo4j/query_cold_logs.log /scripts/neo4j/Neo4jQueryCold.groovy" % (runs, xmlFile))
    
    logger.info("Running the command : /scripts/neo4j/Neo4jQuery.sh %s \
    /tmp/neo4j_Query.gdb.hot %s \
    /var/log/neo4j/query_hot_logs.log /scripts/neo4j/Neo4jQueryHot.groovy" % (runs, xmlFile))

    os.system("/scripts/neo4j/Neo4jQuery.sh %s \
    /tmp/neo4j_Query.gdb.hot %s \
    /var/log/neo4j/query_hot_logs.log /scripts/neo4j/Neo4jQueryHot.groovy" % (runs, xmlFile))


    #logger.info("Gathering the info and putting it in a csv file")
    #gather_data_graph_dms("g_neo4j")
    logger.info("*"*80)


def r_monet():

    pass

def r_jena(runs, queryLocation, dataFile):
    """This function is used to run the Jena DMS without perf tool.
    runs : THe number of runs
    queryLocation : The location of the sparql queries which would be run
    dataFile : The location of the datafile.
    """

    logger.info("*"*80)
    logger.info("Running the scripts for the Jena DMS")
    logger.info("Runs = %s, queryLocations = %s, dataFile = %s" % (runs, queryLocation, dataFile))

    logger.info("Running the command : /scripts/jena/JenaTDBLoad.sh /tmp jena_graph \
    %s /var/log/jena/load_logs.log %s" % (dataFile, runs))
 
    #Load the database
    os.system("/scripts/jena/JenaTDBLoad.sh /tmp jena_graph \
    %s /var/log/jena/load_logs.log %s" % (dataFile, runs))
    
    logger.info("Running the command : /scripts/jena/JenaTDBExecuteHotCache.sh /tmp jena_graph_hot \
    %s %s /var/log/jena/query_hot_logs.log %s" % (dataFile, queryLocation, runs))

    #Run the query
    os.system("/scripts/jena/JenaTDBExecuteHotCache.sh /tmp jena_graph_hot \
    %s %s /var/log/jena/query_hot_logs.log %s" % (dataFile, queryLocation, runs))

    logger.info("Running the command : /scripts/jena/JenaTDBExecuteColdCache.sh /tmp jena_graph_cold \
    %s %s /var/log/jena/query_cold_logs.log %s" % (dataFile, queryLocation, runs))

    #Run the query
    os.system("/scripts/jena/JenaTDBExecuteColdCache.sh /tmp jena_graph_cold \
    %s %s /var/log/jena/query_cold_logs.log %s" % (dataFile, queryLocation, runs))

    #logger.info("Gathering the info and putting it in a csv file")        
    #gather_data_rdf_dms('r_jena')
    logger.info("*"*80)


def r_arq():
    pass


def r_jena_with_perf(runs, queryLocation, dataFile):
    """This function is used to run the Jena DMS with perf tool.
    runs : THe number of runs
    queryLocation : The location of the sparql queries which would be run
    dataFile : The location of the datafile.
    """

    logger.info("*"*80)
    logger.info("Running the scripts for the Jena DMS with Perf")
    logger.info("Runs = %s, queryLocations = %s, dataFile = %s" % (runs, queryLocation, dataFile))

    
    logger.info("Running the loading scripts for the Jena DMS")
    # Running the loads
    for each in range(runs):
        command = "/scripts/jena/JenaTDBLoadPerf.sh /tmp jena_graph_%s %s /var/log/jena/load_logs.log" % (str(each), dataFile)
        run_perf(command, "/var/log/jena/load_log_perf.log", clear_cache = True)

    subprocess.call("ls /tmp/", shell = True)
    subprocess.call("rm -r /tmp/*", shell = True)

    command = "/scripts/jena/JenaTDBLoadPerf.sh /tmp jena_graph_hot %s /dev/null" % (dataFile)
    subprocess.call(command, shell = True)    

    logger.info("Running the queries for the Jena DMS on hot cache")
    m = glob.glob(queryLocation + "/*.sparql")
    for each_command in m:
        name_of_file = each_command.split("/")[-1].split(".")[0]
        subprocess.call("echo %s >> /var/log/jena/query_hot_logs.log" % (name_of_file), shell = True)
        for each in range(runs):
            command = "/scripts/jena/JenaTDBExecuteHotCachePerf.sh /tmp jena_graph_hot /var/log/jena/query_hot_logs.log %s" % (each_command)
            run_perf(command, "/var/log/jena/query_hot_logs_perf.log.%s" %(name_of_file))

    subprocess.call("rm -r /tmp/*", shell = True)

    command = "/scripts/jena/JenaTDBLoadPerf.sh /tmp jena_graph_cold %s /dev/null" % (dataFile)
    subprocess.call(command, shell = True)    

    logger.info("Running the queries for the Jena DMS on cold cache")
    m = glob.glob(queryLocation + "/*.sparql")
    for each_command in m:
        name_of_file = each_command.split("/")[-1].split(".")[0]
        subprocess.call("echo %s >> /var/log/jena/query_cold_logs.log" % (name_of_file), shell = True)
        for each in range(runs):
            command = "/scripts/jena/JenaTDBExecuteColdCachePerf.sh /tmp jena_graph_cold /var/log/jena/query_cold_logs.log %s" % (each_command)
            run_perf(command, "/var/log/jena/query_cold_logs_perf.log.%s" %(name_of_file))


def r_virtuoso(runs, queryLocation, dataFileLocation):
    """This function is used to run the Openlink Virtuoso DMS without perf tool.
    runs : THe number of runs
    queryLocation : The location of the sparql queries which would be run
    dataFileLocation : The location of the datafile.
    """

    logger.info("*"*80)
    logger.info("Running the scripts for the Virtuoso DMS")
    logger.info("Runs = %s, queryLocations = %s, dataFile = %s" \
            % (runs, queryLocation, dataFileLocation))

    logger.info("Running the setup_ini.py script to get the configurations ready")
    logger.info("The command is python3 /scripts/virtuoso/setup_ini.py -l /scripts/virtuoso \
            -df %s -qf %s" % (dataFileLocation, queryLocation))
    # All the files which match *.ttl in the dataFile location, would be loaded
    os.system("python3 /scripts/virtuoso/setup_ini.py -l /scripts/virtuoso -df \
            %s -qf %s" % (dataFileLocation, queryLocation))
    
    logger.info("Starting the virtuoso server")
    # Starting the server
    os.system("cd /scripts/virtuoso && /usr/local/virtuoso-opensource/bin/virtuoso-t -f /scripts/virtuoso/ &")
    time.sleep(30)

    logger.info("Runing the command /scripts/virtuoso/virtuoso_load.sh \
    /usr/local/virtuoso-opensource/bin/isql /var/log/virtuoso/load_logs.log %s" %(runs))     
    # Running the loads
    os.system("/scripts/virtuoso/virtuoso_load.sh /usr/local/virtuoso-opensource/bin/isql /var/log/virtuoso/load_logs.log %s" %(runs))    
    
    logger.info("Runing the command /scripts/virtuoso/virtuoso_execute_cold.sh \
    /usr/local/virtuoso-opensource/bin/isql /var/log/virtuoso/query_cold_logs.log %s %s" % (queryLocation, runs))
    # Running the queries
    os.system("/scripts/virtuoso/virtuoso_execute_cold.sh /usr/local/virtuoso-opensource/bin/isql /var/log/virtuoso/query_cold_logs.log %s %s" % (queryLocation, runs))    

    logger.info("Runing the command /scripts/virtuoso/virtuoso_execute_hot.sh \
    /usr/local/virtuoso-opensource/bin/isql /var/log/virtuoso/query_hot_logs.log %s %s" % (queryLocation, runs))
    # Running the queries
    os.system("/scripts/virtuoso/virtuoso_execute_hot.sh /usr/local/virtuoso-opensource/bin/isql /var/log/virtuoso/query_hot_logs.log %s %s" % (queryLocation, runs))    

    
    logger.info("Gathering the info and putting it in a csv file")        
    #gather_data_rdf_dms('r_virtuoso')    
    #logger.info("*"*80)

def r_virtuoso_with_perf(runs, queryLocation, dataFileLocation):
    """This function is used to run the Openlink Virtuoso DMS with perf tool.
    runs : THe number of runs
    queryLocation : The location of the sparql queries which would be run
    dataFileLocation : The location of the datafile.
    """

    logger.info("*"*80)
    logger.info("Running the scripts for the Virtuoso DMS with perf")
    logger.info("Runs = %s, queryLocations = %s, dataFile = %s" \
            % (runs, queryLocation, dataFileLocation))

    logger.info("Running the setup_ini.py script to get the configurations ready")
    logger.info("The command is python3 /scripts/virtuoso/setup_ini.py -l /scripts/virtuoso \
            -df %s -qf %s" % (dataFileLocation, queryLocation))
    # All the files which match *.ttl in the dataFile location, would be loaded
    os.system("python3 /scripts/virtuoso/setup_ini.py -l /scripts/virtuoso -df \
            %s -qf %s" % (dataFileLocation, queryLocation))
    
    logger.info("Starting the virtuoso server")
    # Starting the server
    os.system("cd /scripts/virtuoso && /usr/local/virtuoso-opensource/bin/virtuoso-t -f /scripts/virtuoso/ &")
    time.sleep(30)

    logger.info("Running the loading scripts for the Virtuoso DMS")
    for each in range(runs):
        # Running the loads
        prelogue = "/usr/local/virtuoso-opensource/bin/isql 1111 dba dba /scripts/virtuoso/prepare.sql> /dev/null 2>> /dev/null;"
        command = "/scripts/virtuoso/virtuoso_load_perf.sh /usr/local/virtuoso-opensource/bin/isql /var/log/virtuoso/load_logs.log"
        epilogue = "/usr/local/virtuoso-opensource/bin/isql 1111 dba dba /scripts/virtuoso/clear.sql> /dev/null 2>> /dev/null;"
        run_perf(command, "/var/log/virtuoso/load_log_perf.log", clear_cache = True, prelogue = prelogue, epilogue = epilogue)

    prelogue = "/usr/local/virtuoso-opensource/bin/isql 1111 dba dba /scripts/virtuoso/prepare.sql> /dev/null 2>> /dev/null;"
    command = "/scripts/virtuoso/virtuoso_load.sh /usr/local/virtuoso-opensource/bin/isql /dev/null"
    subprocess.call(prelogue, shell = True)
    subprocess.call(command, shell = True)

    logger.info("Running the queries for the Virtuoso DMS on hot cache")
    m = glob.glob(queryLocation + "/*.sparql")
    for each_command in m:
        name_of_file = each_command.split("/")[-1].split(".")[0]
        subprocess.call("echo %s >> /var/log/virtuoso/query_hot_logs.log" % (name_of_file), shell = True)
        for each in range(runs):
            command = "/scripts/virtuoso/virtuoso_execute_hot_perf.sh /usr/local/virtuoso-opensource/bin/isql /var/log/virtuoso/query_hot_logs.log %s" % (each_command)
            run_perf(command, "/var/log/virtuoso/query_hot_logs_perf.log.%s" %(name_of_file))

    logger.info("Running the queries for the Virtuoso DMS on cold cache")
    m = glob.glob(queryLocation + "/*.sparql")
    for each_command in m:
        name_of_file = each_command.split("/")[-1].split(".")[0]
        subprocess.call("echo %s >> /var/log/virtuoso/query_cold_logs.log" % (name_of_file), shell = True)
        for each in range(runs):
            command = "/scripts/virtuoso/virtuoso_execute_cold_perf.sh /usr/local/virtuoso-opensource/bin/isql /var/log/virtuoso/query_cold_logs.log %s" % (each_command)
            run_perf(command, "/var/log/virtuoso/query_cold_logs_perf.log.%s" %(name_of_file), clear_cache = True)

    
    #gather_data_rdf_dms('r_virtuoso')    
    #logger.info("*"*80)


def create_log_files(list_to_benchmark):
    """This function is used to create empty log files.
    list_to_benchmark : list of DMS that would be benchmarked."""
    logger.info("*"*80)
    logger.info("Creating empty log files for all the DMS")
    for each in list_to_benchmark:
        os.system('touch %s' % ('/var/log/' + directory_maps[each] + '/load_logs.log'))
        os.system('touch %s' % ('/var/log/' + directory_maps[each] + '/query_cold_logs.log'))
        os.system('touch %s' % ('/var/log/' + directory_maps[each] + '/query_hot_logs.log'))
        os.system('touch %s' % ('/var/log/' + directory_maps[each] + '/index_logs.log'))

    logger.info("Created empty log files for all the DMS")
    logger.info("*"*80)

def foo(list_to_benchmark, runs = 10):
    #create_log_files(list_to_benchmark)    
    print(list_to_benchmark)
    pass

def write_csv_file(csv_list, filename):
    """Dunction is not being used anywhere"""    
    file_handler = open(filename, "w")
    for each in csv_list:
        file_handler.write(",".join(each) + "\n");
    file_handler.close()

def get_name_of_file(file_location):
    """Returns the name of the file given the entire path"""
    try:
        return file_location.split("/")[-1]
    except Exception as e:
        return file_location

def generate_rdf_queries(rdf_query_location):
    """This function will generate SPARQL query file for the 
    Virtuoso RDF Model and the Apache Jena
    rdf_query_location : Where the initial Sparql Queries are provided by the user"""
    logger.info("*"*80)
    logger.info("Creating rdf query files from queries present at %s \
        for Jena (/jena_queries) and Virtuoso (/virtuoso_queries)" % (rdf_query_location))
    os.mkdir("/virtuoso_queries")
    os.mkdir("/jena_queries")
    all_sparql = glob.glob(rdf_query_location + "/*.sparql")
    for each in all_sparql:
        new_file = open("/virtuoso_queries/" + get_name_of_file(each), "w")
        original_file = open(each, "r").read()
        new_file.write("SPARQL;\n")
        new_file.write(original_file)
        new_file.close()
        apache_file = open("/jena_queries/" + get_name_of_file(each), "w")
        apache_file.write(original_file)
        apache_file.close()
    logger.info("Created rdf query files from queries present at %s \
        for Jena (/jena_queries) and Virtuoso (/virtuoso_queries)" % (rdf_query_location))
    logger.info("*"*80)

def generate_graph_queries_perf(gremlin_query_location_cold, gremlin_query_location_hot = None):
    """This function will generate the custom groovy files for all 
        the four graph based dbs for analysis with perf tool.
        gremlin_query_location_cold : The location where the query file for cold cache needs to be generated.        
        gremlin_query_location_hot : The location where the query file for hot cache needs to be generated.        
        """
    if gremlin_query_location_hot is None:
        gremlin_query_location_hot = gremlin_query_location_cold
    logger.info("*"*80)
    logger.info("Creating gremlin query files from gremlin_cold.groovy file present at %s \
        for Gremlin cold cache for Orient, Tinker, Neo4j and Sparksee" % (gremlin_query_location_cold))
    gremlin_queries = open(gremlin_query_location_cold, "r").read()
    sparksee_filehandler = open("/scripts/sparksee/SparkseeQueryColdPerf.groovy", "w")
    sparksee_filehandler.write("""import com.tinkerpop.blueprints.impls.sparksee.*

x = new SparkseeGraph(args[0])
println "===============Loading the Graph Model============"
loadModel = System.currentTimeMillis()
x.loadGraphML(args[1])
println "Time taken to load the graph Model:" + (System.currentTimeMillis() - loadModel)
println "===============Graph Model Loaded============"
x.V.count();
println "Dataset is " + args[1]
println "==============Running The Queries=========="
""")
    sparksee_filehandler.write(gremlin_queries)
    sparksee_filehandler.write("\nx.shutdown()");
    sparksee_filehandler.close()

    tinker_filehandler = open("/scripts/tinker/TinkerQueryColdPerf.groovy", "w")
    tinker_filehandler.write("""x = new TinkerGraph(args[0])
println "===============Loading the Graph Model============"
loadModel = System.currentTimeMillis()
x.loadGraphML(args[1])
println "Time taken to load the graph Model:" + (System.currentTimeMillis() - loadModel)
println "===============Graph Model Loaded============"
x.V.count();
println "Dataset is " + args[1]
println "==============Running The Queries=========="
""")
    tinker_filehandler.write(gremlin_queries)
    tinker_filehandler.write("\nx.shutdown()");
    tinker_filehandler.close()


    neo4j_filehandler = open("/scripts/neo4j/Neo4jQueryColdPerf.groovy", "w")
    neo4j_filehandler.write("""x = new Neo4jGraph(args[0])
println "===============Loading the Graph Model============"
loadModel = System.currentTimeMillis()
x.loadGraphML(args[1])
println "Time taken to load the graph Model:" + (System.currentTimeMillis() - loadModel)
println "===============Graph Model Loaded============"
x.V.count();
println "==============Starting to Run The Queries=========="
""");
    neo4j_filehandler.write(gremlin_queries)
    neo4j_filehandler.write("\nx.shutdown()")
    neo4j_filehandler.close()    

    orient_filehandler = open("/scripts/orient/OrientQueryColdPerf.groovy", "w")
    orient_filehandler.write("""println "===============Loading the Graph Model============"
loadModel = System.currentTimeMillis()
x = new OrientGraph("memory:"+args[0])
x.loadGraphML(args[1])
println "Time taken to load the graph Model:" + (System.currentTimeMillis() - loadModel)
println "===============Graph Model Loaded============"
x.V.count();
println "==============Starting to Run The Queries=========="
""")
    orient_filehandler.write(gremlin_queries)
    orient_filehandler.write("\nx.shutdown()")
    orient_filehandler.close()



    gremlin_queries = open(gremlin_query_location_hot, "r").read()
    sparksee_filehandler = open("/scripts/sparksee/SparkseeQueryHotPerf.groovy", "w")
    sparksee_filehandler.write("""import com.tinkerpop.blueprints.impls.sparksee.*

x = new SparkseeGraph(args[0])
println "===============Loading the Graph Model============"
loadModel = System.currentTimeMillis()
x.loadGraphML(args[1])
println "Time taken to load the graph Model:" + (System.currentTimeMillis() - loadModel)
println "===============Graph Model Loaded============"
x.V.count();
println "Dataset is " + args[1]
println "==============Running The Queries=========="
""")
    sparksee_filehandler.write(gremlin_queries)
    sparksee_filehandler.write("\nx.shutdown()");
    sparksee_filehandler.close()


    tinker_filehandler = open("/scripts/tinker/TinkerQueryHotPerf.groovy", "w")
    tinker_filehandler.write("""
x = new TinkerGraph(args[0])
println "===============Loading the Graph Model============"
loadModel = System.currentTimeMillis()
x.loadGraphML(args[1])
println "Time taken to load the graph Model:" + (System.currentTimeMillis() - loadModel)
println "===============Graph Model Loaded============"
x.V.count();
println "Dataset is " + args[1]
println "==============Running The Queries=========="
""")
    tinker_filehandler.write(gremlin_queries)
    tinker_filehandler.write("\nx.shutdown()");
    tinker_filehandler.close()

    neo4j_filehandler = open("/scripts/neo4j/Neo4jQueryHotPerf.groovy", "w")
    neo4j_filehandler.write("""x = new Neo4jGraph(args[0])
println "===============Loading the Graph Model============"
loadModel = System.currentTimeMillis()
x.loadGraphML(args[1])
println "Time taken to load the graph Model:" + (System.currentTimeMillis() - loadModel)
println "===============Graph Model Loaded============"
x.V.count();

println "==============Starting to Run The Queries=========="
""");
    neo4j_filehandler.write(gremlin_queries)
    neo4j_filehandler.write("\nx.shutdown()")
    neo4j_filehandler.close()    

    orient_filehandler = open("/scripts/orient/OrientQueryHotPerf.groovy", "w")
    orient_filehandler.write("""println "===============Loading the Graph Model============"
loadModel = System.currentTimeMillis()
x = new OrientGraph("memory:"+args[0])
x.loadGraphML(args[1])
println "Time taken to load the graph Model:" + (System.currentTimeMillis() - loadModel)
println "===============Graph Model Loaded============"
x.V.count();

println "==============Starting to Run The Queries=========="
""")
    orient_filehandler.write(gremlin_queries)
    orient_filehandler.write("\nx.shutdown()")
    orient_filehandler.close()

    logger.info("*"*80)

def generate_graph_queries(gremlin_query_location_cold, gremlin_query_location_hot = None):
    """This function will generate the custom groovy files for all 
        the graph based dbs
        gremlin_query_location_cold : The location where the query file for cold cache needs to be generated.        
        gremlin_query_location_hot : The location where the query file for hot cache needs to be generated.        
        """

    if gremlin_query_location_hot is None:
        gremlin_query_location_hot = gremlin_query_location_cold
    logger.info("*"*80)
    logger.info("Creating gremlin query files from gremlin_cold.groovy file present at %s \
        for Gremlin cold cache for Orient, Tinker, Neo4j and Sparksee" % (gremlin_query_location_cold))
    
    gremlin_queries = open(gremlin_query_location_cold, "r").read()
    sparksee_filehandler = open("/scripts/sparksee/SparkseeQueryCold.groovy", "w")
    sparksee_filehandler.write("""import com.tinkerpop.blueprints.impls.sparksee.*

x = new SparkseeGraph(args[0])
println "===============Loading the Graph Model============"
loadModel = System.currentTimeMillis()
x.loadGraphML(args[1])
println "Time taken to load the graph Model:" + (System.currentTimeMillis() - loadModel)
println "===============Graph Model Loaded============"
x.V.count();
println "Dataset is " + args[1]
no_of_times = Integer.parseInt(args[2])
println "==============Running The Queries=========="
for (i in 1..no_of_times) {
    println "################Run "+i+"##################"
""")
    sparksee_filehandler.write(gremlin_queries)
    sparksee_filehandler.write("""}
x.shutdown()""");
    sparksee_filehandler.close()

    tinker_filehandler = open("/scripts/tinker/TinkerQueryCold.groovy", "w")
    tinker_filehandler.write("""x = new TinkerGraph(args[0])
println "===============Loading the Graph Model============"
loadModel = System.currentTimeMillis()
x.loadGraphML(args[1])
println "Time taken to load the graph Model:" + (System.currentTimeMillis() - loadModel)
println "===============Graph Model Loaded============"
x.V.count();
println "Dataset is " + args[1]
no_of_times = Integer.parseInt(args[2])
println "==============Running The Queries=========="
for (i in 1..no_of_times) {
    println "################Run "+i+"##################"
""")
    tinker_filehandler.write(gremlin_queries)
    tinker_filehandler.write("""}
x.shutdown()""");
    tinker_filehandler.close()


    neo4j_filehandler = open("/scripts/neo4j/Neo4jQueryCold.groovy", "w")
    neo4j_filehandler.write("""x = new Neo4jGraph(args[0])
println "===============Loading the Graph Model============"
loadModel = System.currentTimeMillis()
x.loadGraphML(args[1])
println "Time taken to load the graph Model:" + (System.currentTimeMillis() - loadModel)
println "===============Graph Model Loaded============"
x.V.count();

no_of_times = Integer.parseInt(args[2])
println "==============Starting to Run The Queries=========="
for (i in 1..no_of_times) {
    println "################Run "+i+"##################"
""");
    neo4j_filehandler.write(gremlin_queries)
    neo4j_filehandler.write("""}
x.shutdown()""")
    neo4j_filehandler.close()    

    orient_filehandler = open("/scripts/orient/OrientQueryCold.groovy", "w")
    orient_filehandler.write("""println "===============Loading the Graph Model============"
loadModel = System.currentTimeMillis()
x = new OrientGraph("memory:"+args[0])
x.loadGraphML(args[1])
println "Time taken to load the graph Model:" + (System.currentTimeMillis() - loadModel)
println "===============Graph Model Loaded============"
x.V.count();

no_of_times = Integer.parseInt(args[2])
println "==============Starting to Run The Queries=========="
for (i in 1..no_of_times) {
    println "################Run "+i+"##################"
""")
    orient_filehandler.write(gremlin_queries)
    orient_filehandler.write("""}
x.shutdown()""")
    orient_filehandler.close()


    gremlin_queries = open(gremlin_query_location_hot, "r").read()
    sparksee_filehandler = open("/scripts/sparksee/SparkseeQueryHot.groovy", "w")
    sparksee_filehandler.write("""import com.tinkerpop.blueprints.impls.sparksee.*

x = new SparkseeGraph(args[0])
println "===============Loading the Graph Model============"
loadModel = System.currentTimeMillis()
x.loadGraphML(args[1])
println "Time taken to load the graph Model:" + (System.currentTimeMillis() - loadModel)
println "===============Graph Model Loaded============"
x.V.count();
println "Dataset is " + args[1]
no_of_times = Integer.parseInt(args[2])
println "==============Running The Queries=========="
for (i in 1..no_of_times) {
    println "################Run "+i+"##################"
""")
    sparksee_filehandler.write(gremlin_queries)
    sparksee_filehandler.write("""}
x.shutdown()""");
    sparksee_filehandler.close()


    tinker_filehandler = open("/scripts/tinker/TinkerQueryHot.groovy", "w")
    tinker_filehandler.write("""
x = new TinkerGraph(args[0])
println "===============Loading the Graph Model============"
loadModel = System.currentTimeMillis()
x.loadGraphML(args[1])
println "Time taken to load the graph Model:" + (System.currentTimeMillis() - loadModel)
println "===============Graph Model Loaded============"
x.V.count();
println "Dataset is " + args[1]
no_of_times = Integer.parseInt(args[2])
println "==============Running The Queries=========="
for (i in 1..no_of_times) {
    println "################Run "+i+"##################"
""")
    tinker_filehandler.write(gremlin_queries)
    tinker_filehandler.write("""}
x.shutdown()""");
    tinker_filehandler.close()

    neo4j_filehandler = open("/scripts/neo4j/Neo4jQueryHot.groovy", "w")
    neo4j_filehandler.write("""x = new Neo4jGraph(args[0])
println "===============Loading the Graph Model============"
loadModel = System.currentTimeMillis()
x.loadGraphML(args[1])
println "Time taken to load the graph Model:" + (System.currentTimeMillis() - loadModel)
println "===============Graph Model Loaded============"
x.V.count();

no_of_times = Integer.parseInt(args[2])
println "==============Starting to Run The Queries=========="
for (i in 1..no_of_times) {
    println "################Run "+i+"##################"
""");
    neo4j_filehandler.write(gremlin_queries)
    neo4j_filehandler.write("""}
x.shutdown()""")
    neo4j_filehandler.close()    

    orient_filehandler = open("/scripts/orient/OrientQueryHot.groovy", "w")
    orient_filehandler.write("""println "===============Loading the Graph Model============"
loadModel = System.currentTimeMillis()
x = new OrientGraph("memory:"+args[0])
x.loadGraphML(args[1])
println "Time taken to load the graph Model:" + (System.currentTimeMillis() - loadModel)
println "===============Graph Model Loaded============"
x.V.count();

no_of_times = Integer.parseInt(args[2])
println "==============Starting to Run The Queries=========="
for (i in 1..no_of_times) {
    println "################Run "+i+"##################"
""")
    orient_filehandler.write(gremlin_queries)
    orient_filehandler.write("""}
x.shutdown()""")
    orient_filehandler.close()




    logger.info("Creating gremlin query files from gremlin_hot.groovy file present at %s \
        for Hot Cache for Orient, Neo4j and Sparksee" % (gremlin_query_location_hot))



    logger.info("*"*80)

def generate_gremlin_query_for_perf(graph_queries_directory):
    """This function generates individual groovy file for each query to
    run them using the perf based tool for all the graph based DMS.
    graph_queries_directory : This is the initial location where all the gremlin queries 
                            are provided by the user in individual files."""

    if graph_queries_directory[-1] != "/":
        graph_queries_directory+="/"
    all_files = glob.glob(graph_queries_directory + "*.gremlin")
    
    for each in all_files:
        name_of_file = each.split("/")[-1].split(".")[0]
        base = "/gremlin_query_perf/"
        sparksee_filehandler = open(base + "sparksee_" + name_of_file + ".groovy", "w")
        sparksee_filehandler.write("""import com.tinkerpop.blueprints.impls.sparksee.*;
x = new SparkseeGraph("/tmp/sparksee_perf.gdb");\n""");
        sparksee_filehandler.write("""println "======Query %s======";
s = System.currentTimeMillis();\n"""%(name_of_file));
        sparksee_filehandler.write(open(each, "r").read() + "\n")
        sparksee_filehandler.write("println (System.currentTimeMillis() - s);")
        sparksee_filehandler.close()

        tinker_filehandler = open(base + "tinker_" + name_of_file + ".groovy", "w")
        tinker_filehandler.write('x = new TinkerGraph("/tmp/tinker_perf");\n')
        tinker_filehandler.write("""println "======Query %s======";
s = System.currentTimeMillis();\n"""%(name_of_file));
        tinker_filehandler.write(open(each, "r").read() + "\n")
        tinker_filehandler.write("println (System.currentTimeMillis() - s);")
        tinker_filehandler.close()

        neo4j_filehandler = open(base + "neo4j_" + name_of_file + ".groovy", "w")
        neo4j_filehandler.write('x = new Neo4jGraph("/tmp/neo4j_perf");\n')
        neo4j_filehandler.write("""println "======Query %s======";
s = System.currentTimeMillis();\n"""%(name_of_file));
        neo4j_filehandler.write(open(each, "r").read())
        neo4j_filehandler.write("println (System.currentTimeMillis() - s);\n")
        neo4j_filehandler.write("System.exit(0);")
        neo4j_filehandler.close()

        orient_filehandler = open(base + "orient_" + name_of_file + ".groovy", "w")
        orient_filehandler.write('x = new OrientGraph("memory:/orient_perf");\n')
        orient_filehandler.write("println('======Query %s======');\n"%(name_of_file));
        orient_filehandler.write("s = System.currentTimeMillis();\n");
        orient_filehandler.write(open(each, "r").read().strip("\r\n").strip("\n\r"))
        orient_filehandler.write('println (System.currentTimeMillis() - s) ;\n')
        orient_filehandler.close()

def sanity_checks(args):
    """This function runs a few sanity checks before running the software.
    args : The dictionary of the cli arguments which are provided to the script."""
    
    logger.info("*"*80)
    logger.info("Running the sanity checks")
    is_sane = True
    if not os.path.exists(args["graph_datafile"]):
        print("Incorrect Path.")
        logger.error("Incorrect path to the graph_datafile argument")
        return False
    else:
        s = glob.glob(args["graph_datafile"] + "/*")
        if len(s)!=1:
            print("Please make sure there is only one file in the specified \
                graph_datafile directory")
            logger.error("There has to be only one Graphml file in the directory which is \
                given as an argument to the graph_datafile argument")
            return False
    logger.info("graph_datafile argument is valid")

    if not os.path.exists(args["rdf_datafile"]):
        logger.error("Incorrect directory supplied to the rdf_datafile argument")
        print("The directory does not exist")  
    else:
        s = glob.glob(args["graph_datafile"] + "/*")
        if len(s)!=1:
            print("Please make sure there is only one file in the specified \
                rdf_datafile directory")
            logger.error("There has to be only one Graphml file in the directory which is \
                given as an argument to the graph_datafile argument")

            return False
    logger.info("rdf_datafile argument is valid")
  
        
    if not os.path.exists(args["graph_queries"]):
        print("The graph query file does not exist")
        logger.error("The directory supplied as an argument to graph_queries \
                argument does not exist")
        return False
    else:
        s = glob.glob(args["graph_queries"]+"/gremlin.groovy.*")
        if len(s)!=2:
            print("Please make sure that the file gremlin.groovy.hot_cache and \
                    gremlin.groovy.cold_cache is present in the dataset")
            logger.error("The directory supplied as an argument needs to have \
            two files with the name gremlin.groovy.hot_cache and gremlin.groovy.cold_cache")

            return False

    logger.info("graph_queries argument is valid")

    if not os.path.exists(args["rdf_queries"]):
        logger.error("The directory supplied as an argument to rdf_queries \
                argument does not exist")
        print("The Sparql queries do not exist")
    else:
        s = glob.glob(args["rdf_queries"]+ "/*.sparql")
        if len(s) == 0:
            logger.error("Could not find any sparql queries in the path which\
            was given as an argument to rdf_queries")
            print("No sparql files exist")
            return False
    
    logger.info("rdf_queries argument is valid")
    logger.info("All the arguments are valid") 
    return True

def process_perf_file(file_name, csv_list, dms, action, query_number):
    """This function processes a single perf log file.
    file_name : Name of the perf log file.
    csv_list : This is a list which has all the lists.
    dms : The name of the DMS.    
    action : Whether it is a load action or a query action.
    query_number : If it is a query action, then the query number.
    """    
    q = open(file_name, "r")
    all_lines = q.readlines()
    run_id = 1
    not_supported = []
    csv_list_2 = []
    l = [dms, action, query_number, str(run_id)]
    for each in all_lines[1:]:
        if each[0] == "#":
            l = [dms, action, query_number, str(run_id)]
            for each in csv_list_2:
                l.append(each[1])
            csv_list.append(l)
            run_id+=1
            csv_list_2 = []
        else:
            s = re.findall(r"[0-9\.\,]+      [a-zA-Z0-9\-]+", each)
            if len(s)!=0:
                value, key = s[0].split("      ")
                value = value.replace(",", "")
                value = float(value)
                csv_list_2.append([key, str(value)])
    l = [dms, action, query_number, str(run_id)]    
    for each in csv_list_2:
        l.append(each[1])
    csv_list.append(l)
    
    headers = ["DMS", "action", "query_number", "run_id"]
    for each in csv_list_2:
        headers.append(each[0])

    return csv_list, headers    


def process_perf_group(all_files, action_type, query_number):
    """This function process all the perf log files for a load operation or a single query.
    all_files : The list of all the files for the particular action.
    action : Whether it is a load action or a query action.
    query_number : If it is a query action, then the query number.
    """    
    dic_csv = {}
    dic_csv_headers = {}    
    for each in all_files:
        name_of_file = each.split("/")[-1]
        file_number = name_of_file.split(".")[-1]
        csv_list = []
        print(name_of_file)
        dms = each.split("/")[-2]
        temp_list, temp_headers = process_perf_file(each, csv_list, dms, action_type, query_number)
        dic_csv[file_number] = temp_list        
        dic_csv_headers[file_number] = temp_headers
    return dic_csv_headers, dic_csv

def process_all_perfs_dms(perf_directory, query_directory, query_search_string, graph_based):
    """This function process all the perf log files for the load operations and the 
        query operations for a given DMS.
    perf_directory : The directory where all the perf log files are stored.
    query_directory : The directory where all the queries are stored.
    query_search_string : The search string for the query files in the query directory.
    graph_based : This is a boolean which has a true value if it is a graph based DMS.
    """    

    headers = []
    
    if perf_directory[-1]!="/":
        perf_directory = perf_directory + "/"    

    all_files = glob.glob(perf_directory + "load_log_perf*")
    dic_load_headers, dic_load = process_perf_group(all_files, "load", "NA") 
    
    dic_hot_queries = {}
    dic_cold_queries = {}
    all_queries = glob.glob(query_directory +  query_search_string)
    print("\n"*5)    
    print("*********", query_directory +  query_search_string , "*************")    
    print("\n"*5)    
    for each in all_queries:
        name_of_file = None
        if graph_based:
            name_of_file = "_".join(each.split("/")[-1].split(".")[0].split("_")[1:])
        else:
            name_of_file = each.split("/")[-1].split(".")[0]
        print("*********", name_of_file, "*************")
        all_files = glob.glob(perf_directory + "query_hot_logs_perf.log.%s*" % (name_of_file))
        l,m = process_perf_group(all_files, "query_hot", name_of_file)
        dic_hot_queries[name_of_file] = m
        all_files = glob.glob(perf_directory + "query_cold_logs_perf.log.%s*" % (name_of_file))
        l,m = process_perf_group(all_files, "query_cold", name_of_file)
        dic_cold_queries[name_of_file] = m

    print(dic_load_headers)
    return (dic_load_headers, dic_load, dic_hot_queries, dic_cold_queries)

def generate_perf_csv_for_all_dms(type_of_dms, name_of_file):
    """This function process all the perf log files for the given types of DMS and stores
        it in a single csv file.
    type_of_dms : g_ for graph based DMS, and r_ in case of RDF based DMS.
    name_of_file : The name of the CSV file.
    """    

    f = open(name_of_file, "w")
    dic_all = {}
    graph_based = False
    if type_of_dms == "g_":
        graph_based = True
    find_header = None
    
    for each in directory_maps:
        if type_of_dms in each:
            dic_all[each] = process_all_perfs_dms("/var/log/%s/" % (directory_maps[each]), query_directory_maps[each], query_extension_maps[each], graph_based)
            find_header = each


    print(dic_all)
    dic_load_headers = dic_all[find_header][0]
    print(dic_load_headers)
    f.write(",".join(dic_load_headers['1']))
    f.write(",")
    for i in range(2,5):
        f.write(",".join(dic_load_headers[str(i)][4:]))
        if i == 4:
            continue
        f.write(",")
    f.write("\n")

    for each in dic_all:
        m = dic_all[each][1:]
        all_loads = m[0]
        for i in range(len(all_loads['1'])):
            f.write(",".join(all_loads['1'][i]))
            f.write(",")
            f.write(",".join(all_loads['2'][i][4:]))
            f.write(",")
            f.write(",".join(all_loads['3'][i][4:]))
            f.write(",")
            f.write(",".join(all_loads['4'][i][4:]))
            f.write("\n")
        
        all_hot = m[1]
        for each in all_hot:
            for i in range(len(all_hot[each]['1'])):
                print(all_hot[each])        
                f.write(",".join(all_hot[each]['1'][i]))
                f.write(",")
                f.write(",".join(all_hot[each]['2'][i][4:]))
                f.write(",")
                f.write(",".join(all_hot[each]['3'][i][4:]))
                f.write(",")
                f.write(",".join(all_hot[each]['4'][i][4:]))
                f.write("\n")

        all_cold = m[2]
        for each in all_cold:
            for i in range(len(all_cold[each]['1'])):        
                f.write(",".join(all_cold[each]['1'][i]))
                f.write(",")
                f.write(",".join(all_cold[each]['2'][i][4:]))
                f.write(",")
                f.write(",".join(all_cold[each]['3'][i][4:]))
                f.write(",")
                f.write(",".join(all_cold[each]['4'][i][4:]))
                f.write("\n")

    f.close()                       


def generate_perf_csv_for_all_graphs(name_of_file):
    """Redundant function. Not being used anywhere"""
    f = open(name_of_file, "w")
    dic_all = {}
    for each in directory_maps:
        if "g_" in each:
            dic_all[each] = process_all_perfs_graph_dms("/var/log/%s/" % (directory_maps[each]))

    dic_load_headers = dic_all["g_tinker"][0]
    f.write(",".join(dic_load_headers['1']))
    f.write(",")
    for i in range(2,5):
        f.write(",".join(dic_load_headers[str(i)][3:]))
        if i == 4:
            continue
        f.write(",")
    f.write("\n")

    for each in dic_all:
        m = dic_all[each][1:]
        for each in m:
            for i in range(len(each['1'])):
                f.write(",".join(each['1'][i]))
                f.write(",")
                f.write(",".join(each['2'][i][3:]))
                f.write(",")
                f.write(",".join(each['3'][i][3:]))
                f.write(",")
                f.write(",".join(each['4'][i][3:]))
                f.write("\n")
    f.close()                       

if __name__ == "__main__":
    logger.info("Litmus Benchmark Suite")
    parser = argparse.ArgumentParser(description='The Litmus Benchmark Suite')
    parser.add_argument('-gd', '--graph_datafile', help='The location of the Graph Database File', required = True)
    parser.add_argument('-rd', '--rdf_datafile', help='The location of the RDF Database File', required = True)
    parser.add_argument('-gq', '--graph_queries', help='The location of the Gremlin Queries', required = True)
    parser.add_argument('-rq', '--rdf_queries', help = 'The location of the Sparql Queries', required = True)    
    parser.add_argument('-v', '--verbose', action = "store_true", help = "Verbose", required = False)
    parser.add_argument('-a','--all', action = "store_true" , help='Run for all DMS', required=False)
    parser.add_argument('-g','--graph', action = "store_true", help='Run for all Graph Based DMS', required=False)
    parser.add_argument('-r','--rdf', action = "store_true", help='Run for all RDF Based DMS', required=False)
    parser.add_argument('-n', '--runs', help='Number of times, the experiment should be conducted', required = False)
    
    
    args = vars(parser.parse_args())
    if not sanity_checks(args):
        sys.exit(-1)
    
    final_list = None
    verbose = args['verbose']
    if args['all'] or (args['graph'] and args['rdf']):
        final_list = graph_based + rdf_based
        args['graph'] = True
        args['rdf'] = True
    elif args['graph']:
        final_list = graph_based 
    elif args['rdf']:
        final_list = rdf_based
    else:
        final_list = graph_based + rdf_based
    total_runs = None 
    try:
        total_runs = int(args['runs'])
    except Exception as e:
        total_runs = 5
    #foo(final_list, runs = total_runs)
    logger.info("Runs = %d,  Graph_Data_Location = %s, \
                Graph_query_Location = %s, \
                RDF_Data_Location = %s, \
                RDF_Query_Location = %s." 
        % (total_runs, args['graph_datafile'], args['graph_queries'], args['rdf_datafile'], args['rdf_queries']))
    
    create_log_files(final_list)
    

    if args['graph']:
        generate_graph_queries(args['graph_queries']+"/gremlin.groovy.cold_cache", \
                args['graph_queries']+"/gremlin.groovy.hot_cache")
        generate_graph_queries_perf(args['graph_queries']+"/gremlin.groovy.cold_cache", \
                args['graph_queries']+"/gremlin.groovy.hot_cache")
        generate_gremlin_query_for_perf(args['graph_queries'])
        name_of_graph = glob.glob(args['graph_datafile'] + "/*")
        name_of_graph = name_of_graph[0]
#        g_sparksee(total_runs, name_of_graph)
        g_neo4j_with_perf(total_runs, name_of_graph)
#        g_neo4j(total_runs, name_of_graph)
        print("Called the function")
        print("Please run")        
#        g_sparksee_with_perf(1, name_of_graph)
#        g_tinker_with_perf(1, name_of_graph)
        directory_maps = {'g_neo4j' : 'neo4j'}
        generate_perf_csv_for_all_dms("g_", "temp_graph.csv")
#        generate_perf_csv_for_all_graphs("temp.csv")
#        create_csv_from_logs("graph.load.logs", "graph.query.logs", graph_based, True)
    if args["rdf"]:
        generate_rdf_queries(args['rdf_queries'])
        name_of_graph = glob.glob(args['rdf_datafile'] + "/*.ttl")
        name_of_graph = name_of_graph[0]

#        r_virtuoso(total_runs, "/virtuoso_queries", args['rdf_datafile'])
        directory_maps = {'r_jena' : 'jena'}

        r_jena_with_perf(1, '/jena_queries', name_of_graph)
        generate_perf_csv_for_all_dms("r_", "temp_rdf.csv")
        #r_rdf3x_with_perf(1, args['rdf_queries'], name_of_graph)
        #r_virtuoso_with_perf(1, "/virtuoso_queries" , name_of_graph)
        #r_rdf3x(total_runs, args['rdf_queries'], name_of_graph)
#        r_jena(total_runs, "/jena_queries", name_of_graph)
        #create_csv_from_logs("rdf.load.logs", "rdf.query.logs", rdf_based, False)


