import csv
import itertools

from collections import namedtuple

PowerRow = namedtuple('PowerRow', ['total', 'solar', 'nuclear', 'wind', 'hydro', 'gas', 'biofuel', 'buyable'])

class HourOut(namedtuple('HourOut', ['time', 'mw_drawn', 'mw_diff', 'mw_green', 'mw_bought', 'mw_sold', 'co2_out', 'price_selling', 'price_produce', 'price_diff'])):

    def to_row(self):
        # Outputs tuple of strings suitable for writing to csv
        return list(map(str, (
                2,
                str(self.time) + ':00'
               ) + self.mw_drawn + (
                self.mw_diff,
                self.mw_green,
                self.mw_bought,
                self.mw_sold,
                self.co2_out,
                self.price_selling,
                self.price_produce,
                self.price_diff,
                -1
               )))

HourIn = namedtuple('HourIn', ['time', 'mw_available', 'temps', 'solar_coef', 'wind_coef', 'hydro_coef', 'mw_sellable', 'mw_sellable_price', 'historical_drawn'])

def parse_time(time_string):
    # '18:00' -> 18
    return int(time_string.split(':')[0])

def parse_row(row):
    # row: [str]
    time = parse_time(row[1])
    mw = PowerRow(*map(float, row[2:10]))

    if row[0] in ['0', '2']:
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

    init_state = list(map(parse_row, itertools.islice(reader, 3)))
    hour_inputs = list(map(parse_row, [x for x in reader if x[0]]))

    return init_state, hour_inputs

