from src.constants import DIGITS, SYMBOLS


def tokenize(expression: str) -> list[str]:
    """Разбивает математическое выражение на токены"""

    expression = expression.replace('**', 'p').replace('//', 'd')

    s = ''  # накопитель текущего числа
    result = []
    for char in expression:

        if char == ' ':
            if s != '':
                result.append(s)
                s = ''
            continue

        elif char in DIGITS:
            s += char

        elif char in SYMBOLS:
            if s != '':
                result.append(s)
                s = ''
            result.append(char.replace('p', '**').replace('d', '//'))
        else:
            raise SyntaxError(f'Неизвестный символ: {char}')

    if s != '':
        result.append(s)

    return result
