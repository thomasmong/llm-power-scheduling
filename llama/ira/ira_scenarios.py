# Comparison of IRA for the 3 scenarios
import os
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np

corres = {
    "CC": ["LP","QP","CP"],
    "CT": ["MTL"],
    "PP": ["MM"]
}

ira_tab_s1 = {
    "CC": None,
    "CT": None,
    "PP": None,
}
ira_tab_s2 = {
    "CC": None,
    "CT": None,
    "PP": None,
}
ira_tab_s3 = {
    "CC": None,
    "CT": None,
    "PP": None,
}

for op in ira_tab_s1.keys():
    ira_tab_s1[op] = {
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
    ira_tab_s2[op] = {
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
    ira_tab_s3[op] = {
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

for pb in corres.keys():
    for diff in ["imp", "exp"]:
        for tp in ["noTP","TP"]:
            num_requests = None

            # Nom du fichier
            filename = f"{pb}-{diff}-{tp}-ira-llama3-classifier-scenar1-3.txt"

            # Si fichier n'existe pas, ajouter une ligne avec ira=0
            if not os.path.exists(os.path.join('ira/scenar1', filename)):
                # S'il ne s'agit pas de MTL avec TP
                if (pb == "CT" and tp == "TP"):
                    ira_tab_s1[pb][diff][tp]["good"][0] = None
                else:
                    ira_tab_s1[pb][diff][tp]["good"][0] = 0
            else:
                # Lire le contenu du fichier
                with open(os.path.join('ira/scenar1', filename), 'r') as file:
                    content = file.readlines()
                
                # Count the number of requests
                num_requests = len(content) - 1

                # Count good classifications
                num_good = 0
                for line in content[:-1]:
                    line = line.strip()
                    if line in corres[pb]:
                        num_good += 1
                # Ajouter les données au DataFrame
                ira_tab_s1[pb][diff][tp]["good"][0] += num_good
            ira_tab_s1[pb][diff][tp]["total"] = num_requests

            # Nom du fichier
            filename = f"{pb}-{diff}-{tp}-ira-llama3-classifier-scenar2-3.txt"

            # Si fichier n'existe pas, ajouter une ligne avec ira=0
            if not os.path.exists(os.path.join('ira/scenar2', filename)):
                # S'il ne s'agit pas de MTL avec TP
                if (pb == "CT" and tp == "TP"):
                    ira_tab_s2[pb][diff][tp]["good"][0] = None
                else:
                    ira_tab_s2[pb][diff][tp]["good"][0] = 0
            else:
                # Lire le contenu du fichier
                with open(os.path.join('ira/scenar2', filename), 'r') as file:
                    content = file.readlines()
                
                # Count the number of requests
                num_requests = len(content) - 1

                # Count good classifications
                num_good = 0
                for line in content[:-1]:
                    line = line.strip()
                    if line in corres[pb]:
                        num_good += 1
                # Ajouter les données au DataFrame
                ira_tab_s2[pb][diff][tp]["good"][0] += num_good
            ira_tab_s2[pb][diff][tp]["total"] = num_requests

            # Nom du fichier
            filename = f"{pb}-{diff}-{tp}-ira-llama3-classifier-scenar3-3.txt"

            # Si fichier n'existe pas, ajouter une ligne avec ira=0
            if not os.path.exists(os.path.join('ira/scenar3', filename)):
                # S'il ne s'agit pas de MTL avec TP
                if (pb == "CT" and tp == "TP"):
                    ira_tab_s3[pb][diff][tp]["good"][0] = None
                else:
                    ira_tab_s3[pb][diff][tp]["good"][0] = 0
            else:
                # Lire le contenu du fichier
                with open(os.path.join('ira/scenar3', filename), 'r') as file:
                    content = file.readlines()
                
                # Count the number of requests
                num_requests = len(content) - 1

                # Count good classifications
                num_good = 0
                for line in content[:-1]:
                    line = line.strip()
                    if line in corres[pb]:
                        num_good += 1
                # Ajouter les données au DataFrame
                ira_tab_s3[pb][diff][tp]["good"][0] += num_good
            ira_tab_s3[pb][diff][tp]["total"] = num_requests
                        
## Plotting
# Define figure size
fig_width = 3.5  # single column width in inches
fig_height = 2.5  # height in inches
fig_size = (fig_width, fig_height)
# Bar chart
fig, ax = plt.subplots(figsize=fig_size)

index = np.arange(3)
gap = 0.05
bar_width = (1-gap) / 5
colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
mpl.rcParams['hatch.linewidth'] = 0.2

for i, op in enumerate(ira_tab_s1.keys()):
    if op != "CT":
        good_s1 = ira_tab_s1[op]["imp"]["noTP"]["good"][0] + ira_tab_s1[op]["imp"]["TP"]["good"][0] + ira_tab_s1[op]["exp"]["noTP"]["good"][0] + ira_tab_s1[op]["exp"]["TP"]["good"][0]
        total_s1 = ira_tab_s1[op]["imp"]["noTP"]["total"] + ira_tab_s1[op]["imp"]["TP"]["total"] + ira_tab_s1[op]["exp"]["noTP"]["total"] + ira_tab_s1[op]["exp"]["TP"]["total"]
        good_s2 = ira_tab_s2[op]["imp"]["noTP"]["good"][0] + ira_tab_s2[op]["imp"]["TP"]["good"][0] + ira_tab_s2[op]["exp"]["noTP"]["good"][0] + ira_tab_s2[op]["exp"]["TP"]["good"][0]
        total_s2 = ira_tab_s2[op]["imp"]["noTP"]["total"] + ira_tab_s2[op]["imp"]["TP"]["total"] + ira_tab_s2[op]["exp"]["noTP"]["total"] + ira_tab_s2[op]["exp"]["TP"]["total"]
        good_s3 = ira_tab_s3[op]["imp"]["noTP"]["good"][0] + ira_tab_s3[op]["imp"]["TP"]["good"][0] + ira_tab_s3[op]["exp"]["noTP"]["good"][0] + ira_tab_s3[op]["exp"]["TP"]["good"][0]
        total_s3 = ira_tab_s3[op]["imp"]["noTP"]["total"] + ira_tab_s3[op]["imp"]["TP"]["total"] + ira_tab_s3[op]["exp"]["noTP"]["total"] + ira_tab_s3[op]["exp"]["TP"]["total"]
    else:
        good_s1 = ira_tab_s1[op]["imp"]["noTP"]["good"][0] + ira_tab_s1[op]["exp"]["noTP"]["good"][0]
        total_s1 = ira_tab_s1[op]["imp"]["noTP"]["total"] + ira_tab_s1[op]["exp"]["noTP"]["total"]
        good_s2 = ira_tab_s2[op]["imp"]["noTP"]["good"][0] + ira_tab_s2[op]["exp"]["noTP"]["good"][0]
        total_s2 = ira_tab_s2[op]["imp"]["noTP"]["total"] + ira_tab_s2[op]["exp"]["noTP"]["total"]
        good_s3 = ira_tab_s3[op]["imp"]["noTP"]["good"][0] + ira_tab_s3[op]["exp"]["noTP"]["good"][0]
        total_s3 = ira_tab_s3[op]["imp"]["noTP"]["total"] + ira_tab_s3[op]["exp"]["noTP"]["total"]
        
    ira = good_s1 / total_s1 if total_s1 != 0 else 0
    ax.bar(index[i]-bar_width-gap, ira, bar_width, color=colors[0], edgecolor='black', linewidth=0.5, zorder=3)

    ira = good_s2 / total_s2 if total_s2 != 0 else 0
    ax.bar(index[i], ira, bar_width, color=colors[1], linewidth=0.5, edgecolor='black', zorder=3)
    
    ira = good_s3 / total_s3 if total_s3 != 0 else 0
    ax.bar(index[i]+bar_width+gap, ira, bar_width, color=colors[2], linewidth=0.5, edgecolor='black', zorder=3)

ax.legend(["Basic", "Contextualized", "Error-informed"], title="Prompting", title_fontsize=8, bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left', ncols=2, mode="expand", borderaxespad=0., fontsize=8)    

ax.set_xticks(index,ira_tab_s1.keys(), minor=False, fontsize=8)
ax.tick_params(axis='x', labelsize=8)
ax.tick_params(axis='y', labelsize=8)
ax.set_xlabel("Performance metric", fontsize=8)
ax.set_ylabel("IRA", fontsize=8)
plt.grid(color='gray', linewidth=0.5, zorder=0)
plt.subplots_adjust(right=0.7)
plt.tight_layout()
plt.show()