#!/bin/bash
'''
Add final path data to output.json file.

Usage: python3 calc_total.py </path/to/output.json >/path/to/newoutput.json 
'''
import json
import sys

inp = json.load(sys.stdin)

assert 'path_coor' in inp, 'no path_coor'

if 'final_path_cost' not in inp:
    s = set()
    for path in inp['path_coor']:
        for p in path:
            s.add((p[0], p[1], p[2]))

    inp['final_path_exist'] = len(s) != 0
    inp['final_path_cost'] = len(s)
    inp['final_path'] = list(s)

json.dump(inp, sys.stdout)
