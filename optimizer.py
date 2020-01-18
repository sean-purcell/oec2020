import linear_programming as lp
import config

def optimize(inrow, nuclear, value_func, debug=True):
    ROWS = 10
    COLS = 6
    A = np.zeros((ROWS, COLS))
    b = np.zeros((ROWS))
    c = np.zeros((COLS))

    needed = inrow.mw_available.total - nuclear

    i = 0
    A[i] = np.ones((1, COLS))
    A[i][COLS-1] = -1
    b[i] = needed
    i += 1

    A[i] = -np.ones((1, COLS))
    b[i] = -needed
    i += 1

    for j, s in enumerate(['solar', 'nuclear', 'wind', 'hydro', 'gas', 'biofuel', 'buyable']):
        A[i][j] = 1
        b[i] = inrow.mw_available[s]
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

    if debug:
        print(A)
        print(b)
        print(c)

    result = lp.LPSolver(A, b, c).solve()
    print(result)
    return result
