import pytest

from src.parser import calculate


# ===== КОРРЕКТНЫЕ ВЫРАЖЕНИЯ =====
def test_basic_operations():
    """Базовые арифметические операции"""
    assert calculate("2 + 3") == 5
    assert calculate("5 - 2") == 3
    assert calculate("3 * 4") == 12
    assert calculate("8 / 2") == 4
    assert calculate("7 // 2") == 3
    assert calculate("7 % 3") == 1
    assert calculate("2 ** 3") == 8


def test_operator_priority():
    """Приоритет операторов"""
    assert calculate("2 + 3 * 4") == 14
    assert calculate("(2 + 3) * 4") == 20
    assert calculate("2 * 3 + 4") == 10
    assert calculate("2 + 3 * 4 ** 2") == 50
    assert calculate("(2 + 3) * 4 ** 2") == 80


def test_power_priority():
    """Приоритет степени"""
    assert calculate("-2 ** 2") == -4
    assert calculate("(-2) ** 2") == 4
    assert calculate("2 ** 3 ** 2") == 512
    assert calculate("(2 ** 3) ** 2") == 64


def test_unary_operators():
    """Унарные плюс и минус"""
    assert calculate("+5") == 5
    assert calculate("-5") == -5
    assert calculate("-(-5)") == 5
    assert calculate("+(-5)") == -5
    assert calculate("-(3 + 2)") == -5
    assert calculate("+(2 * 3)") == 6


def test_unary_with_operations():
    """Унарные операторы с другими операциями"""
    assert calculate("-3 * 2") == -6
    assert calculate("(-3) * 2") == -6
    assert calculate("2 * (-3)") == -6
    assert calculate("(-2) * (-3)") == 6


def test_float_numbers():
    """Дробные числа"""
    assert calculate("2.5 + 1.5") == 4.0
    assert calculate("3.14 * 2") == 6.28
    assert calculate("5.5 / 2") == 2.75
    assert calculate("1.5 ** 2") == 2.25


def test_integer_output():
    """Целочисленный вывод"""
    assert calculate("4.0 + 2.0") == 6
    assert calculate("8.0 / 2.0") == 4
    assert calculate("2.0 ** 3.0") == 8


def test_parentheses():
    """Скобки"""
    assert calculate("(2 + 3) * 4") == 20
    assert calculate("2 * (3 + 4)") == 14
    assert calculate("((2 + 3) * 4)") == 20
    assert calculate("(2 * (3 + 4))") == 14


def test_complex_parentheses():
    """Сложные вложенные скобки"""
    assert calculate("((((5))))") == 5
    assert calculate("(2 + (3 * (4 - 1)))") == 11
    assert calculate("((2 + 3) * (4 - 1)) + 5") == 20


def test_spaces():
    """Различные варианты пробелов"""
    assert calculate("2+3") == 5
    assert calculate("2 +3") == 5
    assert calculate("2+ 3") == 5
    assert calculate("  2  +  3  ") == 5
    assert calculate("( 2 + 3 ) * 4") == 20


def test_edge_cases():
    """Крайние случаи"""
    assert calculate("0") == 0
    assert calculate("1") == 1
    assert calculate("0 + 0") == 0
    assert calculate("1 * 1") == 1
    assert calculate("0 * 100") == 0
    assert calculate("100 ** 0") == 1
    assert calculate("0 ** 100") == 0


def test_complex_expressions():
    """Сложные выражения"""
    assert calculate("2 + 3 * 4 - 5 / 2") == 11.5
    assert calculate("(2 + 3) * (4 - 1) ** 2") == 45
    assert calculate("10 // 3 * 3 + 10 % 3") == 10
    assert calculate("2 ** 3 ** 2 - 4 * 2") == 504


def test_mixed_float_integer():
    """Смешанные дробные и целые числа"""
    assert calculate("2.5 * 4") == 10.0
    assert calculate("5 // 2 + 1.5") == 3.5
    assert calculate("3.5 ** 2") == 12.25


def test_right_associativity():
    """Право-ассоциативность степени"""
    assert calculate("2 ** 3 ** 2") == 512
    assert calculate("2 ** 2 ** 3") == 256
    assert calculate("3 ** 2 ** 2") == 81


def test_unary_with_power():
    """Унарные операторы со степенью"""
    assert calculate("-2 ** 2") == -4
    assert calculate("(-2) ** 2") == 4
    assert calculate("-2 ** 3") == -8
    assert calculate("(-2) ** 3") == -8
    assert calculate("-(2 ** 2)") == -4


def test_special_division_cases():
    """Особые случаи деления"""
    assert calculate("0 / 5") == 0
    assert calculate("5 / 1") == 5
    assert calculate("1 / 2") == 0.5
    assert calculate("10 // 3") == 3
    assert calculate("10 % 3") == 1


# ===== ОБРАБОТКА ОШИБОК =====
def test_division_by_zero():
    """Ошибки деления на ноль"""
    with pytest.raises(ZeroDivisionError):
        calculate("5 / 0")
    with pytest.raises(ZeroDivisionError):
        calculate("10 // 0")
    with pytest.raises(ZeroDivisionError):
        calculate("10 % 0")


def test_integer_operations_errors():
    """Ошибки для целочисленных операций с дробными числами"""
    with pytest.raises(TypeError):
        calculate("5.5 // 2")
    with pytest.raises(TypeError):
        calculate("5.5 % 2")
    with pytest.raises(TypeError):
        calculate("5 // 2.5")


def test_syntax_errors():
    """Синтаксические ошибки"""
    with pytest.raises(SyntaxError):
        calculate("2 + ")  # неполное выражение
    with pytest.raises(SyntaxError):
        calculate("+")  # только оператор
    with pytest.raises(SyntaxError):
        calculate("(2 + 3")  # незакрытая скобка
    with pytest.raises(SyntaxError):
        calculate("2 + 3)")  # лишняя скобка


def test_two_operators_errors():
    """Два оператора подряд"""
    with pytest.raises(SyntaxError):
        calculate("2 ++ 3")  # два плюса
    with pytest.raises(SyntaxError):
        calculate("2 -- 3")  # два минуса
    with pytest.raises(SyntaxError):
        calculate("2 ** * 3")  # степень и умножение
    with pytest.raises(SyntaxError):
        calculate("2 // / 3")  # два деления
    with pytest.raises(SyntaxError):
        calculate("3 * -2")  # бинарный и унарный без скобок
    with pytest.raises(SyntaxError):
        calculate("3 + -2")  # бинарный и унарный без скобок


def test_unknown_symbols_errors():
    """Неизвестные символы"""
    with pytest.raises(SyntaxError):
        calculate("2 @ 3")
    with pytest.raises(SyntaxError):
        calculate("2 & 3")
    with pytest.raises(SyntaxError):
        calculate("abc")


def test_empty_expression():
    """Пустое выражение"""
    with pytest.raises(ValueError):
        calculate("")
    with pytest.raises(ValueError):
        calculate("   ")
