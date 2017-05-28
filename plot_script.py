from functools import reduce
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import argparse 
import os

rdf_box = {"4store": "#b3e5ff", "rdf3x" : "#9ec5ff", "jena" : "#00d9ff", "virtuoso" : "#00d6e6"}
rdf_line = {"4store": "#2300d1", "rdf3x" : "#190094", "jena" : "#000a52", "virtuoso" : "#050099"}
graph_box = {"sparksee" : "#72f443", "tinker" : "#59fa1e", "orient":"#aafd8c", "neo4j":"#60fb2d"}
graph_line = {"sparksee" : "#195f02", "tinker" : "#195f02", "orient":"#195f02", "neo4j":"#195f02"}

graph_based = ["orient", "neo4j", "tinker", "sparksee"]
rdf_based = ["virtuoso", "rdf3x", "jena", "4store"]
 

#fig = plt.figure()
#ax = fig.add_subplot(111)
global_figure_count = 0

def create_box_and_line_colors(all_dms):
    all_dms.sort()
    box_colors = []
    line_colors = []
    for each in all_dms:
        if each in graph_based:
            box_colors.append(graph_box[each])
            line_colors.append(graph_line[each])
        else:
            box_colors.append(rdf_box[each])
            line_colors.append(rdf_line[each])
    return (box_colors, line_colors)

#box_colors = ['#336B87', '#68829E', '#C4DFE6', '#6FB98F', '#B7B8B6']
#line_colors = ['#763626', '#598234', '#003B46', '#004485', '#34675C']


def geo_mean(array):
    """This function calculates the geometric mean of an array of numbers.
    array : The array of numbers whose geometric mean is to be calculated."""
    return (reduce(lambda x, y: x*y, array))**(1.0/len(array))

def har_mean(array):
    """This function calculates the harmonic mean of an array of numbers.
    array : The array of numbers whose harmonic mean is to be calculated."""
    return ((sum([1/x for x in array]))**(-1))*len(array)

