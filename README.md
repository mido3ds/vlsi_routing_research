# VLSI Routing Research
"Exploring A* Search For Single and Multi Layer Routing."

VLSI research project which explores `A* with Euclidean Distance` in optimizing single/multi layer routing.

## Team #1

| Name                  | Section | B. N |
|-----------------------|---------|------|
| Evram Youssef         | 1       | 9    |
| Remonda Talaat        | 1       | 20   |
| Mahmoud Adas          | 2       | 21   |
| Mohamed Shawky        | 2       | 16   |

## Requirements

* For algorithms:
  + python 3.7+
  + python3-pip
  + numpy
* For plotting:
  + matplotlib
* For experiment running:
  + GNU bash 5.0.16
  + GNU time
  + jq 1.6+

``` sh
$ pip3 install --user numpy matplotlib
```

## Running Algorithms Implementations

Each algo in [ `mod_a_star.py` , `mikami_tabuchi.py` , `maze_lee.py` , `steiner_tree.py` ] takes its input from stdin and writes its output to stdout, so you need to either pipe or redirect stdin/stdout to deal with files.

You can also pipe the output of `gen-input.py` to any of them.

* `python3 mod_a_star.py <inputs/test1.json` 
* `python3 mikami_tabuchi.py <inputs/test1.json` 
* `python3 maze_lee.py <inputs/test1.json` 
* `python3 steiner_tree.py <inputs/test1.json` 

## Verify Outputs

Let `x,y` be the input and output json files respectively, to verify them:
`$ python3 verify.py x y` 

## Mikami Unit Tests

`$ python3 test_mikami_tabuchi.py` 

## Generating Random Input Files

`gen-input.py` has many options to control how you want to generate the input json file. It writes the generated output to stdout, so you may need to either pipe it or redirect it to a file.

``` sh
$ python3 gen-input.py --help
usage: gen-input.py [--help] [-w W] [-h H] [-v V] [-n N] [-d {1,2}]

Generate random input for the routers. See `io_schema.md` .
Requirements:

    - python3 3.8.2
    - python3-pip 20.0.2

    $ pip3 install --user numpy
For help: python gen-input.py --help
Example: python gen-input.py -d 2 -h 50,100 -w 100,10000 -n 100 -v 5 > inputs/test1.json

optional arguments:
  --help    show this help message and exit
  -w W      width, a number or a range "start,end"
  -h H      height, a number or a range "start,end"
  -v V      VIAs, a number or a range "start,end"
  -n N      destination cells, a number or a range "start,end"
  -d {1,2}  layers
```

## Random Test + Verification

1. Choose any algorithm file name, let it be `steiner_tree.py` .
2. Choose arguments to `gen-input.py` , let's say we want to limit w between 2, 10 and h between 10, 20 and the number of targets to be 5 exactly.
3. `$ ./random_test steiner_tree.py -w 2,10 -h 10,20 -n 5` 
4. input, output and err files are printed to stdout and exist in `datasets/steiner_tree.py/{in,out,err}` .
5. This script will run forever (unless an error ocurred) and verifies each out.

## Running Experiment Scripts

To conduct experiments over all algorithms, see `random_comp` :

``` sh
$ ./random_comp 
Usage: random_comp path/to/output/dir num_of_trials [ options to gen-inpu.py ]
$ ./random_comp datasets/10x10 100 -w10 -h10 # 100 trials of w=10, h=10 stored in datasets/10x10
...
...
```

To run the same experiments conducted in the paper, run:

``` sh
$ ./areaConst                       # vary n, while area is const
$ ./nConst                          # vary the area, while n is const
$ ./merge_comp                      # create summary.json, reruns missing tests
$ python3 plot.py <datasets/summary.json # dump plots in datasets/plot
```
