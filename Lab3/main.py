import numpy as np
import pandas as pd
import random
from collections import Counter


def calculate(matrix):
    Is = []
    Js = []
    V = []
    i = random.randrange(len(matrix))
    j = random.randrange(len(matrix))
    ils = [i, matrix[i]]
    jls = [j, matrix[:, j]]
    price = 1.72
    df = pd.DataFrame({
        'i': [],
        'B1': [],
        'B2': [],
        'B3': [],
        'B4': [],
        'j': [],
        'A1': [],
        'A2': [],
        'A3': [],
        'A4': [],
        'Vmin': [],
        'Vmax': [],
        'V*': []
    })

    for k in range(50):
        Is.append(ils)

        Js.append(jls)

        Vmin = np.amin(Is[k][1])
        Vmax = np.amax(Js[k][1])

        Vavg = (Vmin + Vmax) / 2
        V.append([Vmin, Vmax, Vavg])
        df.loc[len(df)] = [ils[0] + 1, ils[1][0], ils[1][1], ils[1][2], ils[1][3],
                           jls[0] + 1, jls[1][0], jls[1][1], jls[1][2], jls[1][3],
                           Vmin,
                           Vmax,
                           Vavg]
        iprev = ils
        jprev = jls
        i = np.argmax(jls[1])
        ils = [i, matrix[i] + iprev[1]]
        j = np.argmin(ils[1])
        jls = [j, matrix[:, j] + jprev[1]]
    p = Counter([m[0] for m in Is])
    q = Counter([m[0] for m in Js])
    for i in p.keys():
        p[i] = p[i] / sum(p.values())
    for i in q.keys():
        q[i] = q[i] / sum(q.values())

    strat1 = p.most_common(1)[0][0] + 1
    strat1_val = p.most_common(1)[0][1]
    strat2 = q.most_common(1)[0][0] + 1
    strat2_val = q.most_common(1)[0][1]

    return df, strat1, strat1_val, strat2, strat2_val, price


def main():
    matrix = np.array([[-9, 7, 6, -2],
                       [13, 11, -5, 3],
                       [6, -4, 3, 2],
                       [5, 1, -1, 5]])
    res, strat1, strat1_val, strat2, strat2_val, price = calculate(matrix)
    pd.options.display.float_format = '{0:.0f}'.format
    print(res)
    print(f'\n\nГравцю P1 слід обрати стратегію {strat1} ({strat1_val})')
    print(f'\nГравцю P2 лід обрати стратегію {strat2} ({strat2_val})')
    print(f'\nЦіна гри {price}')


if __name__ == '__main__':
    main()
