# This is a sample Python script.

# Token:
# cd5c0f2b8bb97f0cd4e46dd6f0e5647922a163d3

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pandas as pd
import numpy as np
import xlsxwriter



def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# ['Num','Date','MinTemp','RayFrom','RayTo','dx','dy','K','B','FLiine']
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
            print_hi('PyCharm')

df = pd.read_csv('daily-min-temperatures-02.csv',
                 names=['Date', 'MinTemp', 'RayFrom', 'RayTo', 'dx', 'dy', 'K', 'B', 'FLiine'])
data_list = df.to_numpy()



def line(x0,x1,x):
    y0 = data_list[x0][1]
    y1 = data_list[x1][1]

    k = (y1 - y0) / (x1 - x0)
    B = (x1 * y0 - x0 * y1) / (x1 - x0)
    eps=1.e-3
    return [k,B,k * x + B,(k * x + B-data_list[x][1]) <= 0]

def is_visible(x0,x1,x):
    y0 = data_list[x0][1]
    y1 = data_list[x1][1]

    k = (y1 - y0) / (x1 - x0)
    B = (x1 * y0 - x0 * y1) / (x1 - x0)
    eps=1.e-3
    return (k * x + B-data_list[x][1]) <= 0

max_dim=9
graph_array = np.eye(max_dim)
iv=is_visible(0,1,2)



print("******",line(0,1,1)[0],line(0,1,1)[1],line(0,1,1)[2],line(0,1,2)[3])

#exit()

x0 = 0
x1 = x0+1
array_k=[]
graph_array.fill(0)
while True:
    vis_k = line(x0, x1, x1)[0]
    vis_k_next = line(x0, x1 + 1, x1+1)[0]
    #print("From= ",x0, "To= ",x1, "k= ",vis_k ,"Next= ",x1 + 1,"next_k=",vis_k_next)
    cluster_size = 1
    #array_k.append([x0,x1,vis_k,vis_k_next,cluster_size])
    graph_array[x0][x0] = 1
    #x1=x0+1
    #for x1 in range(x0+1,max_dim-1):
    while x1 <= max_dim-2:
        vis_k = line(x0, x1, x1)[0]
        vis_k_next = line(x0, x1+1, x1)[0]
        graph_array[x0][x0] = cluster_size
        print("From= ", x0, "To= ", x1, "k= ", vis_k, "Next= ", x1 + 1, "next_k=", vis_k_next)
        array_k.append([x0, x1, vis_k,vis_k_next,cluster_size])
        is_growing = vis_k < vis_k_next
        is_decrease=not is_growing
        if is_growing:
            # Вершина вхоит в кластер? -да
            #vis_k=vis_k_next
            #x0=x1+1
            graph_array[x0][x1] = 1
            graph_array[x1][x0] = 1
            x1=x1+1
            cluster_size = cluster_size+1
            # graph_array[x1][x0] = 1
        else:
            # Вершина вхоит в кластер? -нет
            cluster_size=1
            # начало нового кластера
            x0=x1
            graph_array[x0][x1] = 1
            graph_array[x1][x0] = 1
            x1=x0+1

            print(x0, x1,x1+1, vis_k,vis_k_next,cluster_size,is_growing,is_decrease)
    if x0 < 7:
        print("******************")
        print("array_k=\n",array_k)
        print("******************")
        break
    else:
        x0+=1

# my_range_x1=range(x0,max_dim-2)
# for x1 in range(2,max_dim-2):
#
#     vis_k1=line(x0, x1, x1)[0]
#
#     print(x0,x1,vis_k,vis_k1)
# # for x0 in my_range_x0:
#     my_range_x1=range(x0+1,max_dim-2)
#     my_range_x1=range(x0+1,x0+1)
#     for x1 in my_range_x1:
#         my_range_cur_x=range(x1,max_dim-1)
#         vis_k = line(x0,x1,cur_x)[0]
#         print("kkkkk=",k)
#         for cur_x in my_range_cur_x:
#             par_line = line(x0,x1,cur_x)
#             par_y = data_list[cur_x][1]
#             vis_k = line(x0, x1, cur_x)
#             print("Analyse cur_x=",cur_x, vis_k)
#             num_visible = 0
#
#             if is_visible(x0,x1,cur_x):
#                 num_visible += 1
#                 print("Видно {0} из {1} через ({2},{3}) num {4}".format(cur_x,x0,x0,x1,num_visible))
#                 print("x0 = ", x0, " x1= ", x1, " cur_x = ", cur_x, " par_line = ", par_line, " par_y = ", par_y," ",is_visible(x0,x1,cur_x))
#                 graph_array[x0][cur_x] = 1
#                 graph_array[cur_x][x0] = 1
#
#                 if num_visible>0:
#                     my_range_cur_x=range(cur_x+1,max_dim-1)
#                     x1=cur_x
#                     print("New Range_cur_x=",my_range_cur_x)
#                     break
#

x0 = 0


# while x0 < max_dim - 2:
#     x1 = x0 + 1
#     cur_x = x1 + 1
#     while cur_x < max_dim - 1:
#         vis = line(x0,x1,cur_x)
#         graph_array[x0][x1] = 1
#         graph_array[x1][x0] = 1
#         print(cur_x)
#
#         if vis[3]:
#             print("Видно {0} из {1} через ({2},{3})".format(cur_x, x0, x0, x1))
#             print("x0 = ", x0, " x1= ", x1, " cur_x = ", cur_x, " par_line = ", vis[2], " par_y = ", data_list[x1][1],
#                   " ",
#                   is_visible(x0, x1, cur_x))
#
#             x1 = cur_x
#             graph_array[x0][x1] = 1
#             graph_array[x1][x0] = 1
#         cur_x += 1
#
#     x0 += 1

# x0 = 0
# x1 = 1
# cur_x = 2
#
# while x0 < 8:
#     vis = line(x0, x1, cur_x)
#     graph_array[x0][x1] = 1
#     graph_array[x1][x0] = 1
#     visible_counter = 0
#     if vis[3]:
#         visible_counter += 1
#         x1 = cur_x
#
#         if cur_x < 8: cur_x += 1
#         else:
#             graph_array[x0][x1] = 1
#             graph_array[x1][x0] = 1
#             break
#         print(cur_x)
#     else:
#         print(graph_array[x0])
#         x0 = x1
#         x1 = x0 + 1
#         cur_x = x1 + 1
#         # graph_array[x0][x1] += visible_counter
#         # graph_array[x1][x0] += visible_counter








print(graph_array)
#print(graph_array[362])
#print(graph_array[325])

eOutput = pd.DataFrame(graph_array)
writer = pd.ExcelWriter('ArrayFromPycharm.xlsx', engine='xlsxwriter')

# Convert the dataframe to an XlsxWriter Excel object.
eOutput.to_excel(writer, sheet_name='Sheet1', index=False)

# Close the Pandas Excel writer and output the Excel file.
writer.save()

