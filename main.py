# This is a sample Python script.

# Token:
# cd5c0f2b8bb97f0cd4e46dd6f0e5647922a163d3

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import xlsxwriter


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# ['Num','Date','MinTemp','RayFrom','RayTo','dx','dy','K','B','FLiine']
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')


input_file_name='daily-min-temperatures-02.csv'
df = pd.read_csv(input_file_name,
                 names=['Date', 'MinTemp', 'RayFrom', 'RayTo', 'dx', 'dy', 'K', 'B', 'FLiine'])

data_list = df.to_numpy()


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


max_dim = sum(1 for my_line in open(input_file_name,'r'))

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
                if DEBUG:print("DEBUG_2:",x0, x1, x2, vis_k, vis_k_next, cluster_size, is_growing, is_decrease)
        if x0 == max_dim - 3:
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

plt.matshow(graph_array)

plt.show()


eOutput = pd.DataFrame(graph_array)
writer = pd.ExcelWriter('ArrayFromPycharm.xlsx', engine='xlsxwriter')

# Convert the dataframe to an XlsxWriter Excel object.
eOutput.to_excel(writer, sheet_name='Sheet1', index=False)

# Close the Pandas Excel writer and output the Excel file.
writer.save()

#---------------------------------  Version 1.0 ------------------------------
