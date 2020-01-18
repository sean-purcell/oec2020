import sys
import os
import csv

import config
import parse
import config
import optimizer

optimize_co2 = (os.environ.get('OPT_CO2', '1') != '0')

def clamp(value, minvalue, maxvalue):
    return max(minvalue, min(value, maxvalue))

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

    # Check for blackouts
    def did_blackout(outrow):
        return outrow.mw_diff < 0

    n_blackouts = sum(map(did_blackout, rows))
    print('Blackouts: {}'.format(n_blackouts))

def main():
    (init, hours) = parse.parse_csv(open(sys.argv[1], 'r'))
    writer = csv.writer(open(sys.argv[2], "w"))

    season = config.get_season(hours[0])
    nuclear = init[-1].mw_drawn.nuclear

    def target_nuclear(inrow):
        # This is a control system to decide how much nuclear power we want.

        # Using the provided numbers, hydro is optimal.
        # But nuclear is second-best, and nuclear power supply is inelastic.
        # So we want to use lots of nuclear, but only after we use as much
        # hydro as possible.

        # If we're using 80% as much power this week, adjust estimates down.
        adjust_factor = max(1, inrow.mw_available.total / inrow.historical_drawn[0])
        predicted_drawn = [drawn * adjust_factor for drawn in inrow.historical_drawn]
        avg_draw = sum(predicted_drawn)/len(predicted_drawn)

        # Hydro appears to be pretty stable.
        predicted_needed = max(0, avg_draw - inrow.mw_available.hydro)

        print('Aiming for {} nuclear power'.format(predicted_needed))
        return predicted_needed

    outrows = []
    print('Optimize: {}'.format(optimize_co2))
    for hour in hours:
        rate = config.consumer_rate(season, hour.time)
        nuclear = clamp(target_nuclear(hour), nuclear * 0.99, nuclear*1.01)
        power_row, sold = optimizer.optimize(hour, nuclear, {'cost': -1, 'co2': -2, 'green': 0}, debug=False)
        outrow = gen_outrow(hour, power_row, sold, rate)
        outrows.append(outrow)

    print_summary(outrows)

if __name__ == '__main__':
    main()
