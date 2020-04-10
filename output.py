import csv
import statistics


def storeResults(devices, response_times, methods, nodes, edges, runtime, optimizer, suffix):

  #  fieldnames = ['folds', 'threshold','nms','nonfood_filter','repeated_classes_filter','repeated_courseTypes_filter','threshold_ratio_low','threshold_ratio_high','iteration','Tray Accuracy', 'Menu Accuraccy']
  #  fieldnames = ['list_of_folds','tray_accuracy','menu_accuracy', 'TP','FP', 'FN','Dish precision','Dish recall','F1 score']
    parameter_fields = ['number of nodes', 'numbe of edges', 'runtime', 'optimizer']
    column_names = ['devices', 'response', 'methods']
    Title = ["Title: " + str(suffix)]
    param = ['PARAMETERS']
    results = ['RESULTS']
    avg_resp_for_method = ["avg_resp_vs_method"]
 
    info = list(zip(response_times,methods))
    unique_methods = list(set(methods))
    resp_time_for_method = []
    for m in unique_methods:
        r_t = getAverageResponse(info,m)
        resp_time_for_method.append(r_t)
    
    
    gap = ["", "", ""]

    file = 'C:/Users/Hassan/Documents/MIRI/Final_Thesis/NetworkX/Results_'+suffix+'.csv'

    parameters_value = [nodes, edges, runtime, optimizer]

    with open(file, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(Title)
        writer.writerow(gap)
        writer.writerow(param)
        writer.writerow(parameter_fields)
        writer.writerow(parameters_value)
        writer.writerow(gap)
        writer.writerow(results)
        writer.writerow(gap)
        writer.writerow(column_names)
        for row in zip(devices,response_times,methods):
           writer.writerow(row)
        writer.writerow(gap)
        writer.writerow(avg_resp_for_method)
        writer.writerow(gap)
        writer.writerow(unique_methods)
        writer.writerow(resp_time_for_method)

        f.close()

def getAverageResponse(info, method):
  method_entry = []
  avg = 0
  
  for i in info:
    if i[1] == method: 
      method_entry.append(i[0])

  if method_entry != []:
  
    #avg = sum(method_entry) / len(method_entry)
    avg = statistics.mean(method_entry)
  return avg


   