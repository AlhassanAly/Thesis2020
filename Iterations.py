import pandas as pd
import os
import csv
import collections
import statistics
from Parameters import Edge_devices

d_num = (Edge_devices * 2 )+ 24


def getFileAverage():

    file_path = 'C:/Users/Hassan/Documents/MIRI/Final_Thesis/NetworkX/outputs/'
    list_of_files = os.listdir(file_path)
    methods_list = ['single fog', 'Cloud through fog', 'Cloud direct', 'Inrange cluster', 'Neighbor cluuster']
    average = {'single fog':[],'Cloud through fog':[], 'Cloud direct':[], 'Inrange cluster':[],'Neighbor cluuster':[]}
    for file in list_of_files:

        if file.endswith("." + "csv"):
            filename = file_path + file
            with open(filename, 'rU') as f:
                reader = csv.reader(f)
                data = pd.read_csv(filename, skiprows = d_num)
                for col in data.columns: 
                    for m in methods_list:
                        if m == col:
                            average[m].append(data.at[0,col])
    
    return average
                
def getAverage(avg_dict):
    final_avg = {}
    res_time_deviation = {}
    for method,resp_times in avg_dict.items():
        if resp_times != []:
           final_avg[method]= statistics.mean(resp_times)
           res_time_deviation[method] = statistics.stdev(resp_times)
    return final_avg, res_time_deviation

if __name__ == '__main__':
    average = getFileAverage()
    final_avg = getAverage(average)
    print (final_avg)
    