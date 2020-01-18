import sys
import csv

import parse
import config
import optimizer

def gen_outrow(inrow, power_row, sold):
    co2_out = sum(
        power_row.__getattribute__(s) * config.EMISSIONS[s] / 1000. for s in
            ['solar', 'wind', 'nuclear', 'hydro', 'gas', 'biofuel', 'buyable'])
    dollars = sum(
        power_row.__getattribute__(s) * config.PRICES[s] for s in
            ['solar', 'wind', 'nuclear', 'hydro', 'gas', 'biofuel', 'buyable']) - sold * inrow.mw_sellable_price * 1000
    price_selling = 0
    price_produce = dollars / power_row.total / 1000
    return parse.HourOut(
        time=inrow.time,
        mw_drawn=power_row,
        mw_diff=power_row.total - inrow.mw_available.total,
        mw_green=power_row.solar + power_row.wind + power_row.hydro + power_row.biofuel,
        mw_bought=power_row.buyable,
        mw_sold=sold,
        co2_out=co2_out,
        price_selling=0, # TODO PULL ADD CELINE'S THING
        price_produce=price_produce,
        price_diff=(price_selling-price_produce))

def main():
    (init, hours) = parse.parse_csv(open(sys.argv[1], 'r'))
    writer = csv.writer(sys.stdout)

    nuclear = init[-1].mw_drawn.nuclear

    value_func = {
        'cost': float(sys.argv[2]),
        'co2': float(sys.argv[3]),
        'green': float(sys.argv[4]),
    }

    for hour in hours:
        power_row, sold = optimizer.optimize(hour, nuclear, value_func, debug=False)
        outrow = gen_outrow(hour, power_row, sold)
        writer.writerow(outrow.to_row())

if __name__ == '__main__':
    main()
