import numpy as np

EPS = 1e-8
inf = float('inf')


class LPSolver(object):
    def __init__(self, A, b, c):
        self.m = len(b)
        self.n = len(c)
        m = self.m
        n = self.n

        self.N = np.zeros((self.n + 1), np.int32)
        self.B = np.zeros((self.m), np.int32)
        self.D = np.zeros((self.m + 2, self.n + 2))

        for i in range(m):
            for j in range(n):
                self.D[i][j] = A[i][j]
        for i in range(m):
            self.B[i] = n + i
            self.D[i][n] = -1
            self.D[i][n+1] = b[i]
        for i in range(n):
            self.N[j] = j
            self.D[m][j] = -c[j]
        self.N[n] = -1
        self.D[m+1][n] = 1

    def ltj(self, X, s, j):
        if s == -1 or (X[j], self.N[j]) < (X[s], self.N[s]):
            return j
        else:
            return s

    def pivot(self, r, s):
        D = self.D
        N = self.N
        B = self.B
        a = self.D[r]
        inv = 1 / a[s]

        for i in range(self.m+2):
            if i != r and abs(self.D[i][s]) > EPS:
                b = D[i]
                inv2 = b[s] * inv
                for j in range(self.n+2):
                    b[j] -= a[j] * inv2
                b[s] = a[s] * inv2
        for j in range(self.n+2):
            if j != s:
                D[r][j] *= inv
        for i in range(self.m+2):
            if i != r:
                D[i][s] *= -inv
        D[r][s] = inv
        B[r], N[s] = N[s], B[r]

    def simplex(self, phase):
        x = self.m + phase - 1
        N = self.N
        D = self.D
        B = self.B
        n = self.n
        m = self.m
        while True:
            s = -1
            for j in range(self.n+1):
                if N[j] != -phase:
                    s = self.ltj(D[x],s,j)
            if D[x][s] >= -EPS:
                return True
            r = -1
            for i in range(m):
                if D[i][s] <= EPS:
                    continue
                if r == -1 or (D[i][n+1] / D[i][s], B[i]) < (D[r][n+1] / D[r][s], B[r]):
                    r = i
            if r == -1:
                return False
            self.pivot(r, s)

    def solve(self):
        N = self.N
        D = self.D
        B = self.B
        n = self.n
        m = self.m
        r = 0
        for i in range(1, m):
            if D[i][n+1] < D[r][n+1]:
                r = i
        if D[r][n+1] < -EPS:
            self.pivot(r, n)
            if (not self.simplex(2)) or (D[m+1][n+1] < -EPS):
                return inf
            for i in range(m):
                if B[i] == -1:
                    s = 0
                    for j in range(1, n+1):
                        s = self.ltj(D[i], s, j)
                    self.pivot(i, s)
        ok = self.simplex(1)
        x = np.zeros((n))
        for i in range(m):
            if B[i] < n:
                x[B[i]] = D[i][n+1]
        return (x, D[m][n+1] if ok else inf)

if __name__ == '__main__':
    A = np.array([[50, 24], [30, 33], [-1, 0], [-1, 0]])
    b = np.array([2400, 2100, -45, -5])
    c = np.array([1, 1])
    print(LPSolver(A, b, c).solve())
