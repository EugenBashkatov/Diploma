# This is a sample Python script.

# Token:
# cd5c0f2b8bb97f0cd4e46dd6f0e5647922a163d3

import sys
import os
import math
import logging
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import stem_plot as st
import datetime as dt
import seaborn as sns
# numm=-math.inf
# if numm<10000000:print (math.atan(numm))
# exit()
import xlsxwriter

DEBUG1 = True
DEBUG2 = False
DEBUG3 = False
DEBUG4 = False
DEBUG5 = False

def get_logger(name=__file__, file='log.txt', encoding='utf-8'):
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '[%(asctime)s] %(filename)s:%(lineno)d %(levelname)-8s %(message)s')
    os.remove("log.txt")
    fh = logging.FileHandler(file, encoding=encoding, mode='w')
    #    fh = logging.FileHandler(file, encoding=encoding)
    fh.setFormatter(formatter)
    log.addHandler(fh)

    sh = logging.StreamHandler(stream=sys.stdout)
    sh.setFormatter(formatter)
    log.addHandler(sh)

    return log


log = get_logger()

log.info("start")

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

if __name__ == '__main__':
    # print_hi('PyCharm')
    # TODO # почиctить фильтрацию
    input_file_name = 'daily-min-temperatures.csv'
    full_df = pd.read_csv(
        input_file_name,
        names=[
            'Date',
            'MinTemp'],
        index_col=[0])
    start_date = "1981-01-01"
    end_date = "1981-01-12"
    df = full_df.loc[start_date:end_date].copy(deep=True)

    print(df, df.dtypes, df.index)
    data_list = df['MinTemp'].tolist()

# TODO сделать одномерный массив data_list заполнить для замены дат
max_dim = len(df)
out_data_list_name = "data_list from {0} to {1} length {2}.csv".format(
    start_date, end_date, max_dim)
new_ind = np.arange(0, max_dim)

st.stemplot(new_ind, data_list)
pd.DataFrame(data_list).to_csv(out_data_list_name)
full_df.to_csv("full_df.csv")

for ind in range(0,len(df)): print("DEBUG_3:", ind, df)

def line(x0, x1, data_list):
    y0 = data_list[x0]
    y1 = data_list[x1]

    k = (y1 - y0) / (x1 - x0)
    B = (x1 * y0 - x0 * y1) / (x1 - x0)
    # eps = 1.e-3
    # return [k, B, k * x + B, (k * x + B - data_list[x]) <= 0]
    return k

def is_visible(x0, x1, x):
    y0 = data_list[x0]
    y1 = data_list[x1]

    k = (y1 - y0) / (x1 - x0)
    B = (x1 * y0 - x0 * y1) / (x1 - x0)
    # eps = 1.e-3
    return (k * x + B - data_list[x] <= 0)


# max_dim = sum(1 for my_line in open(input_file_name,'r'))

def print_graph_array(graph_array):
    for ind in range(0, len(graph_array)):
        print(ind, ":", graph_array[ind])


def is_cluster_found(x0, x1, x2, data_list, max_dim, control_k):
    vis_k = line(x0, x1, data_list)
    try:
        vis_k_next = line(x0, x2, data_list)
    except IndexError as e:
        # print(e)
        # print(sys.exc_info())
        vis_k_next = vis_k
    ind = np.argmax([control_k, vis_k, vis_k_next])
    return vis_k, vis_k_next, ind


logger = logging.getLogger('simple_example')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

logger.debug('debug message')
logger.info('info message')
logger.warning('warn message')
logger.error('error message')
logger.critical('critical message')

start_point=0
first_cluster=True

