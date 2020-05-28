#!/bin/env python3
'''
Analyse the summary.json out of merge_comp and random_comp. Read summary.json from stdin.
Requirements: python3.7, matplotlib
'''
import json
import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

Path("tmp/analyse").mkdir(parents=True, exist_ok=True)
inp = json.load(sys.stdin)

algos = {}
for algo, color in (('mikami_tabuchi.py', '.'), ('mod_a_star.py', '.'), ('steiner_tree.py', '.'), ('maze_lee.py', '.')):
    subset = list(filter(lambda x: x['algo'] == algo, inp))

    algos[algo] = {
        'areas': np.array(list(map(lambda x: x['w'], subset))),
        'ns': np.array(list(map(lambda x: x['n'], subset))),
        'times': np.array(
            list(
                map(lambda x: x['time'] if type(x['time']) != str
                    else math.inf, subset)
            )
        ),
        'costs': np.array(list(map(lambda x: x['total_cost'], subset))),
        'targets': np.array(list(map(lambda x: x['total_targets'], subset))),
        'color': color
    }

areas = sorted(list(set(algos['mikami_tabuchi.py']['areas'])))
areas.remove(45)

ns = sorted(list(set(algos['mikami_tabuchi.py']['ns'])))
ns.remove(5)

###########

plt.clf()
plt.title('Running Time vs. #Targets, Width=45')
for label, algo in algos.items():
    cond = algo['areas'] == 45
    plt.plot(
        algo['ns'][cond], algo['times'][cond],
        algo['color'],
        label=label
    )
    plt.xticks(list(set(algo['ns'][cond])))

plt.xlabel('#Targets')
plt.ylabel('Running Time (seconds)')
plt.legend()
plt.savefig('tmp/analyse/areaConst.png')

plt.clf()
plt.title('Running Time vs. Grid Width, #Targets=5')
for label, algo in algos.items():
    cond = algo['areas'] != 45
    plt.plot(
        algo['areas'][cond], algo['times'][cond],
        algo['color'],
        label=label
    )
    plt.xticks(list(set(algo['areas'][cond])))

plt.xlabel('Grid Width')
plt.ylabel('Running Time (seconds)')
plt.legend()
plt.savefig('tmp/analyse/nConst.png')

###########

plt.close()
plt.figure(figsize=(14, 6))
plt.subplots_adjust(
    top=0.905,
    bottom=0.095,
    left=0.08,
    right=0.925,
    hspace=0.215,
    wspace=0.155
)

plt.subplot(1, 2, 1)
plt.title('Median Running Time vs. Grid Width, #Targets=5')
for label, algo in algos.items():
    times_median = [np.median(algo['times'][algo['areas'] == area])
                    for area in areas]

    plt.plot(
        areas, times_median,
        label=label
    )

plt.xticks(areas)
plt.xlabel('Grid Width')
plt.ylabel('Median Running Time (seconds)')
plt.legend()

plt.subplot(1, 2, 2)
plt.title('Median Running Time vs. #Targets, Width=45')
for label, algo in algos.items():
    times_median = [np.median(algo['times'][algo['areas'] == area])
                    for area in areas]

    plt.plot(
        ns, times_median,
        label=label
    )

plt.xticks(ns)
plt.xlabel('#Targets')
plt.ylabel('Median Running Time (seconds)')
plt.legend()

plt.savefig('tmp/analyse/median.png')
plt.show()
