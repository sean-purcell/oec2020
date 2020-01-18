import sys

import parse
import optimizer

def main():
    (init, hours) = parse.parse_csv(open(sys.argv[1], 'r'))

    nuclear = init[-1].mw_drawn.nuclear

    for hour in hours:
        print(hour.time)
        print('Cost:')
        print(optimizer.optimize(hour, nuclear, {'cost': -1, 'co2': 0, 'green': 0}, debug=False))
        print('Co2:')
        print(optimizer.optimize(hour, nuclear, {'cost': 0, 'co2': -1, 'green': 0}, debug=False))
        print('Green:')
        print(optimizer.optimize(hour, nuclear, {'cost': 0, 'co2': 0, 'green': 1}, debug=False))

if __name__ == '__main__':
    main()
