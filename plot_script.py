import pandas as pd
import matplotlib.pyplot as plt
import argparse 
import os

def foobar(loadfile, queryfile):
    load_data = pd.read_csv(loadfile, index_col = False)
    #print(load_data)
    #print(load_data.groupby(by = ['dms']).mean())
    #print(load_data.groupby(by = ['dms']).std())
    #print(load_data.groupby(by = ['dms']).median())
    load_data.boxplot(column=['time'], by = ['dms'])
    plt.ylabel("Time (in milliseconds)")
    plt.title("Time taken for loading a dataset by the different Graph based DMS")
        

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
