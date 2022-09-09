import pandas as pd


def check_file():
    data_file = 'Lab2_Data.xlsx'
    data = pd.read_excel(data_file, engine='openpyxl')
    for i in range(len(data)):
        data = data.rename(index={i: f'П{i + 1}'})
    return data


def laplas(data):
    data_lap = data
    print('\nКритерій недостатньої підстави Лапласа:\n')
    m = len(data_lap.columns)
    for i in range(len(data_lap)):
        data_lap = data_lap.rename(index={f'П{i + 1}': f'M(x{i + 1})'})
    s = data_lap.sum(axis=1) / m
    print(s)
    print('E(x*) = max M(xi) = ', s.max())
    for i, j in enumerate(s):
        if j == s.max():
            print(
                f'Таким чином, якщо є підстави припускати, що всі сценарії рівноймовірні, '
                f'фірмі рекомендується придбати пакет акцій П{i + 1}')


def vald(data):
    data_va = data
    print('\nМаксимінний критерій Вальда:\n')
    for i in range(len(data_va)):
        data_va = data_va.rename(index={f'П{i + 1}': f'W{i + 1}'})
    s = data_va.min(axis=1)
    print(s)
    print('E(x*) = max Wi = ', s.max())
    for i, j in enumerate(s):
        if j == s.max():
            print(f'Таким чином, фірмі слід придбати пакет акцій підприємства П{i + 1}')


def matrix_riska(data):
    data_r = data
    s = data_r.max()
    data_r = s - data_r
    return data_r


def savage(data):
    data_sav = data
    print('\nКритерій мінімаксного ризику Севіджа:\n')
    for i in range(len(data_sav)):
        data_sav = data_sav.rename(index={f'П{i + 1}': f'R{i + 1}'})
    s = data_sav.max(axis=1)
    print(s)
    print('E(x*) = min Ri = ', s.min())
    for i, j in enumerate(s):
        if j == s.min():
            print(f'Таким чином, фірмі слід придбати пакет акцій підприємства П{i + 1}')


def gurv(data):
    data_g = data
    print('\nКритерій песимізму-оптимізму Гурвіца:\n')
    for i in range(len(data_g)):
        data_g = data_g.rename(index={f'П{i + 1}': f'H{i + 1}'})
    a = float(input('Введіть коефіціент песимізму a: '))
    minS = data_g.min(axis=1)
    maxS = data_g.max(axis=1)
    H = a * minS + (1 - a) * maxS
    print(H)
    print('E(x*) = max Hi = ', H.max())
    for i, j in enumerate(H):
        if j == H.max():
            print(f'Таким чином, фірмі слід придбати пакет акцій підприємства П{i + 1}')


def main():
    data = check_file()
    print('\nМАТРИЦЯ ВИГРАШІВ:\n\n', data)
    data_r = matrix_riska(data)
    print('\nМАТРИЦЯ РИЗИКІВ:\n\n', data_r)
    laplas(data)
    vald(data)
    savage(data)
    gurv(data)


if __name__ == '__main__':
    main()
