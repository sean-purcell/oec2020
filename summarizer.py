# Tools for analyzing a historical dataset

import parse

FILES = ['data/inputFile1.csv', 'data/inputFile2.csv', 'data/inputFile3.csv']

def print_summary_stats(name, l):
    print(name, 'max:', max(l), 'min:', min(l), 'avg:', sum(l)/len(l))

def summarize(filename):
    orig, parsed = list(parse.parse_csv(filename))
    hydro = list(row.mw_available.hydro for row in parsed)
    needed = list(row.mw_available.total for row in parsed)
    # amount of additional power needed to generate
    shortfall = list(n-h for n, h in zip (needed, hydro))
    print_summary_stats('needed power', needed)
    print_summary_stats('hydro', hydro)
    print_summary_stats('hydro shortfall', shortfall)
    #for h, n in zip(hydro, needed):
    #    print(h, n, h-n)

for name in FILES:
    summarize(name)
