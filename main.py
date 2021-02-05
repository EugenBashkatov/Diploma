# This is a sample Python script.

# Token:
# cd5c0f2b8bb97f0cd4e46dd6f0e5647922a163d3

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import logistic
from scipy.stats import norm

import xlsxwriter


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# ['Num','Date','MinTemp','RayFrom','RayTo','dx','dy','K','B','FLiine']
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

def logistic_distribution(par_size,par_scale):
    logis = logistic.rvs(size=par_size, scale = par_scale)
    x_logistic = []
    logistic_data = []
    for i in range(0,len(logis)):
        x_logistic.append(i)
        logistic_data.append([i,logis[i]])
    print(logistic_data)

    plt.plot(x_logistic,logis)
    plt.show()
    return logistic_data

def normal_distribution(par_size,par_scale):
    normal = norm.rvs(size=par_size, scale = par_scale)
    x_normal = []
    normal_data = []
    for i in range(0,len(normal)):
        x_normal.append(i)
        normal_data.append([i,normal[i]])
    # print(normal_data)

    plt.plot(x_normal,normal)
    plt.show()
    return normal_data


input_file_name='daily-min-temperatures-02.csv'
df = pd.read_csv(input_file_name,
                 names=['Date', 'MinTemp', 'RayFrom', 'RayTo', 'dx', 'dy', 'K', 'B', 'FLiine'])

# data_list = df.to_numpy()
# data_list = input_file_name
#TODO Выбор распределения
data_list = normal_distribution(20,10)



def line(x0, x1, x):
    y0 = data_list[x0][1]
    y1 = data_list[x1][1]

    k = (y1 - y0) / (x1 - x0)
    B = (x1 * y0 - x0 * y1) / (x1 - x0)
    eps = 1.e-3
    return [k, B, k * x + B, (k * x + B - data_list[x][1]) <= 0]


def is_visible(x0, x1, x):
    y0 = data_list[x0][1]
    y1 = data_list[x1][1]

    k = (y1 - y0) / (x1 - x0)
    B = (x1 * y0 - x0 * y1) / (x1 - x0)
    eps = 1.e-3
    return (k * x + B - data_list[x][1]) <= 0


# max_dim = sum(1 for my_line in open(input_file_name,'r'))
max_dim = len(data_list)




def print_graph_array(graph_array):
    for ind in range(0,len(graph_array)):print(ind,":",graph_array[ind])

def build_graph_with_clusters(start_point, max_dim, DEBUG = False):
    x0 = start_point
    x1 = x0 + 1
    cluster_size = 1
    graph_array = np.eye(max_dim)
    graph_array.fill(0)

    array_k = []
    while True:
        vis_k = line(x0, x1, x1)[0]
        vis_k_next = line(x0, x1 + 1, x1 + 1)[0]

        x1 = x0+1
        x2 = x1+1

        while x1 <= max_dim - 2:
            vis_k = line(x0, x1, x1)[0]
             # x2 = x1+1
            vis_k_next = line(x0, x2, x1)[0]
            graph_array[x0][x0] = cluster_size
            if DEBUG:print("DEBUG_1:GFrom= ", x0, "To= ", x1, "k= ", vis_k, "Next= ", x2, "next_k=", vis_k_next,cluster_size)
            array_k.append([x0, x1, vis_k, vis_k_next, cluster_size])
            is_growing = vis_k < vis_k_next
            is_decrease = not is_growing
            if is_growing:
                # Вершина вхоит в кластер? -да
                # vis_k=vis_k_next
                # x0=x1+1
                graph_array[x0][x1] = 1
                graph_array[x1][x0] = 1
                x1 = x1 + 1
                x2 = x1+1
                cluster_size = cluster_size + 1
                # graph_array[x1][x0] = 1
            else:
                # Вершина вхоит в кластер? -нет
                cluster_size = 1
                # начало нового кластера
                x0 = x1
                x2 = x1+1
                graph_array[x0][x1] = 1
                graph_array[x1][x0] = 1
                x1 = x0 + 1
                x2 = x1+1

                if DEBUG:print(x0, x1, x2, vis_k, vis_k_next, cluster_size, is_growing, is_decrease)
        if x0 == max_dim - 3:
            # x1=x0+1
            # x2=x1
            # continue
            # TODO Придумать, как обработать хвост
            graph_array[x0][x0] = cluster_size+1
            graph_array[x0][x1] = 1
            graph_array[x1][x0] = 1
            if DEBUG:
                print("****  Array_k  ****")
                for ind in range(0,max_dim-2) : print( array_k[ind])
                print("******************")
            break
        if x1 == max_dim - 1:
            break


    return graph_array





graph_array = build_graph_with_clusters(0,max_dim, True)
print(graph_array)


# print(graph_array[362])
# print(graph_array[325])

plt.matshow(graph_array)

plt.show()


eOutput = pd.DataFrame(graph_array)
writer = pd.ExcelWriter('ArrayFromPycharm.xlsx', engine='xlsxwriter')

# Convert the dataframe to an XlsxWriter Excel object.
eOutput.to_excel(writer, sheet_name='Sheet1', index=False)

# Close the Pandas Excel writer and output the Excel file.
writer.save()