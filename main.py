import sys
import os
import csv

import config
import parse
import config
import optimizer

optimize_co2 = (os.environ.get('OPT_CO2', '1') != '0')

def gen_outrow(inrow, power_row, sold, rate):
    co2_out = sum(
        power_row.__getattribute__(s) * config.EMISSIONS[s] / 1000. for s in
            ['solar', 'wind', 'nuclear', 'hydro', 'gas', 'biofuel', 'buyable'])
    dollars = sum(
        power_row.__getattribute__(s) * config.PRICES[s] for s in
            ['solar', 'wind', 'nuclear', 'hydro', 'gas', 'biofuel', 'buyable']) - sold * inrow.mw_sellable_price * 1000
    price_selling = rate / 100
    price_produce = dollars / power_row.total / 1000
    return parse.HourOut(
        time=inrow.time,
        mw_drawn=power_row,
        mw_diff=power_row.total - inrow.mw_available.total,
        mw_green=power_row.solar + power_row.wind + power_row.hydro + power_row.biofuel,
        mw_bought=power_row.buyable,
        mw_sold=sold,
        co2_out=co2_out,
        price_selling=price_selling, # TODO PULL ADD CELINE'S THING
        price_produce=price_produce,
        price_diff=(price_selling-price_produce))

def print_summary(rows):
    # mean and max abs error
    green = sum(row.mw_green for row in rows)
    print('Produced {:,} green MW'.format(round(green, 2)))
    # TODO: wait, how to weight price?
    # price = sum(row.mw_green for row in rows)
    co2 = sum(row.co2_out for row in rows)
    print('Produced {:,} tonnes of CO2'.format(round(co2, 2)))
    # price diff * MW-hrs
    price = 1000 * sum(row.price_diff * row.mw_drawn.total for row in rows)
    print('Total weighted price-diff: {:,}'.format(round(price, 2)))
    # co2

def main():
    (init, hours) = parse.parse_csv(open(sys.argv[1], 'r'))
    writer = csv.writer(open(sys.argv[2], "w"))

    season = config.get_season(hours[0])
    nuclear = init[-1].mw_drawn.nuclear

    outrows = []
    print('Optimize: {}'.format(optimize_co2))
    for hour in hours:
        rate = config.consumer_rate(season, hour.time)
        power_row, sold = optimizer.optimize(hour, nuclear, {'cost': -1, 'co2': 0, 'green': 0}, debug=False)
        outrow = gen_outrow(hour, power_row, sold, rate)
        if outrow.price_diff > 0 and optimize_co2:
            # we broke even, optimize for low CO2 and high green usage
            power_row, sold = optimizer.optimize(hour, nuclear, {'cost': 0, 'co2': -1000, 'green': 1}, profit=0, rate=rate, debug=False)
            outrow = gen_outrow(hour, power_row, sold, rate)
        writer.writerow(outrow.to_row())
        outrows.append(outrow)

    print_summary(outrows)

if __name__ == '__main__':
    main()
