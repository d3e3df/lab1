import pytest

from src.parser import Calculator

calc = Calculator()


def test_operator_priority() -> None:
    """Приоритет операторов"""
    assert calc.calculate("52345 + 62589 * 334") == 20957071
    assert calc.calculate("(52345 + 62589) * 334") == 38387956
    assert calc.calculate("20267 * 282 - 544345") == 5170949
    assert calc.calculate("52346 - 8 * 72 ** 3") == -2933638
    assert calc.calculate("(52346 - 8) * 72 ** 3") == 19535053824
    assert calc.calculate("-7 ** 2") == -49
    assert calc.calculate("(-7) ** 2") == 49
    assert calc.calculate("3 ** 2 ** 5") == 1853020188851841
    assert calc.calculate("(3 ** 2) ** 5") == 59049


def test_unary_operators() -> None:
    """Унарные плюс и минус"""
    assert calc.calculate("+28364") == 28364
    assert calc.calculate("-729745") == -729745
    assert calc.calculate("-(394572)") == -394572
    assert calc.calculate("+(-97235)") == -97235
    assert calc.calculate("-(25346 + 4256)") == -29602
    assert calc.calculate("-9672346253 * 23546") == -227745064873138
    assert calc.calculate("(-9672346253) * 23546") == -227745064873138
    assert calc.calculate("9235004 * (-354325)") == -3272192792300
    assert calc.calculate("(-9235004) * (-354325)") == 3272192792300


def test_float_numbers() -> None:
    """Дробные числа"""
    assert calc.calculate("6.236 + 8.6432") == pytest.approx(14.8792)
    assert calc.calculate("6.236 * 8.6432") == pytest.approx(53.8989952)
    assert calc.calculate("0.1 + 0.2") == pytest.approx(0.3)
    assert calc.calculate("7.28 / 4") == pytest.approx(1.82)
    assert calc.calculate("1.2 ** 4") == pytest.approx(2.0736)
    assert calc.calculate("(6.236 + 8.6432) * 2") == pytest.approx(29.7584)


def test_parentheses() -> None:
    """Скобки"""
    assert calc.calculate("(61346317 - 568) // 666") == 92110
    assert calc.calculate("61346317 - (568 // 666)") == 61346317
    assert calc.calculate(
        "(-(-(-(-(-(-(-(-(-(-(-(-(-(-(-(-(-(-(-(111111111111111))))))))))))))))))))") == -111111111111111
    assert calc.calculate("(52345 + (82523 * (238437923 - 48782)))") == 19672587135088
    assert calc.calculate("((272363 + 30536) * (523 - 99999)) + 7777") == -30131173147


def test_division_by_zero() -> None:
    """Ошибки деления на ноль"""
    with pytest.raises(ZeroDivisionError):
        calc.calculate("6969696969 / 0")
    with pytest.raises(ZeroDivisionError):
        calc.calculate("7272727272 // 0")
    with pytest.raises(ZeroDivisionError):
        calc.calculate("88888888888 % 0")


def test_integer_operations_errors() -> None:
    """Ошибки для целочисленных операций с дробными числами"""
    with pytest.raises(TypeError):
        calc.calculate("3.14159 // 7")
    with pytest.raises(TypeError):
        calc.calculate("9.23668 % 111")
    with pytest.raises(TypeError):
        calc.calculate("7345 // 6.66")


def test_syntax_errors() -> None:
    """Синтаксические ошибки"""
    with pytest.raises(SyntaxError):
        calc.calculate("2 + ")
    with pytest.raises(SyntaxError):
        calc.calculate("+")
    with pytest.raises(SyntaxError):
        calc.calculate("(2 + 3")
    with pytest.raises(SyntaxError):
        calc.calculate("2 + 3)")


def test_two_operators_errors() -> None:
    """Два оператора подряд"""
    with pytest.raises(SyntaxError):
        calc.calculate("9 ++ 255555")
    with pytest.raises(SyntaxError):
        calc.calculate("2534 -- 7435")
    with pytest.raises(SyntaxError):
        calc.calculate("96996 ** * 2202020")
    with pytest.raises(SyntaxError):
        calc.calculate("683456 // / 30000003")
    with pytest.raises(SyntaxError):
        calc.calculate("63456 * -99275")
    with pytest.raises(SyntaxError):
        calc.calculate("782546 + -57892")


def test_unknown_symbols_errors() -> None:
    """Неизвестные символы"""
    with pytest.raises(SyntaxError):
        calc.calculate("53245 & 25346")
    with pytest.raises(SyntaxError):
        calc.calculate("666 $ 777")
    with pytest.raises(SyntaxError):
        calc.calculate("xyz")


def test_empty_expression() -> None:
    """Пустое выражение"""
    with pytest.raises(ValueError):
        calc.calculate("")
    with pytest.raises(ValueError):
        calc.calculate("   ")


def test_complex_numbers() -> None:
    """Комплексные числа"""
    with pytest.raises(Exception):
        calc.calculate("(-1)**0.5")
