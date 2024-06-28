### Compute IRA with cardinality
import numpy as np
import os
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt

# Scenario 1
x = np.array([1, 9/10, 2/3, 1/3])

# Cardinal 1
ira1 = x

# Cardinal 2
ira2 = np.zeros_like(x)
# Read files
problems = ["CC", "CT"]
ira = {
    "CC": {
        "LP": 0,
        "MTL": 0
    },
    "CT": {
        "LP": 0,
        "MTL": 0
}
}
for i, problem in enumerate(problems):
    # list files
    files = [f for f in os.listdir('ira/scenar1/') if f.startswith(problem) and f.endswith("2-2.txt")]
    lines = []
    for file in files:
        with open(os.path.join('ira/scenar1/', file), "r") as f:
            lines += f.readlines()
    for line in lines:
        if "LP" in line:
            ira[problem]["LP"] += 1
        elif "MTL" in line:
            ira[problem]["MTL"] += 1

# Compute the ratio
ratios = {
    "CC": {"LP": 0, "MTL": 0},
    "CT": {"LP": 0, "MTL": 0}
}
for prob in problems:
    count = ira[prob]["LP"] + ira[prob]["MTL"]
    print(f"Ratio of {prob}:")
    print(f"LP: {ira[prob]['LP']/count}")
    print(f"MTL: {ira[prob]['MTL']/count:.2f}")

    ratios[prob]["LP"] = ira[prob]["LP"]/count
    ratios[prob]["MTL"] = ira[prob]["MTL"]/count

ira2 = [xi * ratios["CC"]["LP"] + (1-xi)/2 * ratios["CT"]["MTL"] for xi in x]


# Cardinal 3
ira3 = np.zeros_like(x)
# Read files
problems = ["CC", "CT", "PP"]
ira = {
    "CC": {
        "LP": 0,
        "MTL": 0,
        "MM": 0
    },
    "CT": {
        "LP": 0,
        "MTL": 0,
        "MM": 0
    },
    "PP": {
        "LP": 0,
        "MTL": 0,
        "MM": 0
    }
}
for i, problem in enumerate(problems):
    # list files
    files = [f for f in os.listdir('ira/scenar1/') if f.startswith(problem) and f.endswith("3.txt")]
    lines = []
    for file in files:
        with open(os.path.join('ira/scenar1/', file), "r") as f:
            lines += f.readlines()
    for line in lines:
        if "LP" in line:
            ira[problem]["LP"] += 1
        elif "MTL" in line:
            ira[problem]["MTL"] += 1
        elif "MM" in line:
            ira[problem]["MM"] += 1

# Compute the ratio
ratios = {
    "CC": {"LP": 0, "MTL": 0, "MM": 0},
    "CT": {"LP": 0, "MTL": 0, "MM": 0},
    "PP": {"LP": 0, "MTL": 0, "MM": 0}
}
for prob in problems:
    count = ira[prob]["LP"] + ira[prob]["MTL"] + ira[prob]["MM"]
    print(f"Ratio of {prob}:")
    print(f"LP: {ira[prob]['LP']/count}")
    print(f"MTL: {ira[prob]['MTL']/count:.2f}")
    print(f"MM: {ira[prob]['MM']/count:.2f}")

    ratios[prob]["LP"] = ira[prob]["LP"]/count
    ratios[prob]["MTL"] = ira[prob]["MTL"]/count
    ratios[prob]["MM"] = ira[prob]["MM"]/count

ira3 = [xi * ratios["CC"]["LP"] + (1-xi)/2 * ratios["CT"]["MTL"] + (1-xi)/2 * ratios["PP"]["MM"] for xi in x]


print(f"IRA1: {ira1}")
print(f"IRA2: {ira2}")
print(f"IRA3: {ira3}")

### Plot

# Define figure size
fig_width = 3.5  # single column width in inches
fig_height = 2.5  # height in inches
fig_size = (fig_width, fig_height)
# Bar chart
fig, ax = plt.subplots(figsize=fig_size)

index = np.arange(1,4,dtype=float)
gap = 0.05
bar_width = (1-gap) / 5
colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
mpl.rcParams['hatch.linewidth'] = 0.2


ax.plot(index,[ira1[0],ira2[0],ira3[0]], label=f"$\pi$={x[0]:.2f}", color=colors[0], marker='o')
ax.plot(index,[ira1[1],ira2[1],ira3[1]], label=f"$\pi$={x[1]:.2f}", color=colors[1], marker='o')
ax.plot(index,[ira1[2],ira2[2],ira3[2]], label=f"$\pi$={x[2]:.2f}", color=colors[2], marker='o')
ax.plot(index,[ira1[3],ira2[3],ira3[3]], label=f"$\pi$={x[3]:.2f}", color=colors[3], marker='o')

ax.set_xticks(index,["{LP}", "{LP,MTL}", "{LP,MTL,MM}"], fontsize=8)
ax.set_xlabel("Set of OP classes", fontsize=8)
ax.set_ylabel("IRA", fontsize=8),
ax.tick_params(axis='x', labelsize=8)
ax.tick_params(axis='y', labelsize=8)
ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
                      ncols=2, mode="expand", borderaxespad=0., fontsize=8)
