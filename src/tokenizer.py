from .constants import SYMBOLS, DIGITS


def tokenize(expression):
    # Временная замена двойных операторов на однобуквенные для упрощения разбора
    exp = expression.replace('**', 'p').replace('//', 'd')
    res = []
    s = ''  # накопитель для текущего числа
    i = 0

    while i < len(exp):
        char = exp[i]

        # Пробелы разделяют числа
        if char == ' ':
            if s != '':
                res.append(s)
                s = ''
            i += 1
            continue

        # Собираем цифры и точки в число
        if char in DIGITS:
            s += char

        # Операторы и скобки - завершаем текущее число и добавляем оператор
        elif char in SYMBOLS:
            if s != '':
                res.append(s)
                s = ''
            # Возвращаем оригинальные операторы обратно
            token = char.replace('d', '//').replace('p', '**')
            res.append(token)

        # Любой другой символ - ошибка
        else:
            raise SyntaxError(f"Неизвестный символ: {char}")

        i += 1

    # Добавляем последнее число, если оно есть
    if s != '':
        res.append(s)

    return res
