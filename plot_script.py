from functools import reduce
import pandas as pd
import matplotlib.pyplot as plt
import argparse 
import os

def geo_mean(array):
    return (reduce(lambda x, y: x*y, array))**(1.0/len(array))

def har_mean(array):
    return ((sum([1/x for x in array]))**(-1))*len(array)

def dms_plots(loadfile, queryfile, graph_or_rdf = "Graph"):
    load_data = pd.read_csv(loadfile, index_col = False)
    #print(load_data)
    #print(load_data.groupby(by = ['dms']).mean())
    #print(load_data.groupby(by = ['dms']).std())
    #print(load_data.groupby(by = ['dms']).median())
    
    
    #All plots go here    
    load_data.boxplot(column=['time'], by = ['dms'])
    plt.ylabel("Time (in milliseconds)")
    plt.title("Time taken for loading a dataset by the different %s based DMS" % (graph_or_rdf))

    query_data = pd.read_csv(queryfile, index_col = False)    

    hot_query_data = query_data[query_data['query_type']=='query_hot']
    hot_query_data.boxplot(column = ['time'], by = ['dms', 'query_id'])
    plt.ylabel("Time (in milliseconds)")
    plt.title("Time taken for running queries on a dataset by the different %s based DMS (Hot Cache)"%(graph_or_rdf))

    cold_query_data = query_data[query_data['query_type']=='query_cold']
    cold_query_data.boxplot(column = ['time'], by = ['dms', 'query_id'])
    plt.ylabel("Time (in milliseconds)")
    plt.title("Time taken for running queries on a dataset by the different %s based DMS (Cold Cache)"%(graph_or_rdf))

    

    #All data-analysis goes here
    mean_load_time = load_data.groupby(by = ['dms'], as_index = False).mean()
    var_load_time = load_data.groupby(by = ['dms'], as_index = False).var()
    median_load_time = load_data.groupby(by = ['dms'], as_index = False).median()
    geomean_load_time = load_data.groupby(by = ['dms'], as_index = False).aggregate(geo_mean)
    harmean_load_time = load_data.groupby(by = ['dms'], as_index = False).aggregate(har_mean)
    min_load_time = load_data.groupby(by = ['dms'], as_index = False).min()
    max_load_time = load_data.groupby(by = ['dms'], as_index = False).max()
    df_load_time = pd.DataFrame({'dms':mean_load_time['dms'], \
            'mean':mean_load_time['time'], 'variance':var_load_time['time'], \
            'median':median_load_time['time'], 'geom_mean':geomean_load_time['time'], \
            'har_mean':harmean_load_time['time'], 'min':min_load_time['time'], \
            'max':max_load_time['time']})
    df_load_time.name = 'load_time'

    mean_hot_query_data = hot_query_data.groupby(by = ['dms'], as_index = False).mean()
    var_hot_query_data = hot_query_data.groupby(by = ['dms'], as_index = False).var()
    median_hot_query_data = hot_query_data.groupby(by = ['dms'], as_index = False).median()
    geomean_hot_query_data = hot_query_data.groupby(by = ['dms'], as_index = False).aggregate(geo_mean)
    harmean_hot_query_data = hot_query_data.groupby(by = ['dms'], as_index = False).aggregate(har_mean)
    min_hot_query_data = hot_query_data.groupby(by = ['dms'], as_index = False).min()
    max_hot_query_data = hot_query_data.groupby(by = ['dms'], as_index = False).max()
    df_hot_query_time = pd.DataFrame({'dms':mean_hot_query_data['dms'], \
            'mean':mean_hot_query_data['time'], 'variance':var_hot_query_data['time'], \
            'median':median_hot_query_data['time'], 'geom_mean':geomean_hot_query_data['time'], \
            'har_mean':harmean_hot_query_data['time'], 'min':min_hot_query_data['time'], \
            'max':max_hot_query_data['time']})
    df_hot_query_time.name = 'hot_query_time'

    mean_cold_query_data = cold_query_data.groupby(by = ['dms'], as_index = False).mean()
    var_cold_query_data = cold_query_data.groupby(by = ['dms'], as_index = False).var()
    median_cold_query_data = cold_query_data.groupby(by = ['dms'], as_index = False).median()
    geomean_cold_query_data = cold_query_data.groupby(by = ['dms'], as_index = False).aggregate(geo_mean)
    harmean_cold_query_data = cold_query_data.groupby(by = ['dms'], as_index = False).aggregate(har_mean)
    min_cold_query_data = cold_query_data.groupby(by = ['dms'], as_index = False).min()
    max_cold_query_data = cold_query_data.groupby(by = ['dms'], as_index = False).max()
    df_cold_query_time = pd.DataFrame({'dms':mean_cold_query_data['dms'], \
            'mean':mean_cold_query_data['time'], 'variance':var_cold_query_data['time'], \
            'median':median_cold_query_data['time'], 'geom_mean':geomean_cold_query_data['time'], \
            'har_mean':harmean_cold_query_data['time'], 'min':min_cold_query_data['time'], \
            'max':max_cold_query_data['time']})
    df_cold_query_time.name = 'cold_query_time'

    save_tables(os.getcwd() + "/tables/", [df_load_time, df_hot_query_time, df_cold_query_time], graph_or_rdf)

def save_tables(directory, l, dms):
    if directory[-1]!="/":
        directory = directory + "/"
    for i in l:
        file_handler = open(directory + dms + "_" + i.name + ".tex", "w")
        file_handler.write(i.to_latex())
        file_handler.close()

def save_plot(directory):
    if directory[-1]!="/":
        directory = directory + "/"
    for i in plt.get_fignums():
        print(i)
        plt.figure(i)
        plt.savefig(directory + 'figure%d.png' % i)


def sanity_check(loadfile, queryfile):
    if not os.path.exists(loadfile):
        print("Error: The path for the load csv file does not exist")
        return False

    if not os.path.exists(queryfile):    
        print("Error: The path for the query csv file does not exist")
        return False

    if not os.path.exists("/plots/"):
        os.mkdir("/plots/")
    
    if not os.path.exists("/tables/"):
        os.mkdir("/tables/")

    """
    if not os.path.exists("/plots"):
        os.mkdir("/plots")
    """    
    return True

if __name__ == "__main__" :
    parser = argparse.ArgumentParser(description='The Litmus Plotter')
    parser.add_argument('-lg', '--load_graph_csv', help='The location of the load csv file for Graph', required = True)
    parser.add_argument('-qg', '--query_graph_csv', help='The location of the queries csv file for Graph', required = True)
    parser.add_argument('-lr', '--load_rdf_csv', help='The location of the load csv file for RDF', required = True)
    parser.add_argument('-qr', '--query_rdf_csv', help='The location of the queries csv file for RDF', required = True)

    args = vars(parser.parse_args())
    if not sanity_check(args['load_graph_csv'], args['query_graph_csv']):
        exit(-1)
    
    if not sanity_check(args['load_rdf_csv'], args['query_rdf_csv']):
        exit(-1)

    dms_plots(args['load_graph_csv'], args['query_graph_csv'], "Graph")
    dms_plots(args['load_rdf_csv'], args['query_rdf_csv'], "RDF")


    save_plot("/plots/")
        
    plt.show()
