import pandas as pd
import re


def check_file():
    dataFile = 'Lab1_data.xlsx'
    data = pd.read_excel(dataFile, engine='openpyxl')
    for i in range(len(data)):
        data = data.rename(index={i: f'x{i + 1}'})
    print(data)
    return data


def metod_glavnogo_kriteriya(data):
    print('\nМЕТОД ВИДІЛЕННЯ ОСНОВНОГО КРИТЕРІЮ\n')
    for crit in range(len(data.columns) - 1):
        updated_data = data
        index = crit + 1
        while True:
            try:
                ex = int(input(f'Головним критерієм є {updated_data.columns[index]}. 1 - min, 2 - max: '))
                if ex != 1 and ex != 2:
                    raise ValueError
            except ValueError:
                print('Введено неправильне значення')
                continue
            break

        while True:
            crit_val = input(f'Обмеження {";".join(updated_data.columns.delete([0, index]))}: ')
            try:
                for i, rec_d in enumerate(crit_val.split(';')):
                    gl, val = re.findall(r'([<,>,=]+)(.+)', rec_d)[0]
                    val = float(val)
                    if gl == '<':
                        updated_data = updated_data.drop(
                            updated_data[updated_data[updated_data.columns.delete([0, index])[i]] >= val].index)
                    elif gl == '>':
                        updated_data = updated_data.drop(
                            updated_data[updated_data[updated_data.columns.delete([0, index])[i]] <= val].index)
                    elif gl == '<=':
                        updated_data = updated_data.drop(
                            updated_data[updated_data[updated_data.columns.delete([0, index])[i]] > val].index)
                    elif gl == '>=':
                        updated_data = updated_data.drop(
                            updated_data[updated_data[updated_data.columns.delete([0, index])[i]] < val].index)
                try:
                    if ex == 1:
                        nead_index = updated_data[updated_data.columns[index]].idxmin()
                    elif ex == 2:
                        nead_index = updated_data[updated_data.columns[index]].idxmax()
                    for i in updated_data.index:
                        if i != nead_index:
                            try:
                                updated_data = updated_data.drop(i)
                            except Exception as ex:
                                print(ex)
                    print('\nНайкраще рішення: \n')
                    for i in updated_data:
                        print(i, ':', updated_data[i].iloc[0])
                    print('=========================================================')
                except ValueError:
                    print('Не знайдено кращого рішення із заданими обмеженнями')
            except Exception as ex:
                print(f'Введено неправильне значення. ({ex})')
                continue
            break


def function_cost_analysis(data):
    print('\nМЕТОД ФУНКЦІОНАЛЬНО-ВАРТІСНОГО АНАЛІЗУ\n')
    for crit in range(len(data.columns) - 2):
        updated_data = data
        new_col_name = ''
        index = crit + 1
        while True:
            lim = input(f'Обмеження {updated_data.columns[index]}: ')
            gl, val = re.findall(r'([<,>,=]+)(.+)', lim)[0]
            val = float(val)
            if gl == '<':
                updated_data = updated_data.drop(
                    updated_data[updated_data[updated_data.columns[index]] >= val].index)
            elif gl == '>':
                updated_data = updated_data.drop(
                    updated_data[updated_data[updated_data.columns[index]] <= val].index)
            elif gl == '<=':
                updated_data = updated_data.drop(
                    updated_data[updated_data[updated_data.columns[index]] > val].index)
            elif gl == '>=':
                updated_data = updated_data.drop(
                    updated_data[updated_data[updated_data.columns[index]] < val].index)
            new_col_name = ' / '.join(updated_data.columns.delete([0, index]))
            updated_data[new_col_name] = updated_data[updated_data.columns.delete([0, index])[0]] / updated_data[
                updated_data.columns.delete([0, index])[1]]

            print(f'\nВідношення {new_col_name}:\n')
            updated_data = updated_data.iloc[:, [0, updated_data.columns.get_loc(new_col_name)]]
            print(updated_data + '\n')
            print('\nНайкраще рішення:\n')
            print(data.loc[updated_data[new_col_name].idxmax()])
            print('=========================================================')
            try:
                pass
            except Exception as ex:
                print(f'Введено неправильне значення. ({ex})')
                continue
            break


def func_cor(updated_data):
    print()
    print('ФУНКЦІЯ КОРИСНОСТІ')
    print()
    k = {'k+': [], 'k-': [], 'k+ - k-': []}
    for i in updated_data.columns[1:]:
        if i == updated_data.columns[-1]:
            (k['k+']).append(updated_data[i].min())
        else:
            (k['k+']).append(updated_data[i].max())
    for i in updated_data.columns[1:]:
        if i == updated_data.columns[-1]:
            (k['k-']).append(updated_data[i].max())
        else:
            (k['k-']).append(updated_data[i].min())
    for i in updated_data.columns[1:]:
        if i == updated_data.columns[-1]:
            (k['k+ - k-']).append(updated_data[i].min() - updated_data[i].max())
        else:
            (k['k+ - k-']).append(updated_data[i].max() - updated_data[i].min())
    print('Значення критеріїв k+ та k-:\n')
    Kdf = pd.dataFrame(k)
    print(Kdf)
    col = []
    print('\nЗначення функції локальної корисності:\n')
    for i in updated_data.columns[1:]:

        if i == updated_data.columns[-1]:
            val = (updated_data[i] - updated_data[i].max()) / (updated_data[i].min() - updated_data[i].max())
        else:
            val = (updated_data[i] - updated_data[i].min()) / (updated_data[i].max() - updated_data[i].min())
        col.append(val)
    res = pd.concat(col, axis=1)
    print(res)
    print('\nСХЕМА МАКСИМІНА\n')
    print('Значення функції min pi(x):')
    print(res.min(axis=1))
    print('max min pi (x) =', end=' ')
    print(res.min(axis=1).max())
    max_cor(res)


def max_cor(df):
    print('\nМОДЕЛЬ МАКСИМАЛЬНОЇ УЗАГАЛЬНЕНОЇ КОРИСНОСТІ\n')
    dflist = []
    for i_1 in enumerate(df):
        tlist = []
        coef = input(f'Коефіцієнти p{i_1 + 1}: ')
        clist = []
        for c in coef.split(';'):
            clist.append(float(c))
        for i_2, j in enumerate(df):
            tlist.append(df[j] * clist[i_2])
        res = pd.concat(tlist, axis=1)
        sumr = res.sum(axis=1)
        sumr = sumr.append(pd.Series([(res.sum(axis=1)).max()], index=['max']))
        dflist.append(sumr)
    print(pd.concat(dflist, axis=1))
    print('=============================')
    return 0


if __name__ == '__main__':
    data = check_file()
    metod_glavnogo_kriteriya(data)
    function_cost_analysis(data)
    func_cor(data)
