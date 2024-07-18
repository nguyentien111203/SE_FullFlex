import numpy as np
import pandas as pd
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import matplotlib as mpl


df4 = pd.read_csv(r"./testresult/testresult_per5_40.csv")

df4.head()

plt.rcParams['text.usetex'] = True
plt.rc('font', family='sans-serif', size=40)

FIGPATH = f"./solution"

# COMMON SETTINGS
startx = 100
xdiff = 22
xstep = 50
barwidth = 20
# SOL_NAMES = ['GREEDY2', 'BNBSTARV7B', 'BNBSTARV7', 'ILP_GUROBI']
hatchs = ['/','/','.','.']
set_groups = df4.groupby(['slices']).groups
conf_groups = df4.groupby(['algoconfig']).groups

labels = [r'CLC-SE,$k_1$',r'CLC-SE,$k_2$',r'ILP-SE,$k_1$',r'ILP-SE,$k_2$']
x_ticks = [5,10,15,20]

colors = ['black','black','goldenrod','goldenrod']

CONFIG_NAMES = ['GREEDY_SE_k1','GREEDY_SE_k2','ILP_SE_k1','ILP_SE_k2']
SET_NAMES = [5,10,15,20]

# PLOT ACCRate greedy vs ilp

# Prep data
x = np.zeros((4,4))
y = np.zeros((4,4))
xticklocs = []
xxx = startx
jj = 0
for set_indx in SET_NAMES:
    jj = 0
    for sol_indx in CONFIG_NAMES:
        set_i = set_groups[set_indx].values
        sol_i = conf_groups[sol_indx].values
        iloc = SET_NAMES.index(set_indx)
        yloc = CONFIG_NAMES.index(sol_indx)
        i = [j for j in sol_i if j in set_i]
        # i = groups[indx].values[0]
        data = df4.loc[i]
        value = data['accrate'].values[0]
        x[iloc][yloc] = xxx
        y[iloc][yloc] = value
        # print(set_indx, sol_indx)
        xxx += xdiff
        jj += 1
    xxx += xstep
    jj -= 1
    xticklocs.append(np.average(x[SET_NAMES.index(set_indx)]))
x = x.transpose()
y = y.transpose()

plt.figure(figsize=(8,8), dpi=100)
plt.yscale('linear')
plt.ylabel(r"Acceptance rate")
plt.xlabel(r"Number of slices")
# plt.figure()
plt.grid(color='lightgrey', linestyle='--', zorder=0)
# plt.ylim([0,1])
plt.xticks(xticklocs, labels=x_ticks)


plt.bar(x[1],y[0], width=barwidth, hatch=hatchs[0], label=labels[0], edgecolor=colors[0], fill=True, color='grey', zorder=3)
plt.bar(x[1],y[1], width=barwidth, hatch=hatchs[1], label=labels[1], edgecolor=colors[1], fill=True, color='w', zorder=3, bottom=y[0])
plt.bar(x[2],y[2], width=barwidth, hatch=hatchs[2], label=labels[2], edgecolor=colors[2], fill=True, color='yellow', zorder=3)
plt.bar(x[2],y[3], width=barwidth, hatch=hatchs[3], label=labels[3], edgecolor=colors[3], fill=True, color='w', zorder=3, bottom=y[2])
# plt.bar(x,y, width=barwidth)
plt.ylim([0,1.02])
plt.plot(stacked = True)
#plt.legend()
plt.legend(loc="upper center", prop={'size':20}, framealpha=0)
plt.savefig(f"{FIGPATH}/accrate_eachconf_cmp.pdf", bbox_inches='tight')
plt.show()