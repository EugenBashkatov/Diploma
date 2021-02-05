from scipy.stats import logistic
from scipy.stats import norm
import matplotlib.pyplot as plt
import numpy as np

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
    plt.bar(x_normal, normal, align='center')
    # plt.plot(x_normal,normal)
    plt.show()
    return normal_data

normal_distribution(201,10)


