### Compute optimality loss LP - MTL - MM

import numpy as np
from solver import Solver
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt

# Prices
c = np.array([8.7,8.7,8.7,8.7,8.7,8.7,8.7,12.2,12.2,12.2,12.2,18.2,18.2,18.2,18.2,18.2,18.2,12.2,12.2,8.7,8.7,8.7,8.7,8.7])
c = np.tile(c,2)
# Power demand
P = np.random.randint(3, 10, 24)
P = np.tile(P,2)

n = 10000
current_SOC = 0.3
battery_capacity = 82
max_charging_power = 22

lossLP = {
    "MTL": 0,
    "MM": 0,
    "CST": 0
}
lossMTL = {
    "LP": 0,
    "MM": 0,
    "CST": 0
}
lossMM = {
    "LP": 0,
    "MTL": 0,
    "CST": 0
}

starting_time = np.random.randint(0, 24, n)
duration = np.random.randint(4, 10, n)
for i in range(n):
    # LP
    c_i = c[starting_time[i]:starting_time[i]+duration[i]]
    A = -np.ones(duration[i]).reshape(1,-1)
    b = -np.array([(1 - current_SOC) * battery_capacity])
    lb = np.zeros(duration[i])
    ub = max_charging_power * np.ones(duration[i])
    res_LP = Solver.solve_LP(c_i, A, b, lb=lb, ub=ub)
    obj_CC_LP = np.dot(c_i, res_LP)
    obj_CT_LP = len(res_LP)
    obj_PP_LP = np.max(res_LP+P[starting_time[i]:starting_time[i]+duration[i]])

    # MTL
    A = 1
    B = 1 / battery_capacity
    x_i = current_SOC
    x_f = 1
    Lu = 0
    Uu = max_charging_power
    Lx = 0
    Ux = 1

    res_MTL = Solver.solve_MTL(A, B, x_i, x_f, Lu, Uu, Lx, Ux, n=duration[i])
    l = len(res_MTL)
    obj_CC_MTL = np.dot(c_i[:l], res_MTL)
    obj_CT_MTL = l
    obj_PP_MTL = np.max(res_MTL+P[starting_time[i]:starting_time[i]+l])

    # MM
    func = [lambda x,j=j: x[j] + P[starting_time[i]+j] for j in range(duration[i])]
    Aeq = -np.ones(duration[i]).reshape(1,-1)
    beq = -np.array([(1 - current_SOC) * battery_capacity])
    A = None
    b = None
    lb = np.zeros(duration[i]).reshape(1,-1)
    ub = max_charging_power * np.ones(duration[i]).reshape(1,-1)
    res_MM = Solver.solve_MM(func, A, b, Aeq, beq, lb=lb, ub=ub)
    obj_CC_MM = np.dot(c_i, res_MM)
    obj_CT_MM = len(res_MM)
    obj_PP_MM = np.max(res_MM+P[starting_time[i]:starting_time[i]+duration[i]])


    # CST (constant power)
    res_CST = np.ones(duration[i]) * ((1 - current_SOC) * battery_capacity) / duration[i]
    obj_CC_CST = np.dot(c_i, res_CST)
    obj_CT_CST = len(res_CST)
    obj_PP_CST = np.max(res_CST+P[starting_time[i]:starting_time[i]+duration[i]])

    '''
    # Plot power vectors
    fig_width = 3.5  # single column width in inches
    fig_height = 2.5  # height in inches
    fig_size = (fig_width, fig_height)
    fig, (ax1,ax2) = plt.subplots(2, 1, figsize=fig_size, sharex=True, height_ratios=[2, 1])
    
    ax1.stairs(res_CST, label="Constant Power", linewidth=2,zorder=2)
    ax1.stairs(res_LP, label="Charging Cost", linewidth=2,zorder=2)
    ax1.stairs(res_MTL, label="Charging Time", linewidth=2,zorder=2)
    ax1.stairs(res_MM, label="Power Peak", linewidth=2,zorder=2)
    
    ax1.set_ylabel("Power (kW)", fontsize=8)
    ax1.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left', ncols=2, mode="expand", borderaxespad=0., fontsize=8)
    ax1.grid(zorder=0)
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)

    lns1 = ax2.stairs(c[starting_time[i]:starting_time[i]+duration[i]], color='k', label="Price", linewidth=2, zorder=2)
    ax2.set_ylabel("Price (cents/kWh)", fontsize=8)
    ax2.set_xlabel("Time (hours)", fontsize=8)
    ax2b = ax2.twinx()
    lns2 = ax2b.stairs(P[starting_time[i]:starting_time[i]+duration[i]], color='k', linestyle=':', label="Non-flexible load", linewidth=2, zorder=2)
    ax2b.set_ylabel("Power (kW)", fontsize=8)

    # added these three lines
    labs = ["Price", "Non-flexible load"]
    ax2.legend([lns1,lns2], labs, bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left', ncols=2, mode="expand", borderaxespad=0., fontsize=8)
    ax2.grid(zorder=0)
    ax1.tick_params(axis='x', labelsize=8)
    ax1.tick_params(axis='y', labelsize=8)
    ax2b.tick_params(axis='y', labelsize=8)

    fig.tight_layout()
    plt.show()
    '''

    lossLP["MTL"] += (obj_CC_MTL - obj_CC_LP) / obj_CC_LP
    lossLP["MM"] += (obj_CC_MM - obj_CC_LP) / obj_CC_LP
    lossLP["CST"] += (obj_CC_CST - obj_CC_LP) / obj_CC_LP

    lossMTL["LP"] += (obj_CT_LP - obj_CT_MTL) / obj_CT_MTL
    lossMTL["MM"] += (obj_CT_MM - obj_CT_MTL) / obj_CT_MTL
    lossMTL["CST"] += (obj_CT_CST - obj_CT_MTL) / obj_CT_MTL

    lossMM["LP"] += (obj_PP_LP - obj_PP_MM) / obj_PP_MM
    lossMM["MTL"] += (obj_PP_MTL - obj_PP_MM) / obj_PP_MM
    lossMM["CST"] += (obj_PP_CST - obj_PP_MM) / obj_PP_MM



# Average
lossLP["MTL"] /= n/100
lossLP["MM"] /= n/100
lossLP["CST"] /= n/100
print(lossLP)

lossMTL["LP"] /= n/100
lossMTL["MM"] /= n/100
lossMTL["CST"] /= n/100
print(lossMTL)

lossMM["LP"] /= n/100
lossMM["MTL"] /= n/100
lossMM["CST"] /= n/100
print(lossMM)