#plt.tight_layout()
#plt.show()

# Scenario 3
x = np.array([1, 9/10, 2/3, 1/3])

# Cardinal 1
ira1 = x

# Cardinal 2
ira2 = np.zeros_like(x)
# Read files
problems = ["CC", "CT"]
ira = {
    "CC": {
        "LP": 0,
        "MTL": 0
    },
    "CT": {
        "LP": 0,
        "MTL": 0
}
}
for i, problem in enumerate(problems):
    # list files
    files = [f for f in os.listdir('ira/scenar3/') if f.startswith(problem) and f.endswith("2.txt")]
    lines = []
    for file in files:
        with open(os.path.join('ira/scenar3/', file), "r") as f:
            lines += f.readlines()
    for line in lines:
        if "LP" in line:
            ira[problem]["LP"] += 1
        elif "MTL" in line:
            ira[problem]["MTL"] += 1
            
# Compute the ratio
ratios = {
    "CC": {"LP": 0, "MTL": 0},
    "CT": {"LP": 0, "MTL": 0}
}

for prob in problems:
    count = ira[prob]["LP"] + ira[prob]["MTL"]
    print(f"Ratio of {prob}:")
    print(f"LP: {ira[prob]['LP']/count}")
    print(f"MTL: {ira[prob]['MTL']/count:.2f}")

    ratios[prob]["LP"] = ira[prob]["LP"]/count
    ratios[prob]["MTL"] = ira[prob]["MTL"]/count
    
ira2 = [xi * ratios["CC"]["LP"] + (1-xi)/2 * ratios["CT"]["MTL"] for xi in x]

# Cardinal 3
ira3 = np.zeros_like(x)
# Read files
problems = ["CC", "CT", "PP"]
ira = {
    "CC": {
        "LP": 0,
        "MTL": 0,
        "MM": 0
    },
    "CT": {
        "LP": 0,
        "MTL": 0,
        "MM": 0
    },
    "PP": {
        "LP": 0,
        "MTL": 0,
        "MM": 0
    }
}
for i, problem in enumerate(problems):
    # list files
    files = [f for f in os.listdir('ira/scenar3/') if f.startswith(problem) and f.endswith("3.txt")]
    lines = []
    for file in files:
        with open(os.path.join('ira/scenar3/', file), "r") as f:
            lines += f.readlines()
    for line in lines:
        if "LP" in line:
            ira[problem]["LP"] += 1
        elif "MTL" in line:
            ira[problem]["MTL"] += 1
        elif "MM" in line:
            ira[problem]["MM"] += 1
            
# Compute the ratio
ratios = {
    "CC": {"LP": 0, "MTL": 0, "MM": 0},
    "CT": {"LP": 0, "MTL": 0, "MM": 0},
    "PP": {"LP": 0, "MTL": 0, "MM": 0}
}

for prob in problems:
    count = ira[prob]["LP"] + ira[prob]["MTL"] + ira[prob]["MM"]
    print(f"Ratio of {prob}:")
    print(f"LP: {ira[prob]['LP']/count}")
    print(f"MTL: {ira[prob]['MTL']/count:.2f}")
    print(f"MM: {ira[prob]['MM']/count:.2f}")

    ratios[prob]["LP"] = ira[prob]["LP"]/count
    ratios[prob]["MTL"] = ira[prob]["MTL"]/count
    ratios[prob]["MM"] = ira[prob]["MM"]/count
    
ira3 = [xi * ratios["CC"]["LP"] + (1-xi)/2 * ratios["CT"]["MTL"] + (1-xi)/2 * ratios["PP"]["MM"] for xi in x]

print(f"IRA1: {ira1}")
print(f"IRA2: {ira2}")
print(f"IRA3: {ira3}")

### Plot

# Define figure size
fig_width = 3.5  # single column width in inches
fig_height = 2.5  # height in inches
fig_size = (fig_width, fig_height)
# Bar chart
#fig, ax = plt.subplots(figsize=fig_size)

index = np.arange(1,4,dtype=float)
gap = 0.05
bar_width = (1-gap) / 5
colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
mpl.rcParams['hatch.linewidth'] = 0.2


ax.plot(index,[ira1[0],ira2[0],ira3[0]], label=f"\pi={x[0]:.2f}", color=colors[0], marker='o', linestyle='--')
ax.plot(index,[ira1[1],ira2[1],ira3[1]], label=f"\pi={x[1]:.2f}", color=colors[1], marker='o', linestyle='--')
ax.plot(index,[ira1[2],ira2[2],ira3[2]], label=f"\pi={x[2]:.2f}", color=colors[2], marker='o', linestyle='--')
ax.plot(index,[ira1[3],ira2[3],ira3[3]], label=fr"$\pi$={x[3]:.2f}", color=colors[3], marker='o', linestyle='--')

#ax.set_xticks(index)
#ax.set_xticklabels(["LP", "LP+MTL", "LP+MTL+MM"])
#ax.set_ylabel("IRA")
#ax.legend()
plt.grid(color='gray', linewidth=0.5, zorder=0)
plt.subplots_adjust(right=0.7)
plt.tight_layout()
plt.show()