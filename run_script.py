import argparse
import os
import glob
import sys
import time
graph_based = ['g_sparksee', 'g_orient', 'g_neo4j' ]

rdf_based = ['r_rdf3x', 'r_monet', 'r_jena', 'r_arq', 'r_virtuoso' ]

directory_maps = { \
    'g_sparksee':'sparksee', \
    'g_orient' : 'orient', \
    'g_neo4j' : 'neo4j', \
    'r_rdf3x' : 'rdf3x', \
    'r_monet' : 'monet', \
    'r_jena' : 'jena', \
    'r_arq' : 'arq', \
    'r_virtuoso' : 'virtuoso'
    }


def gather_data_graph_dms(dms):
    #Gather the data and put it in a csv format
    csv_load = []
    file_handler = open("/var/log/%s/load_logs.log" % (directory_maps[dms]), "r")
    all_lines = file_handler.readlines()
    file_handler.close()
    run_id = 1
    for each in all_lines:
        try:
            csv_load.append([directory_maps[dms], str(run_id), "load", str(int(each.strip()))])
            run_id+=1
        except Exception as e:
            print(e)

    for each in csv_load:
        print(",".join(each))

    file_handler = open("/var/log/%s/query_logs.log" % (directory_maps[dms]), "r")
    all_lines = file_handler.readlines()[5:]
    file_handler.close()
    run_id = 0
    csv_query = []
    flag = True
    for each in all_lines:
        if each[0]=="#":
            run_id+=1
            flag = True
            continue;
        if flag:
            query_no = int(each.split("Query ")[1].split("=")[0])
            flag = False
        else:
            try:
                csv_query.append([directory_maps[dms], str(run_id), "query",\
                 str(query_no), str(int(each.strip()))])
                flag = True
            except Exception as e:
                print(e)
    
    for each in csv_query:
        print(",".join(each))

def gather_data_rdf_dms(dms):
    #Gather the data and put it in a csv format
    csv_load = []
    file_handler = open("/var/log/%s/load_logs.log" % (directory_maps[dms]), "r")
    all_lines = file_handler.readlines()
    file_handler.close()
    run_id = 1
    for each in all_lines:
        csv_load.append([directory_maps[dms], str(run_id), "load", \
            each.strip().split("\t")[2]])
        run_id+=1


    file_handler = open("/var/log/%s/query_logs.log" % (directory_maps[dms]), "r")
    all_lines = file_handler.readlines()
    file_handler.close()
    run_id = 0
    query_name = ""
    csv_query = []
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
            csv_query.append([directory_maps[dms], str(run_id), "query", query_name, \
                    each.strip().split("\t")[2]])

    
    for each in csv_load:
        print(",".join(each))
    for each in csv_query:
        print(",".join(each))


def g_sparksee(runs, xmlFile):
    #Loading the database
    os.system("/scripts/sparksee/SparkseeLoad.sh %s \
    /tmp/sparksee.gdb %s \
    /var/log/sparksee/load_logs.log" % (runs, xmlFile))

    #Querying the database
    os.system("/scripts/sparksee/SparkseeQuery.sh %s \
    /tmp/HelloWorld.gdb %s \
    /var/log/sparksee/query_logs.log" % (runs, xmlFile))

    #Gather the data and put it in a csv format
    gather_data_graph_dms("g_sparksee")

def r_rdf3x(runs, queryLocations, dataFile):
    #Loading the database
    os.system("/scripts/rdf3x/RDF3xLoad.sh %s /tmp rdf3x_graph \
    %s /var/log/rdf3x/load_logs.log" % (runs, dataFile)) 
    
    #Querying the database
    os.system("/scripts/rdf3x/RDF3xExecute.sh /tmp rdf3x_graph \
    %s %s /var/log/rdf3x/query_logs.log %s" % (dataFile, queryLocations, runs)) 
        
    gather_data_rdf_dms("r_rdf3x")

