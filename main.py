import sys

import config
import parse
import optimizer

def green(row):
    return row.mw_drawn.solar + row.mw_drawn.hydro + row.mw_drawn.power + row.mw_drawn.biofuel

def judge(rows):
    green = sum(green(row) for row in rows)
    print(green)
    # price
    # co2


def main():
    (init, hours) = parse.parse_csv(open(sys.argv[1], 'r'))

    season = config.get_season(hours[0])
    nuclear = init[-1].mw_drawn.nuclear

    for hour in hours:
        print(hour.time)
        rate = config.consumer_rate(season, hour.time)
        print('Cost:')
        print(optimizer.optimize(hour, rate, nuclear, {'cost': -1, 'co2': 0, 'green': 0}, debug=False))
        print('Co2:')
        print(optimizer.optimize(hour, rate, nuclear, {'cost': 0, 'co2': -1, 'green': 0}, debug=False))
        print('Green:')
        print(optimizer.optimize(hour, rate, nuclear, {'cost': 0, 'co2': 0, 'green': 1}, debug=False))

if __name__ == '__main__':
    main()
