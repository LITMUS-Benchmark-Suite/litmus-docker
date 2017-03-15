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
    /tmp/HelloWorld.gdb %s \
    /var/log/sparksee/load_logs.log" % (runs, xmlFile))

    #Querying the database
    os.system("/scripts/sparksee/SparkseeQuery.sh %s \
    /tmp/HelloWorld.gdb %s \
    /var/log/sparksee/query_logs.log" % (runs, xmlFile))

    pass

def r_rdf3x():
    pass

def g_orient():
    pass

def g_neo4j():
    pass

def r_monet():
    pass

def r_jena():
    pass

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
