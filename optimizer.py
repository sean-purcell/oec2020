import numpy as np
import scipy.optimize as spo

import linear_programming as lp
import config

# rate: cost charged to Ontario consumers in cents/kWh, can change hourly
def optimize(inrow, rate, nuclear, value_func, debug=True):
    ROWS = 16
    COLS = 7
    A = np.zeros((ROWS, COLS))
    b = np.zeros((ROWS))
    c = np.zeros((COLS))

    needed = inrow.mw_available.total - nuclear

    i = 0
    A[i] = np.ones((1, COLS))
    A[i][COLS-1] = -1
    b[i] = needed * 1.025
    i += 1

    A[i] = -A[i-1]
    b[i] = -needed
    i += 1

    for j, s in enumerate(['solar', 'wind', 'hydro', 'gas', 'biofuel', 'buyable']):
        A[i][j] = 1
        b[i] = inrow.mw_available.__getattribute__(s)
        i += 1
        A[i][j] = -1
        b[i] = 0
        i += 1

        c[j] = value_func['co2'] * config.EMISSIONS[s] + value_func['cost'] * config.PRICES[s]
        if s in ['hydro', 'wind', 'solar', 'biofuel']:
            c[j] += value_func['green']

    A[i][COLS-1] = 1
    b[i] = inrow.mw_sellable
    i += 1
    A[i][COLS-1] = -1
    b[i] = 0
    i += 1
    c[COLS-1] = value_func['cost'] * inrow.mw_sellable_price * -1000

    if debug:
        print(A)
        print(b)
        print(c)

    result = lp.LPSolver(A, b, c).solve()
    # result2 = spo.linprog(-c, A, b)
    if debug:
        print(A)
        print(b)
        print(c)
        print(result)
    return result