def dms_plots(loadfile, queryfile, destination_folder, actions = ["query_hot", "query_cold"], graph_or_rdf = "Graph", line_w = 2):
    """This function plots and stores the data in form of latex tables for a given set of dms plots.
    loadfile : The csv file with the load times for all the DMS.
    queryfile : The csv file about the run times of different queries for all the DMS.
    graph_or_rdf : Graph for a graph based DMS, RDF for RDF based DMS."""

    load_data = None
    hot_query_data = None
    cold_query_data = None

    if graph_or_rdf.lower() == "both":
        graph_or_rdf = "Graph and RDF"
    
    if loadfile is not None:
        load_data = pd.read_csv(loadfile, index_col = False)

        dmss = []
        for each in load_data['dms']:
            if each not in dmss:
                dmss.append(each)

        box_colors, line_colors = create_box_and_line_colors(dmss)
        load_data_boxplot = load_data.boxplot(column=['time'], by = ['dms'], patch_artist = True, return_type = 'dict', fontsize = 14)
        if graph_or_rdf == "RDF":    
            plt.ylabel("Time (in seconds)")
        else:
            plt.ylabel("Time (in seconds)")
        
        plt.title("Time taken for loading a dataset by the different %s based DMS" % (graph_or_rdf))

        for i in range(len(load_data_boxplot['time']['fliers'])):
            load_data_boxplot['time']['fliers'][i].set_color(line_colors[i%len(line_colors)])
            load_data_boxplot['time']['fliers'][i].set_linewidth(line_w)


        for i in range(len(load_data_boxplot['time']['medians'])):
            load_data_boxplot['time']['medians'][i].set_color(line_colors[i%len(line_colors)])
            load_data_boxplot['time']['medians'][i].set_linewidth(line_w)

        for i in range(0,len(load_data_boxplot['time']['whiskers']),2):
            load_data_boxplot['time']['whiskers'][i].set_color(line_colors[(i//2)%len(line_colors)])
            load_data_boxplot['time']['whiskers'][i+1].set_color(line_colors[(i//2)%len(line_colors)])
            load_data_boxplot['time']['whiskers'][i].set_linewidth(line_w)
            load_data_boxplot['time']['whiskers'][i+1].set_linewidth(line_w)
        

        for i in range(0,len(load_data_boxplot['time']['caps']),2):
            load_data_boxplot['time']['caps'][i].set_color(line_colors[(i//2)%len(line_colors)])
            load_data_boxplot['time']['caps'][i+1].set_color(line_colors[(i//2)%len(line_colors)])
            load_data_boxplot['time']['caps'][i].set_linewidth(line_w)
            load_data_boxplot['time']['caps'][i+1].set_linewidth(line_w)

        for i in range(len(load_data_boxplot['time']['boxes'])):
            load_data_boxplot['time']['boxes'][i].set(color = line_colors[i%len(box_colors)])
            load_data_boxplot['time']['boxes'][i].set(facecolor = box_colors[i%len(box_colors)])
            load_data_boxplot['time']['boxes'][i].set_linewidth(line_w)



    if queryfile is not None:
        query_data = pd.read_csv(queryfile, index_col = False)    

        if "query_hot" in actions:
            hot_query_data = query_data[query_data['query_type']=='query_hot']
            zz = hot_query_data.groupby(['dms','query_id'], as_index = False).mean()
                
            dmss = []
            dic = {}
            for each in zz['dms']:
                dmss.append(each)
            box_colors, line_colors = create_box_and_line_colors(dmss)


            hot_query_data_plot = hot_query_data.boxplot(column = ['time'], by = ['dms', 'query_id'], patch_artist = True, return_type = 'dict', fontsize = 14)
            for i in range(len(hot_query_data_plot['time']['fliers'])):
                hot_query_data_plot['time']['fliers'][i].set_color(line_colors[i%len(line_colors)])
                hot_query_data_plot['time']['fliers'][i].set_linewidth(line_w)


            for i in range(len(hot_query_data_plot['time']['medians'])):
                hot_query_data_plot['time']['medians'][i].set_color(line_colors[i%len(line_colors)])
                hot_query_data_plot['time']['medians'][i].set_linewidth(line_w)

            for i in range(0,len(hot_query_data_plot['time']['whiskers']),2):
                hot_query_data_plot['time']['whiskers'][i].set_color(line_colors[(i//2)%len(line_colors)])
                hot_query_data_plot['time']['whiskers'][i+1].set_color(line_colors[(i//2)%len(line_colors)])
                hot_query_data_plot['time']['whiskers'][i].set_linewidth(line_w)
                hot_query_data_plot['time']['whiskers'][i+1].set_linewidth(line_w)
            

            for i in range(0,len(hot_query_data_plot['time']['caps']),2):
                hot_query_data_plot['time']['caps'][i].set_color(line_colors[(i//2)%len(line_colors)])
                hot_query_data_plot['time']['caps'][i+1].set_color(line_colors[(i//2)%len(line_colors)])
                hot_query_data_plot['time']['caps'][i].set_linewidth(line_w)
                hot_query_data_plot['time']['caps'][i+1].set_linewidth(line_w)

            for i in range(len(hot_query_data_plot['time']['boxes'])):
                hot_query_data_plot['time']['boxes'][i].set(color = line_colors[i%len(box_colors)])
                hot_query_data_plot['time']['boxes'][i].set(facecolor = box_colors[i%len(box_colors)])
                hot_query_data_plot['time']['boxes'][i].set_linewidth(line_w)





            plt.ylabel("Time (in seconds)")
            plt.title("Time taken for running queries on a dataset by the different %s based DMS (Warm Cache)"%(graph_or_rdf))


        if "query_cold" in actions:
            cold_query_data = query_data[query_data['query_type']=='query_cold']
            zz = cold_query_data.groupby(['dms','query_id'], as_index = False).mean()

            dmss = []
            for each in zz['dms']:
                dmss.append(each)
            box_colors, line_colors = create_box_and_line_colors(dmss)

            cold_query_data_plot = cold_query_data.boxplot(column = ['time'], by = ['dms', 'query_id'], patch_artist = True, fontsize = 14, return_type = 'dict')

            for i in range(len(cold_query_data_plot['time']['fliers'])):
                cold_query_data_plot['time']['fliers'][i].set_color(line_colors[i%len(line_colors)])
                cold_query_data_plot['time']['fliers'][i].set_linewidth(line_w)


            for i in range(len(cold_query_data_plot['time']['medians'])):
                cold_query_data_plot['time']['medians'][i].set_color(line_colors[i%len(line_colors)])
                cold_query_data_plot['time']['medians'][i].set_linewidth(line_w)

            for i in range(0,len(cold_query_data_plot['time']['whiskers']),2):
                cold_query_data_plot['time']['whiskers'][i].set_color(line_colors[(i//2)%len(line_colors)])
                cold_query_data_plot['time']['whiskers'][i+1].set_color(line_colors[(i//2)%len(line_colors)])
                cold_query_data_plot['time']['whiskers'][i].set_linewidth(line_w)
                cold_query_data_plot['time']['whiskers'][i+1].set_linewidth(line_w)
            

            for i in range(0,len(cold_query_data_plot['time']['caps']),2):
                cold_query_data_plot['time']['caps'][i].set_color(line_colors[(i//2)%len(line_colors)])
                cold_query_data_plot['time']['caps'][i+1].set_color(line_colors[(i//2)%len(line_colors)])
                cold_query_data_plot['time']['caps'][i].set_linewidth(line_w)
                cold_query_data_plot['time']['caps'][i+1].set_linewidth(line_w)

            for i in range(len(cold_query_data_plot['time']['boxes'])):
                cold_query_data_plot['time']['boxes'][i].set(color = line_colors[i%len(box_colors)])
                cold_query_data_plot['time']['boxes'][i].set(facecolor = box_colors[i%len(box_colors)])
                cold_query_data_plot['time']['boxes'][i].set_linewidth(line_w)



            plt.ylabel("Time (in seconds)")
            plt.title("Time taken for running queries on a dataset by the different %s based DMS (Cold Cache)"%(graph_or_rdf))

    

    if loadfile is not None:
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
        save_tables(destination_folder + "/tables/", [df_load_time], graph_or_rdf)

    if queryfile is not None:

        if "query_hot" in actions:
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
            save_tables(destination_folder + "/tables/", [df_hot_query_time], graph_or_rdf)

        if "query_cold" in actions:
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
            save_tables(destination_folder + "/tables/", [df_cold_query_time], graph_or_rdf)

def perf_specific_parameter(panda_dataframe, action, parameter_name, graph_or_rdf, only_table = False, line_w = 2):
    target_dataframe = panda_dataframe[panda_dataframe['action'] == action]
    groupby = None
    plt_title = None
    df_ = None
    
    if action == 'load':
        groupby = ['DMS']
        plt_title = "%s for loading a dataset by the different %s based DMS" % (parameter_name, graph_or_rdf)
    elif action == 'query_hot':
        groupby = ['DMS', 'query_number']
        plt_title = "%s for running queries on a dataset by the different %s based DMS (Hot Cache)"%(parameter_name, graph_or_rdf)
    else:
        groupby = ['DMS', 'query_number']
        plt_title = "%s for running queries on a dataset by the different %s based DMS (Cold Cache)"%(parameter_name, graph_or_rdf)

    #All data-analysis goes here
        
    if action == 'load':
        mean_ = target_dataframe.groupby(by = groupby, as_index = False).mean()
        var_ = target_dataframe.groupby(by = groupby, as_index = False).var()
        median_ = target_dataframe.groupby(by = groupby, as_index = False).median()
        geomean_ = target_dataframe.groupby(by = groupby, as_index = False).aggregate(geo_mean)
        harmean_ = target_dataframe.groupby(by = groupby, as_index = False).aggregate(har_mean)
        min_ = target_dataframe.groupby(by = groupby, as_index = False).min()
        max_ = target_dataframe.groupby(by = groupby, as_index = False).max()
        df_ = pd.DataFrame({'dms':mean_['DMS'], \
                'mean':mean_[parameter_name], 'variance':var_[parameter_name], \
                'median':median_[parameter_name], 'geom_mean':geomean_[parameter_name], \
                'har_mean':harmean_[parameter_name], 'min':min_[parameter_name], \
                'max':max_[parameter_name]})
        df_.name = graph_or_rdf + "_" + action + "_" + parameter_name
        

    else:
        mean_ = target_dataframe.groupby(by = groupby, as_index = False).mean()
        var_ = target_dataframe.groupby(by = groupby, as_index = False).var()
        median_ = target_dataframe.groupby(by = groupby, as_index = False).median()
        geomean_ = target_dataframe.groupby(by = groupby, as_index = False).aggregate(geo_mean)
        harmean_ = target_dataframe.groupby(by = groupby, as_index = False).aggregate(har_mean)
        min_ = target_dataframe.groupby(by = groupby, as_index = False).min()
        max_ = target_dataframe.groupby(by = groupby, as_index = False).max()
        df_ = pd.DataFrame({'dms':mean_['DMS'], 'query_number' : mean_['query_number'],\
                'mean':mean_[parameter_name], 'variance':var_[parameter_name], \
                'median':median_[parameter_name], 'geom_mean':geomean_[parameter_name], \
                'har_mean':harmean_[parameter_name], 'min':min_[parameter_name], \
                'max':max_[parameter_name]})
        df_.name = graph_or_rdf + "_" + action + "_" + parameter_name

    if not only_table:

        boxp = target_dataframe.boxplot(column = [parameter_name], by = groupby, patch_artist = True, return_type = 'dict', fontsize = 14)    
        plt.ylabel(parameter_name)
        plt.title(plt_title)

        
        zz = target_dataframe.groupby(groupby, as_index = False).mean()
        dmss = []
        for each in zz['DMS']:
            dmss.append(each)

        box_colors, line_colors = create_box_and_line_colors(dmss)

        for i in range(len(boxp[parameter_name]['fliers'])):
            boxp[parameter_name]['fliers'][i].set_color(line_colors[i%len(line_colors)])
            boxp[parameter_name]['fliers'][i].set_linewidth(line_w)


        for i in range(len(boxp[parameter_name]['medians'])):
            boxp[parameter_name]['medians'][i].set_color(line_colors[i%len(line_colors)])
            boxp[parameter_name]['medians'][i].set_linewidth(line_w)

        for i in range(0,len(boxp[parameter_name]['whiskers']),2):
            boxp[parameter_name]['whiskers'][i].set_color(line_colors[(i//2)%len(line_colors)])
            boxp[parameter_name]['whiskers'][i+1].set_color(line_colors[(i//2)%len(line_colors)])
            boxp[parameter_name]['whiskers'][i].set_linewidth(line_w)
            boxp[parameter_name]['whiskers'][i+1].set_linewidth(line_w)
        

        for i in range(0,len(boxp[parameter_name]['caps']),2):
            boxp[parameter_name]['caps'][i].set_color(line_colors[(i//2)%len(line_colors)])
            boxp[parameter_name]['caps'][i+1].set_color(line_colors[(i//2)%len(line_colors)])
            boxp[parameter_name]['caps'][i].set_linewidth(line_w)
            boxp[parameter_name]['caps'][i+1].set_linewidth(line_w)

        for i in range(len(boxp[parameter_name]['boxes'])):
            boxp[parameter_name]['boxes'][i].set(color = line_colors[i%len(box_colors)])
            boxp[parameter_name]['boxes'][i].set(facecolor = box_colors[i%len(box_colors)])
            boxp[parameter_name]['boxes'][i].set_linewidth(line_w)

        save_plot(args['destination_folder'] + "/plots")    
    return df_

def dms_plots_perf_data(perffile, action, parameters, destination_folder, graph_or_rdf = "Graph"):
    """This function plots and stores the perf data in form of latex tables for a given set of dms plots.
    loadfile : The csv file with the load times for all the DMS.
    queryfile : The csv file about the run times of different queries for all the DMS.
    graph_or_rdf : Graph for a graph based DMS, RDF for RDF based DMS."""

    all_data = pd.read_csv(perffile, index_col = False)
    list_of_tables = []
    all_parameters = "cycles,instructions,cache-references,cache-misses,bus-cycles,L1-dcache-loads,L1-dcache-load-misses,L1-dcache-stores,dTLB-loads,dTLB-load-misses,LLC-loads,LLC-load-misses,LLC-stores,branches,branch-misses,context-switches,cpu-migrations,page-faults".split(",")

    for each in parameters:
        for each_action in actions:
            list_of_tables.append(perf_specific_parameter(all_data, each_action, each, graph_or_rdf, only_table = False))
    
    only_tables = list(set(all_parameters) - set(parameters))
    for each in only_tables:
        for each_action in actions:
            list_of_tables.append(perf_specific_parameter(all_data, each_action, each, graph_or_rdf, only_table = True))


    if not os.path.exists(destination_folder + "/tables/"):
        os.mkdir(destination_folder + "/tables/")
    save_tables(destination_folder + "/tables/", list_of_tables, graph_or_rdf)


def save_tables(directory, l, dms):
    """The function saves all the tables in tex format.
    directory : The directory where all the tables are stored.
    l : The list of all the tables.
    dms : The name of the DMS whose tables are stored."""
    if directory[-1]!="/":
        directory = directory + "/"
    for i in l:
        file_handler = open(directory + dms + "_" + i.name + ".tex", "w")
        file_handler.write(i.to_latex())
        file_handler.close()

def save_plot(directory):
    """The function saves all the plots in png format.
    directory : The directory where all the png formats are stored."""
    global global_figure_count    
    if directory[-1]!="/":
        directory = directory + "/"
    for i in plt.get_fignums():
        plt.figure(i)
        plt.savefig(directory + 'figure%d.png' % global_figure_count, bbox_inches='tight', dpi = 600)
        global_figure_count+=1
    plt.close('all')

def pre_run():
    if not os.path.exists("/plots/"):
        os.mkdir("/plots/")
    
    if not os.path.exists("/tables/"):
        os.mkdir("/tables/")

def sanity_check(loadfile, queryfile):
    """The function runs a certain sanity checks before running the code.
    loadfile : The path of the loadfile.
    queryfile : The path of the queryfile.
    """
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
    parser.add_argument('-pg', '--perf_graph', help = 'The location of the perf csv file for the Graph based DMS', required = False)
    parser.add_argument('-pr', '--perf_rdf', help = 'The location of the perf csv file for the RDF based DMS', required = False)
    parser.add_argument('-cr', '--combined_csv', help = 'The location of the perf csv file for both RDF based and Graph based DMS', required = False)

    parser.add_argument('-pf', '--plot_for', help = 'The actions for which we need to plot. eg. "load,query_hot,query_cold"', required = False)

    parser.add_argument('-lg', '--load_graph_csv', help='The location of the load csv file for Graph', required = False)
    parser.add_argument('-pp', '--plot_parameters', help='The parameters to be plotted for perf.', required = False)
    parser.add_argument('-qg', '--query_graph_csv', help='The location of the queries csv file for Graph', required = False)
    parser.add_argument('-lr', '--load_rdf_csv', help='The location of the load csv file for RDF', required = False)
    parser.add_argument('-qr', '--query_rdf_csv', help='The location of the queries csv file for RDF', required = False)
    parser.add_argument('-lc', '--load_combined_csv', help='The location of the load csv file for Both', required = False)
    parser.add_argument('-qc', '--query_combined_csv', help='The location of the queries csv file for Both', required = False)


    parser.add_argument('-df', '--destination_folder', help = 'The destination folder where the plots have to be generated', required = True)

#    parser.add_argument('-lr', '--load_rdf_csv', help='The location of the load csv file for RDF', required = True)
#    parser.add_argument('-qr', '--query_rdf_csv', help='The location of the queries csv file for RDF', required = True)

    args = vars(parser.parse_args())
#    if not sanity_check(args['load_graph_csv'], args['query_graph_csv']):
#        exit(-1)
    
#    if not sanity_check(args['load_rdf_csv'], args['query_rdf_csv']):
#        exit(-1)

    #dms_plots(args['load_graph_csv'], args['query_graph_csv'], args['destination_folder'], "Graph")
#    dms_plots(args['load_rdf_csv'], args['query_rdf_csv'], "RDF")
    font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 18}

    plt.rc('font', **font)

    #dms_plots_perf_data("temp_rdf.csv", "load", ['L1-dcache-loads', 'L1-dcache-load-misses'] , graph_or_rdf = "RDF")
    if not os.path.exists(args['destination_folder']):
        os.mkdir(args['destination_folder'])
    if not os.path.exists(args['destination_folder'] + "/plots/"):
        os.mkdir(args['destination_folder'] + "/plots/")
    if not os.path.exists(args['destination_folder'] + "/tables/"):
        os.mkdir(args['destination_folder'] + "/tables/")


    plot_parameters = ['L1-dcache-loads', 'L1-dcache-load-misses']

    if args['plot_parameters']:
        plot_parameters = args['plot_parameters'].strip('"').split(",")


    actions = args["plot_for"].split(",")
    if args["load_graph_csv"]:
        dms_plots(args["load_graph_csv"], None, args['destination_folder'], graph_or_rdf = "Graph", line_w = 2, actions = actions)
    if args["query_graph_csv"]:
        dms_plots(None, args["query_graph_csv"], args['destination_folder'], graph_or_rdf = "Graph", line_w = 2, actions = actions)

    if args["load_rdf_csv"]:
        dms_plots(args["load_rdf_csv"], None, args['destination_folder'], graph_or_rdf = "RDF", line_w = 2, actions = actions)
    if args["query_rdf_csv"]:
        dms_plots(None, args["query_rdf_csv"], args['destination_folder'], graph_or_rdf = "RDF", line_w = 2, actions = actions)

    if args["load_combined_csv"]:
        dms_plots(args["load_combined_csv"], None, args['destination_folder'], graph_or_rdf = "both", line_w = 2, actions = actions)
    if args["query_combined_csv"]:
        dms_plots(None, args["query_combined_csv"], args['destination_folder'], graph_or_rdf = "both", line_w = 2, actions = actions)



    
    if args["perf_graph"]:
        dms_plots_perf_data(args["perf_graph"], actions, plot_parameters, args['destination_folder'], graph_or_rdf = "Graph")
    if args["perf_rdf"]:
        dms_plots_perf_data(args["perf_rdf"], actions, plot_parameters, args['destination_folder'], graph_or_rdf = "RDF")
    if args["combined_csv"]:
        dms_plots_perf_data(args["combined_csv"], actions, plot_parameters, args['destination_folder'], graph_or_rdf = "RDF and Graph")
            

#    save_plot(args['destination_folder'] + "/plots")
    
    #plt.show()
