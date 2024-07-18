import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import collections

plt.rcParams['text.usetex'] = True
plt.rc('font', family='sans-serif', size=40)

FIGPATH = f"./solution"
startx = 100
xdiff = 22
xstep = 50
barwidth = 20
# SOL_NAMES = ['GREEDY2', 'BNBSTARV7B', 'BNBSTARV7', 'ILP_GUROBI']
hatchs = ['/','.','o','']
x_ticks = [5, 10, 15, 20]

df2 = pd.read_csv(r"./testresult/testresult_per5.csv")

df2.head()

set_groups = df2.groupby(['slices']).groups
sol_groups = df2.groupby(['algosol']).groups

SET_NAMES = [5,10,15,20]
SOL_NAMES = ['GREEDY_SE','ILP_SE']

labels = ['CLC-SE', 'ILP-SE']

colors = ['black','goldenrod']
# Prep data
# Prep data
# Prep data
x = np.zeros((4,2))
y = np.zeros((4,2))
xticklocs = []
xxx = startx
jj = 0
for set_indx in SET_NAMES:
    jj = 0
    for sol_indx in SOL_NAMES:
        set_i = set_groups[set_indx].values
        sol_i = sol_groups[sol_indx].values
        iloc = SET_NAMES.index(set_indx)
        yloc = SOL_NAMES.index(sol_indx)
        i = [j for j in sol_i if j in set_i]
        # i = groups[indx].values[0]
        data = df2.loc[i]
        value = data['runtime'].values[0]
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
# Plot
plt.figure(figsize=(8,8), dpi=100)
plt.yscale('log')
plt.ylabel(r"Runtime (seconds)")
plt.xlabel(r"Number of slices")
# plt.figure()
plt.grid(color='lightgrey', linestyle='--', zorder=0)
# plt.ylim([0,1])
plt.xticks(xticklocs, labels=x_ticks)

for xi in range(len(x)):
    plt.bar(x[xi],y[xi], width=barwidth, hatch=hatchs[xi], label=labels[xi], edgecolor=colors[xi], fill=True, color='w', zorder=3)
# plt.bar(x,y, width=barwidth)
plt.ylim([10**-1,10**2])
#plt.legend()
plt.legend(loc="upper center", prop={'size':20}, framealpha=0)
plt.savefig(f"{FIGPATH}/runtime_cmp.pdf", bbox_inches='tight')
plt.show()