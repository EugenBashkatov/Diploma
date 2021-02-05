from matplotlib import pyplot as plt
from matplotlib import style
import pandas as pd
import numpy as np

input_file_name='daily-min-temperatures-02.csv'
df = pd.read_csv(input_file_name,
                 names=['Date', 'MinTemp'])

data_list = df.to_numpy()

x = []
y = []

for i in range(0,len(data_list)):
    data_list[i][0] = i
    x.append(i)
    y.append(data_list[i][1])
    print(data_list[i])

print("@@@@ X @@@@ ", x)
print("@@@@ Y @@@@ ", y)
style.use('ggplot')

x1 = [0,1,2]
y1 = [2,2,2]

# x2 = [0,0,0]
# y2 = [4,3,2]


# plt.plot(x1,y1)
# plt.plot(x2,y2)

# plt.legend(["Dataset 1", "Dataset 2"])
#
# plt.title('Epic Info')
# plt.ylabel('Y axis')
# plt.xlabel('X axis')
#
# plt.show()
#
#
plt.bar(x, y, align='center')
#
#
#
#
# plt.title('Epic Info')
# plt.ylabel('Y axis')
# plt.xlabel('X axis')
#
plt.show()

