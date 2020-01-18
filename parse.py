import csv
import itertools

from collections import namedtuple

PowerRow = namedtuple('PowerRow', ['total', 'solar', 'nuclear', 'wind', 'hydro', 'gas', 'biofuel', 'buyable'])

HourOut = namedtuple('HourOut', ['time', 'mw_drawn', 'mw_diff', 'mw_green', 'mw_bought', 'mw_sold', 'co2_out', 'price_selling', 'price_produce', 'price_diff'])

HourIn = namedtuple('HourIn', ['time', 'mw_available', 'temps', 'solar_coef', 'wind_coef', 'hydro_coef', 'mw_sellable', 'mw_sellable_price', 'historical_drawn'])

def parse_time(time_string):
    # '18:00' -> 18
    return int(time_string.split(':')[0])

def parse_row(row):
    # row: [str]
    time = parse_time(row[1])
    mw = PowerRow(*map(float, row[2:10]))

    if row[0] == '0':
        args = ([time, mw] + list(map(float, row[10:row.index('-1')])))
        return HourOut(*args)
    elif row[0] == '1':
        temps = list(map(float, row[11:16]))
        historical_drawn = list(map(float, row[19:24]))
        args = [time, mw, temps] + list(map(float, row[15:20])) + [historical_drawn]
        return HourIn(*args)

def parse_csv(csv_file):
    # return ([HourOut]], [HourIn])

    reader = csv.reader(csv_file)

    init_state = list(itertools.islice(reader, 3))
    hour_inputs = list(map(parse_row, [x for x in reader if x[0]]))

    return init_state, hour_inputs

