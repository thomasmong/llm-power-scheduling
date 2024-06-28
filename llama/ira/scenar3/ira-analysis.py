import os
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np

# Chemin du dossier contenant les fichiers (dossier ira)
folder_path = os.path.join(os.getcwd(), 'ira/scenar3')


corres = {
    "CC": ["LP","QP","CP"],
    "CT": ["MTL"],
    "PV": ["QP","CP"],
    "GD": ["CP"],
    "PP": ["MM"]
}

ira_tab = {
    "CC": None,
    "CT": None,
    "PP": None,
    "PV": None,
    "GD": None
}

for op in ira_tab.keys():
    ira_tab[op] = {
        "imp": {
            "noTP": {
                "good": [0 for i in range(5)],
                "total": None
            },
            "TP": {
                "good": [0 for i in range(5)],
                "total": None
            }
        },
        "exp": {
            "noTP": {
                "good": [0 for i in range(5)],
                "total": None
            },
            "TP": {
                "good": [0 for i in range(5)],
                "total": None
            }
        }
    }

total_time = 0

for pb in corres.keys():
    for diff in ["imp", "exp"]:
        for tp in ["noTP","TP"]:
            for num_ops in range(1, 6):

                num_requests = None

                # Nom du fichier
                filename = f"{pb}-{diff}-{tp}-ira-llama3-classifier-scenar3-{num_ops}.txt"

                # Si fichier n'existe pas, ajouter une ligne avec ira=0
                if not os.path.exists(os.path.join(folder_path, filename)):
                    # S'il ne s'agit pas de MTL avec TP
                    if (pb == "CT" and tp == "TP"):
                        ira_tab[pb][diff][tp]["good"][num_ops-1] = None
                    else:
                        ira_tab[pb][diff][tp]["good"][num_ops-1] = 0
                else:
                    # Lire le contenu du fichier
                    with open(os.path.join(folder_path, filename), 'r') as file:
                        content = file.readlines()
                    
                    # Count the number of requests
                    num_requests = len(content) - 1

                    # Count good classifications
                    num_good = 0
                    for line in content[:-1]:
                        line = line.strip()
                        if line in corres[pb]:
                            num_good += 1
                    
                    total_time += float(content[-1].split(": ")[1])

                    # Ajouter les données au DataFrame
                    ira_tab[pb][diff][tp]["good"][num_ops-1] += num_good
            ira_tab[pb][diff][tp]["total"] = num_requests

# Print total time
print(total_time)

## Plotting
# Define figure size
fig_width = 7  # single column width in inches
fig_height = 2.5  # height in inches
fig_size = (fig_width, fig_height)
# Bar chart
fig, ax = plt.subplots(figsize=fig_size)

index = np.arange(5)
gap = 0.3
bar_width = (1-gap) / 5

colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
mpl.rcParams['hatch.linewidth'] = 0.2

patches = []
general_total = [0] * 5
general_good = [0] * 5

for i, op in enumerate(ira_tab.keys()):
    for j in range(5):
        # Explicit ira
        if op != "CT":
            good = ira_tab[op]["exp"]["noTP"]["good"][j] + ira_tab[op]["exp"]["TP"]["good"][j]
            total = ira_tab[op]["exp"]["noTP"]["total"] + ira_tab[op]["exp"]["TP"]["total"]
            general_good[j] += good
            general_total[j] += total
        else:
            good = ira_tab[op]["exp"]["noTP"]["good"][j]
            total = ira_tab[op]["exp"]["noTP"]["total"]
            general_good[j] += good
            general_total[j] += total
        ira = good / total if total != 0 else 0
        ax.bar(index[i]+(j-2)*(bar_width+0.05) , ira, bar_width, label=op, color=colors[j], edgecolor='black', linewidth=0.5, zorder=3)

        # Implicit ira
        if op != "CT":
            good = ira_tab[op]["imp"]["noTP"]["good"][j] + ira_tab[op]["imp"]["TP"]["good"][j]
            total = ira_tab[op]["imp"]["noTP"]["total"] + ira_tab[op]["imp"]["TP"]["total"]
            general_good[j] += good
            general_total[j] += total
        else:
            good = ira_tab[op]["imp"]["noTP"]["good"][j]
            total = ira_tab[op]["imp"]["noTP"]["total"]
            general_good[j] += good
            general_total[j] += total
        ira = good / total if total != 0 else 0
        ax.bar(index[i]+(j-2)*(bar_width+0.05) , ira, bar_width, color=colors[j], hatch='..', edgecolor='black', linewidth=0.5, zorder=3)

print(np.array(general_good) / np.array(general_total))

# Manual legend
ops = ["LP","MTL","MM","QP","CP"]
for i in range(5):
    label = "{"+",".join(ops[:i+1])+"}"
    patches.append(mpl.patches.Patch(facecolor=colors[i], edgecolor='black', linewidth=0.5, label=label))

lg = ax.legend(handles=patches, title="Set of OP classes", bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left', ncols=3, mode="expand", borderaxespad=0., fontsize=8, title_fontsize=8)
ax.add_artist(lg)

patches = []
patches.append(mpl.patches.Patch(facecolor='white', edgecolor='black', linewidth=0.5, label="Explicit"))
patches.append(mpl.patches.Patch(facecolor='white', edgecolor='black', linewidth=0.5, hatch='..', label="Implicit"))
ax.legend(handles=patches, loc='best', title="Difficulty",fontsize=8, title_fontsize=8)

ax.set_xticks(index,ira_tab.keys(), minor=False, fontsize=8)
ax.tick_params(axis='x', labelsize=8)
ax.tick_params(axis='y', labelsize=8)
ax.set_xlabel("Performance metric", fontsize=8)
ax.set_ylabel("IRA", fontsize=9)
plt.grid(color='gray', linewidth=0.5, zorder=0)
plt.subplots_adjust(top=0.75, bottom=0.15)
plt.show()