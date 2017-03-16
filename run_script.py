import argparse
import os

graph_based = ['g_sparksee', 'g_orient', 'g_neo4j' ]

rdf_based = ['r_rdf3x', 'r_monet', 'r_jena', 'r_arq' ]

directory_maps = { \
    'g_sparksee':'sparksee', \
    'g_orient' : 'orient', \
    'g_neo4j' : 'neo4j', \
    'r_rdf3x' : 'rdf3x', \
    'r_monet' : 'monet', \
    'r_jena' : 'jena', \
    'r_arq' : 'arq'
    }

def g_sparksee(runs, xmlFile):
    #Loading the database
    os.system("/scripts/sparksee/SparkseeLoad.sh %s \
    /tmp/sparksee.gdb %s \
    /var/log/sparksee/load_logs.log" % (runs, xmlFile))

    #Querying the database
    os.system("/scripts/sparksee/SparkseeQuery.sh %s \
    /tmp/HelloWorld.gdb %s \
    /var/log/sparksee/query_logs.log" % (runs, xmlFile))


def r_rdf3x(runs, queryLocations, dataFile):
    #Loading the database
    os.system("/scripts/rdf3x/RDF3xLoad.sh %s /tmp/ rdf3x_graph \
    %s /var/rdf3x/load_logs.log" % (runs, dataFile)) 
    
    #Querying the database
    os.system("/scripts/rdf3x/RDF3xExecute.sh /tmp/ rdf3x_graph \
    %s %s /var/rdf3x/load_logs.log %s" % (dataFile, queryLocations, runs)) 
        

def g_orient(runs, xmlFile):
    #Loading the database
    os.system("/scripts/orient/OrientLoad.sh %s \
    /tmp/orient_load.gdb %s /scripts/orient/OrientLoad.groovy \
    /var/log/orient/load_logs.log" % (runs, xmlFile))

    #Querying the database
    os.system("/scripts/orient/OrientQuery.sh %s \
    /tmp/orient_query.gdb %s /scripts/orient/OrientLoad.groovy \
    /var/log/orient/query_logs.log" % (runs, xmlFile))


def g_neo4j(runs, xmlFile):
    #Loading the database
    os.system("/scripts/neo4j/Ne04jLoad.sh %s \
    /tmp/neo4j_load.gdb %s \
    /var/log/neo4j/load_logs.log" % (runs, xmlFile))

    #Querying the database
    os.system("/scripts/sparksee/Neo4jQuery.sh %s \
    /tmp/neo4j_Query.gdb %s \
    /var/log/neo4j/query_logs.log" % (runs, xmlFile))
    

def r_monet():
    pass

def r_jena(runs, queryLocation, dataFile):
    #Load the database
    os.system("/scripts/jena/JenaTDBLoad.sh /tmp/ jena_graph \
    %s /var/jena/load_log.log %s" % (dataFile, runs))
    
    #Run the query
    os.system("/scripts/jena/JenaTDBExecute.sh /tmp/ jena_graph \
    %s %s /var/jena/query_logs.log %s" % (dataFile, queryLocation, runs))

def r_arq():
    pass

def create_log_files(list_to_benchmark):
    for each in list_to_benchmark:
        os.system('touch %s' % ('/var/log/' + directory_maps[each] + '/load_logs.log'))
        os.system('touch %s' % ('/var/log/' + directory_maps[each] + '/query_logs.log'))
        os.system('touch %s' % ('/var/log/' + directory_maps[each] + '/index_logs.log'))

def foo(list_to_benchmark, runs = 10):
    #create_log_files(list_to_benchmark)    
    print(list_to_benchmark)
    pass
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='The Litmus Benchmark Suite')
    parser.add_argument('-v', '--verbose', action = "store_true", help = "Verbose", required = False)
    parser.add_argument('-a','--all', action = "store_true" , help='Run for all DMS', required=False)
    parser.add_argument('-g','--graph', action = "store_true", help='Run for all Graph Based DMS', required=False)
    parser.add_argument('-r','--rdf', action = "store_true", help='Run for all RDF Based DMS', required=False)
    parser.add_argument('-n', '--runs', help='Number of times, the experiment should be conducted', required = False)
    args = vars(parser.parse_args())
    final_list = None
    verbose = args['verbose']
    if args['all'] or (args['graph'] and args['rdf']):
        final_list = graph_based + rdf_based
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
    g_sparksee(10, '/graph_data/graph-example-1.xml')
