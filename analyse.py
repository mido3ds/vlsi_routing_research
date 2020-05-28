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
        'targets': np.array(list(map(lambda x: x['total_targets'] / x['n'] * 100, subset))),
        'color': color
    }

areas = sorted(list(set(algos['mikami_tabuchi.py']['areas'])))
areas.remove(45)

ns = sorted(list(set(algos['mikami_tabuchi.py']['ns'])))
ns.remove(5)

###########

plt.clf()
plt.subplots_adjust(
    top=0.91,
    bottom=0.095,
    left=0.09,
    right=0.93,
    hspace=0.215,
    wspace=0.155
)

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
plt.grid()
plt.savefig('tmp/analyse/areaConst.png')

plt.clf()
plt.subplots_adjust(
    top=0.91,
    bottom=0.095,
    left=0.09,
    right=0.93,
    hspace=0.215,
    wspace=0.155
)

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
plt.grid()
plt.savefig('tmp/analyse/nConst.png')

###########

plt.clf()
plt.subplots_adjust(
    top=0.91,
    bottom=0.095,
    left=0.09,
    right=0.93,
    hspace=0.215,
    wspace=0.155
)

plt.title('Median Running Time vs. Grid Width, #Targets=5')
for label, algo in algos.items():
    times_median = [np.median(algo['times'][algo['areas'] == area])
                    for area in areas]

    plt.plot(
        areas, times_median,
        label=label,
        linewidth=(2 if label == 'mod_a_star.py' else 1),
        marker=('o' if label == 'mod_a_star.py' else None)
    )

plt.xticks(areas)
plt.xlabel('Grid Width')
plt.ylabel('Median Running Time (seconds)')
plt.legend()
plt.grid()
plt.savefig('tmp/analyse/medianTime_nConst.png')

plt.clf()
plt.subplots_adjust(
    top=0.91,
    bottom=0.095,
    left=0.09,
    right=0.93,
    hspace=0.215,
    wspace=0.155
)

plt.title('Median Running Time vs. #Targets, Width=45')
for label, algo in algos.items():
    non_inf = algo['times'][algo['times'] != math.inf]
    non_inf_ns = algo['ns'][algo['times'] != math.inf]
    times_median = [np.median(non_inf[non_inf_ns == n]) for n in ns]

    plt.plot(
        ns, times_median,
        label=label,
        linewidth=(2 if label == 'mod_a_star.py' else 1),
        marker=('o' if label == 'mod_a_star.py' else None)
    )

plt.xticks(ns)
plt.xlabel('#Targets')
plt.ylabel('Median Running Time (seconds)')
plt.legend()
plt.grid()
plt.savefig('tmp/analyse/medianTime_areaConst.png')

#########

plt.clf()
plt.subplots_adjust(
    top=0.91,
    bottom=0.095,
    left=0.09,
    right=0.93,
    hspace=0.215,
    wspace=0.155
)

plt.title('Max Path Cost vs. Grid Width, #Targets=5')
for label, algo in algos.items():
    costs_max = [np.max(algo['costs'][algo['areas'] == area])
                 for area in areas]

    plt.plot(
        areas, costs_max,
        label=label,
        linewidth=(2 if label == 'mod_a_star.py' else 1),
        marker=('o' if label == 'mod_a_star.py' else None)
    )

plt.xticks(areas)
plt.xlabel('Grid Width')
plt.ylabel('Max Path Cost')
plt.legend()
plt.grid()
plt.savefig('tmp/analyse/maxCost_nConst.png')

plt.clf()
plt.subplots_adjust(
    top=0.91,
    bottom=0.095,
    left=0.09,
    right=0.93,
    hspace=0.215,
    wspace=0.155
)

plt.title('Max Path Cost vs. #Targets, Width=45')
for label, algo in algos.items():
    costs_max = [np.max(algo['costs'][algo['ns'] == n])
                 for n in ns]

    plt.plot(
        ns, costs_max,
        label=label,
        linewidth=(2 if label == 'mod_a_star.py' else 1),
        marker=('o' if label == 'mod_a_star.py' else None)
    )

plt.xticks(ns)
plt.xlabel('#Targets')
plt.ylabel('Max Path Cost')
plt.legend()
plt.grid()
plt.savefig('tmp/analyse/maxCost_areaConst.png')

#########
plt.clf()
plt.subplots_adjust(
    top=0.91,
    bottom=0.095,
    left=0.09,
    right=0.93,
    hspace=0.215,
    wspace=0.155
)

plt.title('Avg Path Cost vs. Grid Width, #Targets=5')
for label, algo in algos.items():
    costs_avg = [np.average(algo['costs'][algo['areas'] == area])
                 for area in areas]

    plt.plot(
        areas, costs_avg,
        label=label,
        linewidth=(2 if label == 'mod_a_star.py' else 1),
        marker=('o' if label == 'mod_a_star.py' else None)
    )

plt.xticks(areas)
plt.xlabel('Grid Width')
plt.ylabel('Avg Path Cost')
plt.legend()
plt.grid()
plt.savefig('tmp/analyse/avgCost_nConst.png')

plt.clf()
plt.subplots_adjust(
    top=0.91,
    bottom=0.095,
    left=0.09,
    right=0.93,
    hspace=0.215,
    wspace=0.155
)

