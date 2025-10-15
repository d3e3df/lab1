from src.tokenizer import tokenize


class Calculator:
    """Калькулятор"""

    def __init__(self) -> None:
        """Инициализация переменных состояния парсера"""
        self.tokens: list[str] = []
        self.current_token: str | None = None
        self.pos: int = 0

    def next_token(self) -> None:
        """Переход к следующему токену"""
        self.pos += 1
        self.current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def primary(self) -> float:
        """Обрабатывает выражения в скобках или числа"""
        if self.current_token == '(':
            self.next_token()
            result = self.expr()
            if self.current_token != ')':
                raise SyntaxError("Ожидалась )")
            self.next_token()
        else:
            if self.current_token is None:
                raise SyntaxError("Выражение неполное - ожидалось число")
            try:
                result = float(self.current_token)
            except ValueError:
                raise SyntaxError(f"Ожидалось число, а не '{self.current_token}'")

            self.next_token()

        return result

    def unary(self) -> float:
        """Обрабатывает унарные операторы"""
        if self.current_token in ['+', '-']:
            if self.pos > 0 and self.tokens[self.pos - 1] in ['+', '-', '*', '/', '//', '%', '**']:
                raise SyntaxError(f"Два оператора подряд: '{self.tokens[self.pos - 1]}' и '{self.current_token}'")

            operator = self.current_token
            self.next_token()
            if self.current_token is None:
                raise SyntaxError(f"После унарного '{operator}' ожидалось число")
            if self.current_token == '(':
                result = self.unary()
            else:
                result = self.pow()
            return result if operator == '+' else -result
        return self.primary()

    def pow(self) -> float:
        """Обрабатывает операцию возведения в степень"""
        result = self.unary()
        if self.current_token == '**':
            self.next_token()
            result **= self.pow()
        return result

    def mul(self) -> float:
        """Обрабатывает мультипликативные операции"""
        result = self.pow()
        while self.current_token in ['*', '/', '//', '%']:
            operator = self.current_token
            self.next_token()
            right = self.pow()

            match operator:
                case '*':
                    result *= right
                case '/':
                    if right == 0:
                        raise ZeroDivisionError("Деление на ноль")
                    result /= right
                case '//':
                    if not (result.is_integer() and right.is_integer()):
                        raise TypeError("// и % только для целых чисел")
                    if right == 0:
                        raise ZeroDivisionError("Деление на ноль")
                    result //= right
                case '%':
                    if not (result.is_integer() and right.is_integer()):
                        raise TypeError("// и % только для целых чисел")
                    if right == 0:
                        raise ZeroDivisionError("Деление на ноль")
                    result %= right
        return result

    def add(self) -> float:
        """Обрабатывает аддитивные операции"""
        result = self.mul()

        while self.current_token in ['+', '-']:
            operator = self.current_token
            self.next_token()
            if operator == '+':
                result += self.mul()
            else:
                result -= self.mul()

        return result

    def expr(self) -> float:
        """Начинает разбор выражения"""
        return self.add()

    def calculate(self, exp: str) -> float:
        """Вычисляет математическое выражение"""
        self.tokens = tokenize(exp)

        if not self.tokens:
            raise ValueError("Пустое выражение")

        self.current_token = self.tokens[0]
        self.pos = 0

        result = self.expr()

        if self.current_token is not None:
            raise SyntaxError(f"Лишнее в конце: '{self.current_token}'")

        try:
            return int(result) if result.is_integer() else result
        except AttributeError:
            raise Exception("Ответ не принадлежит R")
