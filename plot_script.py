from functools import reduce
import pandas as pd
import matplotlib.pyplot as plt
import argparse 
import os

def geo_mean(array):
    return (reduce(lambda x, y: x*y, array))**(1.0/len(array))

def har_mean(array):
    return ((sum([1/x for x in array]))**(-1))*len(array)

def foobar(loadfile, queryfile):
    load_data = pd.read_csv(loadfile, index_col = False)
    #print(load_data)
    #print(load_data.groupby(by = ['dms']).mean())
    #print(load_data.groupby(by = ['dms']).std())
    #print(load_data.groupby(by = ['dms']).median())
    
    #All plots go here    
    load_data.boxplot(column=['time'], by = ['dms'])
    plt.ylabel("Time (in milliseconds)")
    plt.title("Time taken for loading a dataset by the different Graph based DMS")

    query_data = pd.read_csv(queryfile, index_col = False)    

    hot_query_data = query_data[query_data['query_type']=='query_hot']
    hot_query_data.boxplot(column = ['time'], by = ['dms', 'query_id'])
    plt.ylabel("Time (in milliseconds)")
    plt.title("Time taken for running queries on a dataset by the different Graph based DMS (Hot Cache)")

    cold_query_data = query_data[query_data['query_type']=='query_cold']
    cold_query_data.boxplot(column = ['time'], by = ['dms', 'query_id'])
    plt.ylabel("Time (in milliseconds)")
    plt.title("Time taken for running queries on a dataset by the different Graph based DMS (Cold Cache)")

    #All data-analysis goes here
    mean_load_time = load_data.groupby(by = ['dms'], as_index = False).mean()
    var_load_time = load_data.groupby(by = ['dms'], as_index = False).var()
    median_load_time = load_data.groupby(by = ['dms'], as_index = False).median()
    geomean_load_time = load_data.groupby(by = ['dms'], as_index = False).aggregate(geo_mean)
    harmean_load_time = load_data.groupby(by = ['dms'], as_index = False).aggregate(har_mean)
    min_load_time = load_data.groupby(by = ['dms'], as_index = False).min()
    max_load_time = load_data.groupby(by = ['dms'], as_index = False).max()
    
    mean_hot_query_data = hot_query_data.groupby(by = ['dms'], as_index = False).mean()
    var_hot_query_data = hot_query_data.groupby(by = ['dms'], as_index = False).var()
    median_hot_query_data = hot_query_data.groupby(by = ['dms'], as_index = False).median()
    geomean_hot_query_data = hot_query_data.groupby(by = ['dms'], as_index = False).aggregate(geo_mean)
    harmean_hot_query_data = hot_query_data.groupby(by = ['dms'], as_index = False).aggregate(har_mean)
    min_hot_query_data = hot_query_data.groupby(by = ['dms'], as_index = False).min()
    max_hot_query_data = hot_query_data.groupby(by = ['dms'], as_index = False).max()


    mean_cold_query_data = cold_query_data.groupby(by = ['dms'], as_index = False).mean()
    var_cold_query_data = cold_query_data.groupby(by = ['dms'], as_index = False).var()
    median_cold_query_data = cold_query_data.groupby(by = ['dms'], as_index = False).median()
    geomean_cold_query_data = cold_query_data.groupby(by = ['dms'], as_index = False).aggregate(geo_mean)
    harmean_cold_query_data = cold_query_data.groupby(by = ['dms'], as_index = False).aggregate(har_mean)
    min_cold_query_data = cold_query_data.groupby(by = ['dms'], as_index = False).min()
    max_cold_query_data = cold_query_data.groupby(by = ['dms'], as_index = False).max()
    
        
    plt.show()

def sanity_check(loadfile, queryfile):
    if not os.path.exists(loadfile):
        print("Error: The path for the load csv file does not exist")
        return False

    if not os.path.exists(queryfile):    
        print("Error: The path for the query csv file does not exist")
        return False
    """
    if not os.path.exists("/plots"):
        os.mkdir("/plots")
    """    
    return True

if __name__ == "__main__" :
    parser = argparse.ArgumentParser(description='The Litmus Plotter')
    parser.add_argument('-l', '--load_csv', help='The location of the load csv file', required = True)
    parser.add_argument('-q', '--query_csv', help='The location of the queries csv file', required = True)

    args = vars(parser.parse_args())
    if not sanity_check(args['load_csv'], args['query_csv']):
        exit(-1)
    
    foobar(args['load_csv'], args['query_csv'])
