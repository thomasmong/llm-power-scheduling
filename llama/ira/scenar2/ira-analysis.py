import os
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np

# Chemin du dossier contenant les fichiers (dossier ira)
folder_path = os.path.join(os.getcwd(), 'ira/scenar2')


corres = {
    "CC": ["LP","QP","CP"],
    "CT": ["MTL"],
    "PP": ["MM"]
}

ira_tab = {
    "CC": None,
    "EI": None,
    "CT": None,
    "PP": None,
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
            num_requests = None

            # Nom du fichier
            filename = f"{pb}-{diff}-{tp}-ira-llama3-classifier-scenar2-3.txt"

            # Si fichier n'existe pas, ajouter une ligne avec ira=0
            if not os.path.exists(os.path.join(folder_path, filename)):
                # S'il ne s'agit pas de MTL avec TP
                if (pb == "CT" and tp == "TP"):
                    ira_tab[pb][diff][tp]["good"][0] = None
                else:
                    ira_tab[pb][diff][tp]["good"][0] = 0
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
                ira_tab[pb][diff][tp]["good"][0] += num_good
            ira_tab[pb][diff][tp]["total"] = num_requests

# Print total time
print(total_time)

## Plotting
# Define figure size
fig_width = 3.5  # single column width in inches
fig_height = 2.5  # height in inches
fig_size = (fig_width, fig_height)
# Bar chart
fig, ax = plt.subplots(figsize=fig_size)

index = np.arange(4)
gap = 0.3
bar_width = (1-gap) / 5

colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
mpl.rcParams['hatch.linewidth'] = 0.2

patches = []

for i, op in enumerate(ira_tab.keys()):
    if op != "PP":
        diff = ["exp","imp"]
        for dif in diff:
            if op != "CT":
                good = ira_tab[op][dif]["noTP"]["good"][0] + ira_tab[op][dif]["TP"]["good"][0]
                total = ira_tab[op][dif]["noTP"]["total"] + ira_tab[op][dif]["TP"]["total"]
            else:
                good = ira_tab[op][dif]["noTP"]["good"][0]
                total = ira_tab[op][dif]["noTP"]["total"]
            ira = good / total if total != 0 else 0
            ax.bar(index[i], ira, bar_width, color=colors[0], hatch='oo' if dif=="imp" else None, edgecolor='black', linewidth=0.5)
    else:
        diff = ["imp","exp"]
        for dif in diff:
            good = ira_tab[op][dif]["noTP"]["good"][0] + ira_tab[op][dif]["TP"]["good"][0]
            total = ira_tab[op][dif]["noTP"]["total"] + ira_tab[op][dif]["TP"]["total"]
            ira = good / total if total != 0 else 0
            ax.bar(index[i], ira, bar_width, color=colors[0], hatch='oo' if dif=="imp" else None, edgecolor='black', linewidth=0.5)

# Manual legend
patches = []
patches.append(mpl.patches.Patch(facecolor='white', edgecolor='black', linewidth=0.5, label="Explicit"))
patches.append(mpl.patches.Patch(facecolor='white', edgecolor='black', linewidth=0.5, hatch='oo', label="Implicit"))
ax.legend(handles=patches, loc='upper right',fontsize=8, title_fontsize=9)

ax.set_xticks(index,ira_tab.keys(), minor=False, fontsize=8)
ax.set_xlabel("Performance metric", fontsize=9)
ax.set_ylabel("IRA", fontsize=9)
plt.subplots_adjust(right=0.7)
plt.tight_layout()
plt.show()