def build_graph_with_clusters(start_point, data_list, max_dim, DEBUG=False):
    x0 = start_point  # начало кластера
    cluster_start = start_point  # начало кластера
    x1 = x0 + 1  # рабочая вершина
    x2 = x1 + 1  # контрольная вершина
    cluster_start = x0
    cluster_size = 1
    clusters_count = 0
    # cluster_start.append(start_point)
    graph_array = np.eye(max_dim)
    graph_array.fill(0)
    control_k = line(x0, x1, data_list)
    #log.info("x0={} x1={}, x2={} control01={} ".format(x0, x1, x2, control_k))
    if max_dim == 2:  # если всего 2 вершины, матрица 2x2

        vis_k, vis_k_next, ind = is_cluster_found(
            x0, x1, x2, data_list, max_dim)
        #log.debug("1=Start cluster x0={} (x1={} x2={}) ind={} vis_k=({} {})".format(x0, x1, x2, ind, vis_k, vis_k_next))

        if ind == 2:  # end cluster x0
            graph_array[x0][x0] = 2
            # array_cluster_size[x0]
        else:
            graph_array[x1][x1] = 2
            # graph_array[x0][x0] = 1
            # graph_array[x1][x0] = 1
            return graph_array
        if max_dim == 3:  # если матрица 3x3
            vis_k, vis_k_next, ind = is_cluster_found(
                x0, x1, x2, data_list, max_dim)
            if ind == 0:  # end cluster x0
                #log.debug("2=Start cluster x0={} (x1={} x2={}) ind={} vis_k=({} {})".format(x0, x1, x2, ind, vis_k, vis_k_next))

                graph_array[x0][x0] = 2

            # graph_array.fill(1)
            # graph_array[x1][x1]=2
            return graph_array
    array_k = []
    array_cluster_start = np.arange(0, max_dim)
    array_cluster_sizes = np.arange(0, max_dim)
    interior_list = []
    array_cluster_sizes.fill(0)
    cluster_list = array_cluster_sizes.tolist()

    clusters_count = 0
    cluster_len = 1
    control_x = x1
    # -----------------------------------------------
    # Start main algoriithm
    # -----------------------------------------------
    d_cluster_begin={}
    control_k = line(x0, x1, data_list)
    control_2 = line(x0, x2, data_list)
    x0=0
    x1 = 1
    first_cluster=True
    start_cluster = x0
    p_cluster_begin=[]
    d_cluster_length={0:1}
    d_cluster_chain={0:[0]}
    while True:
        # x1 = x0 + 1
        x2 = x1 + 1

        cluster_len = 1
        while x2 <= max_dim - 1:

            # x2 = x1+1
            vis_k, vis_k_next, ind = is_cluster_found(
                x0, x1, x2, data_list, max_dim, control_k)
            control_2 = line(x0, x2, data_list)

            #log.info("x0={} x1={}, x2={} ind={} control_k={} control_2={}".format(x0, x1, x2, ind, control_k, control_2))
            # cluster end x0 start new cluster x1=x2
            # control_k=libe(x0,x1,data_list
            # flag1=False #
            # flag2=True
            if ind == 2: # найдено начало кластера:
                start_clustter=x0
                #log.debug(' найдено началo кластера в {} {} {} {} {}'.format(x1,d_cluster_begin,d_cluster_chain,d_cluster_begin,interior_list))

                #if x1==x0+1:
                if first_cluster:
                    #log.debug('2= найден первый кластер {} {} {}'.format(d_cluster_begin, d_cluster_chain, d_cluster_begin))

                    p_cluster_begin.append(x0)
                    d_cluster_chain[x0] = interior_list.insert(x0, x0)
                    d_cluster_length[x0] = cluster_len

                    #if collected_chain:
                        #list(interior_list).insert(0,x0)
                        ##log.debug("*****{}".format(interior_list))
                        # #interior_list.append(interior_list.insert(0,x0))
                        # d_cluster_chain[x0]=interior_list.insert(0,x0)
                        # d_cluster_begin[x0]=0
                        # d_cluster_length[x0]=cluster_len

                st.rays_plot(x0, data_list[x0], x2, data_list[x2])

                # if (x2 - x1 == 1) and cluster_len == 0:
                # TODO Fix patch #1
                if x2>=2:
                #if (x2 - x1 == 1):
                # if len(interior_list) == 0 and x1 == x0 + 1:
                    # ---------------------------
                    interior_list.append(x1)
                    list(array_cluster_sizes).append(interior_list)
                    cluster_list[x0] = interior_list
                    # test_list[0] = [2,3]
                    array_cluster_sizes[x0] = x2-x1+1
                # ---------------------------

                #log.debug("ind=2:****** Start={}{} interior_list={}".format(x0, x2, interior_list))
                # array_cluster_sizes[x0].append(cluster_list)
                # x0 = x1  # новое начало кластера x0=x1
                clusters_count += 1
                array_cluster_sizes[x1] += 1
                # TODO Fix patch #2

                cluster_list[x1] = interior_list

                x1 = x2
                x2 += 1
                control_k = line(x0, x1, data_list)
                control_2 = line(x0, x2, data_list)
                #log.info( "x0={} x1={}, x2={} ind={} control_k={} control_2={}".format( x0, x1, x2, ind, control_k, control_2))
                #log.debug("5 Cluster start={} interior_list={} cluster_len={}".format(x1, interior_list, cluster_len))


                interior_list = []
                # x1 = x0 + 1
                x2 = x1 + 1
                print("**0****", x0, x1, x2, control_k, ind)
                # array_k.append([x0, x1, x2, vis_k, vis_k_next, cluster_len])

                if DEBUG1:
                    print(
                        "DEBUG_1:From= ",
                        x0,
                        "To= ",
                        x1,
                        "k= ",
                        vis_k,
                        "Next= ",
                        x2,
                        "next_k=",
                        vis_k_next,
                        "cluster_size=",
                        cluster_size,
                        "ind=",
                        ind,
                        "cluster_len=",
                        cluster_len)
            if ind != 2:  # continue cluster: x1 собирание цепочки вершин для класиера, x1 входит в текущий кластер
                first_cluster=False
                #log.debvis_k_next,x0))
                interior_list.insert(0,x2)
                cluster_len += 1
                #log.debug("5 Cluster start={} interior_list={}".format(x1, interior_list))
                if len(array_cluster_sizes) == 0:
                    array_cluster_sizes.append(cluster_len)
                array_cluster_sizes[x1] += 1
                # x1=x2
                # control_k=line(x0,x1,data_list)
                x2 += 1
                print("**1****", x0, x1, x2, ind, cluster_len, interior_list)
                # if DEBUG1: print("DEBUG_1:From= ", x0, "To= ", x1, "k= ", vis_k, "Next= ", x2, "next_k=", vis_k_next,
                #                  "cluster_size=", cluster_size, "ind=", ind, "cluster_len=", cluster_len)
            array_k.append([x0, x1, x2, vis_k, vis_k_next, cluster_len])
            # x1 += 1
            # x2 += 1
            collected_chain=True
        if x2 > (max_dim - 1):
            cluster_len = x2 - x1
            array_cluster_sizes[x1] = cluster_len
            cluster_list[x1] = interior_list
            print("**111****", x0, x1, x2, ind, cluster_len, interior_list)
            print("------------------------------------------------------------")
            break

            is_growing = vis_k <= vis_k_next
            is_decrease = not is_growing
            if is_growing:
                # Вершина x2 вхоит в кластер? -да
                graph_array[x0][x1] = 1
                # graph_array[x0][x2] = 1
                graph_array[x1][x0] = 1
                # graph_array[x2][x0] = 1
                if DEBUG4:
                    print(
                        "DEBUG_4:From= ",
                        x0,
                        "To= ",
                        x1,
                        "k= ",
                        vis_k,
                        "Next= ",
                        x2,
                        "next_k=",
                        vis_k_next,
                        "cluster_size=",
                        cluster_size,
                        is_growing)

                # x0 = x1
                x1 = x1 + 1
                x2 = x1 + 1
                # TODO  graph_array[x0][x0] += 1
                graph_array[x0][x0] += 1
                # val=graph_array[x0][x0]
                # cluster_range=range(x0,val)
                # for i in range(x0,x0+cluster_range-1):
                #     for j in range(x0, x0+cluster_range-1):
                #             graph_array[i][j]=1
                # cluster_size = cluster_size + 1
                # graph_array[x1][x0] = 1
            else:
                # Вершина x1 вхоит в x0 кластер? -нет
                graph_array[x0][x0] = cluster_size
                cluster_size = 1
                # начало нового кластера в x1
                x0 = x1
                x1 = x0 + 1
                x2 = x1 + 1
                # TODO Проверить логику
                # graph_array[x0][x1] = 1
                # graph_array[x1][x0] = 1
                x1 = x0 + 1
                x2 = x1 + 1
                if DEBUG2:
                    print(
                        "DEBUG_2:",
                        x0,
                        x1,
                        x2,
                        vis_k,
                        vis_k_next,
                        cluster_size,
                        is_decrease)
        # if x0 == max_dim - 3:
        #     #graph_array[x0][x0] = cluster_size+1
        #     #graph_array[x0][x1] = 1
        #     #graph_array[x0][x2] = 1
        #     #graph_array[x1][x0] = 1
        #     #graph_array[x2][x0] = 1
        #     #graph_array[x2][x0] = 1
        #     break
        # if x1 == max_dim - 1:
        #     break
    if DEBUG:
        lenk = len(array_k)
        print("****  Array_k  ****")
        for i in range(0, lenk):
            print("DEBUG_5: ind=", i, array_k[i])
        print("******************")
        print("****  Array_cluster_size  ({}) ****".format(clusters_count))
        for i in range(0, len(array_cluster_sizes)):
            print("DEBUG_5: ind=", i, array_cluster_sizes[i])
        print("******************")
    print(cluster_list)
    return graph_array



graph_array = build_graph_with_clusters(start_point, data_list, max_dim, True)

plt.show()
# print(graph_array)
# fig = plt.figure()
# ax = fig.add_axes([0,0,1,1])
# x = ['C', 'C++', 'Java', 'Python', 'PHP']
# y = [4,2,3,7,3]
# ax.bar(x,y)
plt.matshow(graph_array)

plt.show()

# eOutput = pd.DataFrame(graph_array)
# writer = pd.ExcelWriter('ArrayFromPycharm.xlsx', engine='xlsxwriter')
#
# # Convert the dataframe to an XlsxWriter Excel object.
# eOutput.to_excel(writer, sheet_name='Sheet1', index=False)
#
# # Close the Pandas Excel writer and output the Excel file.
# writer.save()

# ---------------------------------  Version 1.0 ------------------------------