def g_orient(runs, xmlFile):
    #Loading the database
    os.system("/scripts/orient/OrientLoad.sh %s \
    /tmp/orient_load.gdb %s /scripts/orient/OrientLoad.groovy \
    /var/log/orient/load_logs.log" % (runs, xmlFile))

    #Querying the database
    os.system("/scripts/orient/OrientQuery.sh %s \
    /tmp/orient_query.gdb %s /scripts/orient/OrientQuery.groovy \
    /var/log/orient/query_logs.log" % (runs, xmlFile))

    gather_data_graph_dms("g_orient")



def g_neo4j(runs, xmlFile):
    #Loading the database
    os.system("/scripts/neo4j/Neo4jLoad.sh %s \
    /tmp/neo4j_load.gdb %s \
    /var/log/neo4j/load_logs.log" % (runs, xmlFile))

    #Querying the database
    os.system("/scripts/neo4j/Neo4jQuery.sh %s \
    /tmp/neo4j_Query.gdb %s \
    /var/log/neo4j/query_logs.log" % (runs, xmlFile))
    
    gather_data_graph_dms("g_neo4j")


def r_monet():

    pass

def r_jena(runs, queryLocation, dataFile):
    #Load the database
    os.system("/scripts/jena/JenaTDBLoad.sh /tmp/ jena_graph \
    %s /var/log/jena/load_logs.log %s" % (dataFile, runs))
    
    #Run the query
    os.system("/scripts/jena/JenaTDBExecute.sh /tmp/ jena_graph \
    %s %s /var/log/jena/query_logs.log %s" % (dataFile, queryLocation, runs))

    gather_data_rdf_dms('r_jena')

def r_arq():
    pass

def r_virtuoso(runs, queryLocation, dataFileLocation):
    # All the files which match *.ttl in the dataFile location, would be loaded
    os.system("python3 /scripts/virtuoso/setup_ini.py -l /scripts/virtuoso -df %s -qf %s" % (dataFileLocation, queryLocation))
    
    # Starting the server
    os.system("cd /scripts/virtuoso && /usr/local/virtuoso-opensource/bin/virtuoso-t -f /scripts/virtuoso/ &")
    time.sleep(30)
    # Running the loads
    os.system("/scripts/virtuoso/virtuoso_load.sh /usr/local/virtuoso-opensource/bin/isql /var/log/virtuoso/load_logs.log %s" %(runs))    
    # Running the queries
    os.system("/scripts/virtuoso/virtuoso_execute.sh /usr/local/virtuoso-opensource/bin/isql /var/log/virtuoso/query_logs.log %s %s" % (queryLocation, runs))    
    
    gather_data_rdf_dms('r_virtuoso')    

def create_log_files(list_to_benchmark):
    for each in list_to_benchmark:
        os.system('touch %s' % ('/var/log/' + directory_maps[each] + '/load_logs.log'))
        os.system('touch %s' % ('/var/log/' + directory_maps[each] + '/query_logs.log'))
        os.system('touch %s' % ('/var/log/' + directory_maps[each] + '/index_logs.log'))

def foo(list_to_benchmark, runs = 10):
    #create_log_files(list_to_benchmark)    
    print(list_to_benchmark)
    pass

def write_csv_file(csv_list, filename):
    file_handler = open(filename, "w")
    for each in csv_list:
        file_handler.write(",".join(each) + "\n");
    file_handler.close()

def get_name_of_file(file_location):
    try:
        return file_location.split("/")[-1]
    except Exception as e:
        return file_location

def generate_rdf_queries(rdf_query_location):
    """This function will generate SPARQL query file for the 
    Virtuoso RDF Model and the Apache Jena"""
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
        apache_file.write(original_file.split(";")[0])
        apache_file.close()

