#!/bin/env python3
'''
Analyse the summary.json out of merge_comp and random_comp. Read summary.json from stdin.
Requirements: python3.7, matplotlib
'''
import json
import sys
import math

# from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from matplotlib.ticker import FormatStrFormatter, LinearLocator

inp = json.load(sys.stdin)

for algo, color in (('mikami_tabuchi.py', '.'), ('mod_a_star.py', '^'), ('steiner_tree.py', '.')):#, ('maze_lee.py', 'o')):
    subset = list(filter(lambda x: x['algo'] == algo, inp))
    areas = np.array(list(map(lambda x: x['w'], subset)))
    ns = np.array(list(map(lambda x: x['n'], subset)))
    times = np.array(
        list(map(lambda x: x['time'] if type(x['time']) != str else math.inf, subset)))
    ds = np.array(list(map(lambda x: x['d'], subset)))

    plt.plot(
        ns, times,
        color,
        label=algo
    )
    # plt.xticks(list(set(ns)))

    plt.xlabel('Width and Height')
    plt.ylabel('Running Time (seconds)')

plt.legend()
plt.show()
