# Compute global optimality loss
import os
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np

optim_loss = {
    "CC":
        {
        "LP": 0,
        "MTL": 15,
        "MM": 14
        },
    "CT":
        {
        "LP": 116,
        "MTL": 0,
        "MM": 116
        },
    "PP":
        {
        "LP": 92,
        "MTL": 92,
        "MM": 0
        }
}

model = "llama3"
## Scenario 1
countLP = {"CC": 0, "CT": 0, "PP": 0}
countMTL = {"CC": 0, "CT": 0, "PP": 0}
countMM = {"CC": 0, "CT": 0, "PP": 0}
# Ratio of classification
problems = ["CC", "CT", "PP"]
# Read all the files in /ira/scenar1
path = "ira/scenar1"
files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

for file in files:
    if "classifier" in file:
        filename = os.path.join(path, file)
        with open(filename, "r") as f:
            content = f.readlines()
        prob = file.split("-")[0]
        for line in content:
            if "LP" in line:
                countLP[prob] += 1
            elif "MTL" in line:
                countMTL[prob] += 1
            elif "MM" in line:
                countMM[prob] += 1
# Compute the ratio
cumul_s1 = {"CC": 0, "CT": 0, "PP": 0}
for prob in problems:
    count = countLP[prob] + countMTL[prob] + countMM[prob]
    print(f"Ratio of {prob}:")
    print(f"LP: {countLP[prob]/count:.2f}")
    print(f"MTL: {countMTL[prob]/count:.2f}")
    print(f"MM: {countMM[prob]/count:.2f}")

    cumul_s1[prob] =  countLP[prob]/count * optim_loss[prob]["LP"] + countMTL[prob]/count * optim_loss[prob]["MTL"] + countMM[prob]/count * optim_loss[prob]["MM"]

    print(f"Average optimality loss for {prob}: {cumul_s1[prob]}")
    print()

## Scenario 2
countLP = {"CC": 0, "CT": 0, "PP": 0}
countMTL = {"CC": 0, "CT": 0, "PP": 0}
countMM = {"CC": 0, "CT": 0, "PP": 0}

# Read all the files in /ira/scenar2
path = "ira/scenar2"
files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
for file in files:
    if "classifier" in file:
        filename = os.path.join(path, file)
        with open(filename, "r") as f:
            content = f.readlines()
        prob = file.split("-")[0]
        for line in content:
            if "LP" in line:
                countLP[prob] += 1
            elif "MTL" in line:
                countMTL[prob] += 1
            elif "MM" in line:
                countMM[prob] += 1
# Compute the ratio
cumul_s2 = {"CC": 0, "CT": 0, "PP": 0}
for prob in problems:
    count = countLP[prob] + countMTL[prob] + countMM[prob]
    print(f"Ratio of {prob}:")
    print(f"LP: {countLP[prob]/count:.2f}")
    print(f"MTL: {countMTL[prob]/count:.2f}")
    print(f"MM: {countMM[prob]/count:.2f}")

    cumul_s2[prob] =  countLP[prob]/count * optim_loss[prob]["LP"] + countMTL[prob]/count * optim_loss[prob]["MTL"] + countMM[prob]/count * optim_loss[prob]["MM"]

    print(f"Average optimality loss for {prob}: {cumul_s2[prob]}")
    print()


## Scenario 3
countLP = {"CC": 0, "CT": 0, "PP": 0}
countMTL = {"CC": 0, "CT": 0, "PP": 0}
countMM = {"CC": 0, "CT": 0, "PP": 0}

# Read all the files in /ira/scenar3
path = "ira/scenar3"
files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
for file in files:
    if "classifier" in file:
        filename = os.path.join(path, file)
        prob = file.split("-")[0]
        ops = file.split("-")[-1]
        if prob in problems and ops == '3.txt':
            with open(filename, "r") as f:
                content = f.readlines()
            for line in content:
                if "LP" in line:
                    countLP[prob] += 1
                elif "MTL" in line:
                    countMTL[prob] += 1
                elif "MM" in line:
                    countMM[prob] += 1
# Compute the ratio
cumul_s3 = {"CC": 0, "CT": 0, "PP": 0}
for prob in problems:
    count = countLP[prob] + countMTL[prob] + countMM[prob]
    print(f"Ratio of {prob}:")
    print(f"LP: {countLP[prob]/count:.2f}")
    print(f"MTL: {countMTL[prob]/count:.2f}")
    print(f"MM: {countMM[prob]/count:.2f}")

    cumul_s3[prob] =  countLP[prob]/count * optim_loss[prob]["LP"] + countMTL[prob]/count * optim_loss[prob]["MTL"] + countMM[prob]/count * optim_loss[prob]["MM"]

    print(f"Average optimality loss for {prob}: {cumul_s3[prob]:.2f}")
    print()

## Plot the results

# Define figure size
fig_width = 3.5  # single column width in inches
fig_height = 2.5  # height in inches
fig_size = (fig_width, fig_height)
# Bar chart
fig, ax = plt.subplots(figsize=fig_size)

index = np.arange(3,dtype=float)
gap = 0.05
bar_width = (1-gap) / 5
colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
mpl.rcParams['hatch.linewidth'] = 0.2


for i, prob in enumerate(problems):
    ax.bar(i - bar_width, cumul_s1[prob], bar_width, label=prob, color=colors[0], linewidth=0.5, edgecolor='black', zorder=3)
    ax.bar(i, cumul_s2[prob], bar_width, color=colors[1], linewidth=0.5, edgecolor='black', zorder=3)
    ax.bar(i + bar_width, cumul_s3[prob], bar_width, color=colors[2], linewidth=0.5, edgecolor='black', zorder=3)

index = np.arange(3)
ax.legend(["Basic", "Contextualized", "Error-informed"], title="Prompting", title_fontsize=8, loc='best', fontsize=8)
ax.tick_params(axis='x', labelsize=8)
ax.tick_params(axis='y', labelsize=8)    
ax.set_xticks(index, problems, minor=False, fontsize=8)
ax.set_xlabel("Performance metric", fontsize=8)
ax.set_ylabel("Average relative optimality loss (%)", fontsize=8)
plt.grid(color='gray', linewidth=0.5, zorder=0)
plt.subplots_adjust(right=0.7)
plt.tight_layout()
plt.show()