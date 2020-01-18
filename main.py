import sys

import parse
import optimizer

def main():
    (init, hours) = parse.parse_csv(open(sys.argv[1], 'r'))

    nuclear = init[-1].mw_drawn.nuclear

    print('Cost:')
    optimizer.optimize(hours[0], nuclear, {'cost': -1, 'co2': 0, 'green': 0})
    print('Co2:')
    optimizer.optimize(hours[0], nuclear, {'cost': 0, 'co2': -1, 'green': 0})
    print('Green:')
    optimizer.optimize(hours[0], nuclear, {'cost': 0, 'co2': 0, 'green': 1})

if __name__ == '__main__':
    main()