def generate_graph_queries(gremlin_query_location):
    """This function will generate the custom groovy files for all 
        the three graph based dbs"""
    
    gremlin_queries = open(gremlin_query_location, "r").read()
    sparksee_filehandler = open("/scripts/sparksee/SparkseeQuery.groovy", "w")
    sparksee_filehandler.write("""import com.tinkerpop.blueprints.impls.sparksee.*

x = new SparkseeGraph(args[0])
println "===============Loading the Graph Model============"
loadModel = System.currentTimeMillis()
x.loadGraphML(args[1])
println "Time taken to load the graph Model:" + (System.currentTimeMillis() - loadModel)
println "===============Graph Model Loaded============"

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

    neo4j_filehandler = open("/scripts/neo4j/Neo4jQuery.groovy", "w")
    neo4j_filehandler.write("""x = new Neo4jGraph(args[0])
println "===============Loading the Graph Model============"
loadModel = System.currentTimeMillis()
x.loadGraphML(args[1])
println "Time taken to load the graph Model:" + (System.currentTimeMillis() - loadModel)
println "===============Graph Model Loaded============"


no_of_times = Integer.parseInt(args[2])
println "==============Starting to Run The Queries=========="
for (i in 1..no_of_times) {
    println "################Run "+i+"##################"
""");
    neo4j_filehandler.write(gremlin_queries)
    neo4j_filehandler.write("""}
x.shutdown()""")
    neo4j_filehandler.close()    

    orient_filehandler = open("/scripts/orient/OrientQuery.groovy", "w")
    orient_filehandler.write("""println "===============Loading the Graph Model============"
loadModel = System.currentTimeMillis()
x = new OrientGraph("memory:"+args[0])
x.loadGraphML(args[1])
println "Time taken to load the graph Model:" + (System.currentTimeMillis() - loadModel)
println "===============Graph Model Loaded============"


no_of_times = Integer.parseInt(args[2])
println "==============Starting to Run The Queries=========="
for (i in 1..no_of_times) {
    println "################Run "+i+"##################"
""")
    orient_filehandler.write(gremlin_queries)
    orient_filehandler.write("""}
x.shutdown()""")
    orient_filehandler.close()

def sanity_checks(args):
    is_sane = True
    if not os.path.exists(args["graph_datafile"]):
        print("Incorrect Path.")
        return False
    else:
        s = glob.glob(args["graph_datafile"] + "/*")
        if len(s)!=1:
            print("Please make sure there is only one file in the specified graph_datafile directory")
            return False

    if not os.path.exists(args["rdf_datafile"]):
        print("The directory does not exist")  
    else:
        s = glob.glob(args["graph_datafile"] + "/*")
        if len(s)!=1:
            print("Please make sure there is only one file in the specified rdf_datafile directory")
            return False

   
        
    if not os.path.exists(args["graph_queries"]):
        print("The graph query file does not exist")
        return False
    else:
        s = glob.glob(args["graph_queries"]+"/gremlin.groovy")
        if len(s)!=1:
            print("Please make sure that the file gremlin.groovy is present in the dataset")
            return False

    if not os.path.exists(args["rdf_queries"]):
        print("The Sparql queries do not exist")
    else:
        s = glob.glob(args["rdf_queries"]+ "/*.sparql")
        if len(s) == 0:
            print("No sparql files exist")
            return False
    
    return True


if __name__ == "__main__":
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
    
    if args['graph']:
        generate_graph_queries(args['graph_queries']+"/gremlin.groovy")
        name_of_graph = glob.glob(args['graph_datafile'] + "/*")
        name_of_graph = name_of_graph[0]
        g_sparksee(total_runs, name_of_graph)
        g_orient(total_runs, name_of_graph)
        g_neo4j(total_runs, name_of_graph)
    if args["rdf"]:
        generate_rdf_queries(args['rdf_queries'])
        name_of_graph = glob.glob(args['rdf_datafile'] + "/*.ttl")
        name_of_graph = name_of_graph[0]
        create_log_files(final_list)
        r_virtuoso(total_runs, "/virtuoso_queries", args['rdf_datafile'])
                
        r_rdf3x(total_runs, args['rdf_queries'], name_of_graph)
        r_jena(total_runs, "/jena_queries", name_of_graph)

