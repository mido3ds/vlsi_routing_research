#!/bin/env python3
'''
Analyse the summary.json out of merge_comp and random_comp. Read summary.json from stdin.
Requirements: python3.7, matplotlib
'''
import json
import sys
import math

import matplotlib.pyplot as plt
import numpy as np

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

plt.clf()
plt.title('W=H=45, different N (num of targets)')
for label, algo in algos.items():
    cond = algo['areas'] == 45
    plt.plot(
        algo['ns'][cond], algo['times'][cond],
        algo['color'],
        label=label
    )
    plt.xticks(list(set(algo['ns'][cond])))

plt.xlabel('Number of Targets')
plt.ylabel('Running Time (seconds)')
plt.legend()
plt.savefig('areaConst.png')

plt.clf()
plt.title('N=5, different W,H (where W=H)')
for label, algo in algos.items():
    cond = algo['areas'] != 45
    plt.plot(
        algo['areas'][cond], algo['times'][cond],
        algo['color'],
        label=label
    )
    plt.xticks(list(set(algo['areas'][cond])))

plt.xlabel('W or H')
plt.ylabel('Running Time (seconds)')
plt.legend()
plt.savefig('nConst.png')


def sort_x(x, y):
    return zip(*sorted(zip(x, y), key=lambda x: x[0]))
