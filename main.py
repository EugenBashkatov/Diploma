# This is a sample Python script.

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


# Cov = pd.read_csv("path/to/file.txt",
#                 sep='\t',
#                names=["Sequence", "Start", "End", "Coverage"])
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
x1 = 1


print("******",line(0,1,1)[0],line(0,1,1)[1],line(0,1,1)[2],line(0,1,2)[3])
# exit()
my_range_x0=range(0,max_dim-1)
for x0 in range(0, max_dim):

    for x1 in range(x0+1, max_dim-2):
        my_range_cur_x=range(x1,max_dim-1)

        for cur_x in my_range_cur_x:
            par_line = line(x0,x1,cur_x)
            par_y = data_list[cur_x][1]
            print("Analyse cur_x=",cur_x)
            num_visible = 0

            if is_visible(x0,x1,cur_x):
                num_visible += 1
                print("Видно {0} из {1} через ({2},{3}) num {4}".format(cur_x,x0,x0,x1,num_visible))
                print("x0 = ", x0, " x1= ", x1, " cur_x = ", cur_x, " par_line = ", par_line, " par_y = ", par_y," ",is_visible(x0,x1,cur_x))
                graph_array[x0][cur_x] = 1
                graph_array[cur_x][x0] = 1

                if num_visible>0:
                    my_range_cur_x=range(cur_x+1,max_dim-1)
                    x1=cur_x
                    print("New Range_cur_x=",my_range_cur_x)
                    break

print(graph_array)
#print(graph_array[362])
#print(graph_array[325])

eOutput = pd.DataFrame(graph_array)
writer = pd.ExcelWriter('ArrayFromPycharm.xlsx', engine='xlsxwriter')

# Convert the dataframe to an XlsxWriter Excel object.
eOutput.to_excel(writer, sheet_name='Sheet1', index=False)

# Close the Pandas Excel writer and output the Excel file.
writer.save()