plt.title('Avg Path Cost vs. #Targets, Width=45')
for label, algo in algos.items():
    costs_avg = [np.average(algo['costs'][algo['ns'] == n])
                 for n in ns]

    plt.plot(
        ns, costs_avg,
        label=label,
        linewidth=(2 if label == 'mod_a_star.py' else 1),
        marker=('o' if label == 'mod_a_star.py' else None)
    )

plt.xticks(ns)
plt.xlabel('#Targets')
plt.ylabel('Avg Path Cost')
plt.legend()
plt.grid()
plt.savefig('tmp/analyse/avgCost_areaConst.png')

#########
plt.clf()
plt.subplots_adjust(
    top=0.91,
    bottom=0.095,
    left=0.09,
    right=0.93,
    hspace=0.215,
    wspace=0.155
)

plt.title('Total Path Cost vs. Grid Width, #Targets=5')
for label, algo in algos.items():
    costs_total = [np.sum(algo['costs'][algo['areas'] == area])
                   for area in areas]

    plt.plot(
        areas, costs_total,
        label=label,
        linewidth=(2 if label == 'mod_a_star.py' else 1),
        marker=('o' if label == 'mod_a_star.py' else None)
    )

plt.xticks(areas)
plt.xlabel('Grid Width')
plt.ylabel('Total Path Cost')
plt.legend()
plt.grid()
plt.savefig('tmp/analyse/totalCost_nConst.png')

plt.clf()
plt.subplots_adjust(
    top=0.91,
    bottom=0.095,
    left=0.09,
    right=0.93,
    hspace=0.215,
    wspace=0.155
)

plt.title('Total Path Cost vs. #Targets, Width=45')
for label, algo in algos.items():
    costs_total = [np.sum(algo['costs'][algo['ns'] == n])
                   for n in ns]

    plt.plot(
        ns, costs_total,
        label=label,
        linewidth=(2 if label == 'mod_a_star.py' else 1),
        marker=('o' if label == 'mod_a_star.py' else None)
    )

plt.xticks(ns)
plt.xlabel('#Targets')
plt.ylabel('Total Path Cost')
plt.legend()
plt.grid()
plt.savefig('tmp/analyse/totalCost_areaConst.png')

#########
plt.clf()
plt.subplots_adjust(
    top=0.91,
    bottom=0.095,
    left=0.09,
    right=0.93,
    hspace=0.215,
    wspace=0.155
)

plt.title('% Reached Targets vs. Grid Width, #Targets=5')
for label, algo in algos.items():
    plt.plot(
        areas, [np.sum(algo['targets'][algo['areas'] == area])
                for area in areas],
        label=label,
        linewidth=(2 if label == 'mod_a_star.py' else 1),
        marker=('o' if label == 'mod_a_star.py' else None)
    )

plt.xticks(areas)
plt.xlabel('Grid Width')
plt.ylabel('% Reached Targets')
plt.legend()
plt.grid()
plt.savefig('tmp/analyse/percTargets_nConst.png')

plt.clf()
plt.subplots_adjust(
    top=0.91,
    bottom=0.095,
    left=0.09,
    right=0.93,
    hspace=0.215,
    wspace=0.155
)

plt.title('% Reached Targets vs. #Targets, Width=45')
for label, algo in algos.items():
    plt.plot(
        ns, [np.sum(algo['targets'][algo['ns'] == n])
             for n in ns],
        label=label,
        linewidth=(2 if label == 'mod_a_star.py' else 1),
        marker=('o' if label == 'mod_a_star.py' else None)
    )

plt.xticks(ns)
plt.xlabel('#Targets')
plt.ylabel('% Reached Targets')
plt.legend()
plt.grid()
plt.savefig('tmp/analyse/percTargets_areaConst.png')

#########
plt.clf()
plt.subplots_adjust(
    top=0.91,
    bottom=0.095,
    left=0.09,
    right=0.93,
    hspace=0.215,
    wspace=0.155
)

plt.title('# Timeouts vs. Grid Width, #Targets=5')
for label, algo in algos.items():
    y = [(algo['times'][algo['areas'] == area] == math.inf).sum()
         for area in areas]
    if len(y) == 0:
        break
    plt.plot(
        areas, y,
        label=label,
        linewidth=(2 if label == 'mod_a_star.py' else 1),
        marker=('o' if label == 'mod_a_star.py' else '^' if label ==
                'steiner_tree.py' else None)
    )

plt.xticks(areas)
plt.xlabel('Grid Width')
plt.ylabel('# Timeouts')
plt.legend()
plt.grid()
plt.savefig('tmp/analyse/timeouts_nConst.png')

plt.clf()
plt.subplots_adjust(
    top=0.91,
    bottom=0.095,
    left=0.09,
    right=0.93,
    hspace=0.215,
    wspace=0.155
)

plt.title('# Timeouts vs. #Targets, Width=45')
for label, algo in algos.items():
    y = [(algo['times'][algo['ns'] == n] == math.inf).sum()
         for n in ns]
    if len(y) == 0:
        break
    plt.plot(
        ns, y,
        label=label,
        linewidth=(2 if label == 'mod_a_star.py' else 1),
        marker=('o' if label == 'mod_a_star.py' else '^' if label ==
                'steiner_tree.py' else None)
    )

plt.xticks(ns)
plt.xlabel('#Targets')
plt.ylabel('# Timeouts')
plt.legend()
plt.grid()
plt.savefig('tmp/analyse/timeouts_areaConst.png')
