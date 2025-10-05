from .tokenizer import tokenize

# Глобальные переменные состояния парсера
tokens: list[str] = []
current_token = None
pos = 0


def next_token():
    global pos, current_token
    pos += 1
    current_token = tokens[pos] if pos < len(tokens) else None


def primary():
    """Обрабатывает числа и скобки"""
    global current_token

    # Если видим скобку - разбираем выражение внутри
    if current_token == '(':
        next_token()
        result = expr()  # рекурсивно разбираем что внутри скобок
        if current_token != ')':
            raise SyntaxError("Ожидалась )")
        next_token()
        return result
    else:
        # Обработка обычного числа
        if current_token is None:
            raise SyntaxError("Выражение неполное - ожидалось число")

        try:
            num = float(current_token)
        except ValueError:
            raise SyntaxError(f"Ожидалось число, а не '{current_token}'")

        next_token()
        return num


def unary():
    """Обрабатывает унарные + и - (знаки перед числами)"""
    global current_token

    if current_token in ['+', '-']:
        # Запрещаем два оператора подряд
        if pos > 0 and tokens[pos - 1] in ['+', '-', '*', '/', '//', '%', '**']:
            raise SyntaxError(f"Два оператора подряд: '{tokens[pos - 1]}' и '{current_token}'")

        op = current_token
        next_token()
        if current_token is None:
            raise SyntaxError(f"После унарного '{op}' ожидалось число")

        # Проверяем, не идет ли после унарного оператора степень
        if current_token == '(':
            # Если скобка - разбираем как обычно
            value = unary()
        else:
            # Если не скобка, разбираем через pow, чтобы правильно обработать **
            value = pow()

        return value if op == '+' else -value
    else:
        return primary()


def pow():
    """Обрабатывает степень ** (право-ассоциативная)"""
    result = unary()

    if current_token == '**':
        next_token()
        right = pow()
        result = result ** right
    return result


def mul():
    """Обрабатывает *, /, //, %"""
    result = pow()

    while current_token in ['*', '/', '//', '%']:
        op = current_token
        next_token()
        right = pow()

        if op == '*':
            result *= right
        elif op == '/':
            if right == 0:
                raise ZeroDivisionError("Деление на ноль")
            result /= right
        elif op == '//':
            # // и % работают только с целыми числами
            if not (result.is_integer() and right.is_integer()):
                raise TypeError("// и % только для целых чисел")
            if right == 0:
                raise ZeroDivisionError("Деление на ноль")
            result = int(result) // int(right)
        elif op == '%':
            if not (result.is_integer() and right.is_integer()):
                raise TypeError("// и % только для целых чисел")
            if right == 0:
                raise ZeroDivisionError("Деление на ноль")
            result = int(result) % int(right)

    return result


def add():
    """Обрабатывает + и -"""
    result = mul()

    while current_token in ['+', '-']:
        op = current_token
        next_token()
        right = mul()
        if op == '+':
            result += right
        else:
            result -= right

    return result


def expr():
    return add()


def calculate(expression):
    """Главная функция - вычисляет выражение"""
    global tokens, current_token, pos

    tokens = tokenize(expression)

    if not tokens:
        raise ValueError("Пустое выражение")

    pos = 0
    current_token = tokens[0]

    result = expr()

    # Проверяем что разобрали всё выражение (не осталось лишних токенов)
    if current_token is not None:
        raise SyntaxError(f"Лишнее в конце: '{current_token}'")

    # Если результат целый - возвращаем как int
    if result.is_integer():
        return int(result)
    else:
        return result
