import numpy as np
import scipy.optimize as spo

import linear_programming as lp
import config
import parse

def optimize(inrow, rate, nuclear, value_func, debug=True):
    """
    Parameters:
        inrow:
            HourIn, containing current power demand, current power available
            from each source, projected future load, etc.

        rate:
            The cost charged to Ontario customers in cents/kWh, can change
            hourly.

        nuclear:
            Current amount of power supplied by nuclear.

        value_func: {'cost': float, 'green': float, 'co2': float}
            How to prioritize tradeoffs between lower costs, higher green
            production, and lower co2 emissions.

        debug:
            If true, logs the matrices passed to the linear optimizer.
    """

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

    poss = 0
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
        poss += inrow.mw_available.__getattribute__(s)
    if poss < needed:
        used = inrow.mw_available
        used = used._replace(nuclear=nuclear)
        used = used._replace(total=sum(used[1:]))
        return (used, 0)

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
    result2 = spo.linprog(-c, A, b)
    assert (abs(result[1] + result2.fun) < 1e-3)
    if debug:
        print(A)
        print(b)
        print(c)
        print(result)
    # Create PowerRow
    used = {key: result[0][i] for i, key in enumerate(['solar', 'wind', 'hydro', 'gas', 'biofuel', 'buyable'])}
    used['nuclear'] = nuclear
    used['total'] = inrow.mw_available.total
    return (parse.PowerRow(**used), result[0][-1])
