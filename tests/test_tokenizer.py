import pytest

from src.tokenizer import tokenize


def test_valid_expressions() -> None:
    """Токенизация с допустимыми символами"""
    assert tokenize("10+5") == ['10', '+', '5']
    assert tokenize("11   - 7") == ['11', '-', '7']
    assert tokenize(" 238    * ( - 3) + 51") == ['238', '*', '(', '-', '3', ')', '+', '51']
    assert tokenize("+-*214(())))((") == ['+', '-', '*', '214', '(', '(', ')', ')', ')', ')', '(', '(']
    assert tokenize("1%2//3/4+5-6*(7)**8") == ['1', '%', '2', '//', '3', '/', '4', '+', '5', '-', '6', '*', '(', '7',
                                               ')', '**', '8']


def test_invalid_expressions() -> None:
    """Токенизация с недопустимыми символами"""
    with pytest.raises(SyntaxError):
        tokenize("xyz")
    with pytest.raises(SyntaxError):
        tokenize("666 $ 666")
    with pytest.raises(SyntaxError):
        tokenize("a+b-c")
    with pytest.raises(SyntaxError):
        tokenize("5 ^ 5")
    with pytest.raises(SyntaxError):
        tokenize("#33523452")
