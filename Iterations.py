import pandas as pd
import os
import csv

def getFileAverage():

    file_path = 'C:/Users/Hassan/Documents/MIRI/Final_Thesis/NetworkX/'
    list_of_files = os.listdir(file_path)

    for file in list_of_files:

        if file.endswith("." + "csv"):
            filename = file_path + file
            with open(filename, 'rU') as f:
                reader = csv.reader(f)
                data = pd.read_csv(filename, skiprows = 44)
                print (data['Cloud direct'])


if __name__ == '__main__':
    getFileAverage()