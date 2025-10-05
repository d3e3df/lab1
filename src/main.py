from src.parser import calculate


def main():
    print("Калькулятор M1 (Рекурсивный спуск)")
    print("Поддерживает: +, -, *, /, //, %, **, скобки, унарные +/-")
    print("Введите 'exit' для выхода")

    while True:
        try:
            expression = input("> ").strip()
            if expression.lower() == 'exit':
                break
            if not expression:
                raise ValueError("Пустое выражение")

            result = calculate(expression)
            print(f"Результат: {result}")

        except (SyntaxError, ValueError, ZeroDivisionError, TypeError) as e:
            print(f"Ошибка: {e}")
        except KeyboardInterrupt:
            print("\nВыход...")
            break


if __name__ == "__main__":
    main()
