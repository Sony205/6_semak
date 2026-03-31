import re


def validate_login(login):
    """Задание 1: Валидация логина"""
    pattern = r'^[A-Za-z][A-Za-z0-9_]{4,19}(?<!_)$'
    return bool(re.fullmatch(pattern, login))


def find_dates(text):
    """Задание 2: Поиск дат в тексте"""
    pattern = r'\b(\d{1,2})([.\-/])(\d{1,2})\2(\d{2}|\d{4})\b'
    return [m.group(0) for m in re.finditer(pattern, text)]


def parse_log(log):
    """Задание 3: Парсинг логов"""
    # 2024-02-10 14:23:01 INFO user=ada action=login ip=192.168.1.15
    pattern = (
        r'^(\d{4}-\d{2}-\d{2})\s+'
        r'(\d{2}:\d{2}:\d{2})\s+'
        r'\w+\s+'
        r'user=([^\s]+)\s+'
        r'action=([^\s]+)\s+'
        r'ip=((?:\d{1,3}\.){3}\d{1,3})$'
    )
    match = re.fullmatch(pattern, log.strip())
    if match:
        return {
            'date': match.group(1),
            'time': match.group(2),
            'user': match.group(3),
            'action': match.group(4),
            'ip': match.group(5)
        }
    return None


def validate_password(password):
    """Задание 4: Проверка пароля"""
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'\d', password):
        return False
    if not re.search(r'[!@#$%^&*]', password):
        return False
    return True


def validate_email(email, domains):
    """Задание 5: E-mail с ограниченными доменами"""
    email = email.strip()
    m = re.fullmatch(r'([A-Za-z0-9._%+-]+)@([A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+)', email)
    if not m:
        return False
    domain = m.group(2).lower()
    allowed = {d.lower() for d in domains}
    return domain in allowed


def normalize_phone(phone):
    """Задание 6: Нормализация телефонных номеров"""
    digits = re.sub(r'\D', '', phone)

    if len(digits) == 10:
        digits = '+7' + digits
    elif len(digits) == 11 and digits[0] in '78':
        digits = '+7' + digits[1:]
    else:
        return None

    return digits



def main():

    while True:
        print("\nВыберите номер задания (1-6) или 0 для выхода:")
        print("1. Валидация логина")
        print("2. Поиск дат в тексте")
        print("3. Парсинг логов")
        print("4. Проверка пароля")
        print("5. E-mail с ограниченными доменами")
        print("6. Нормализация телефонных номеров")
        print("0. Выход")

        choice = input("\nВаш выбор: ")

        if choice == '0':
            print("Выход из программы.")
            break

        elif choice == '1':
            login = input("Введите логин: ")
            result = validate_login(login)
            print(f"Результат: {result}")

        elif choice == '2':
            text = input("Введите текст: ")
            result = find_dates(text)
            print(f"Найденные даты: {result}")

        elif choice == '3':
            log = input("Введите лог: ")
            result = parse_log(log)
            print(f"Результат: \n{result}")

        elif choice == '4':
            password = input("Введите пароль: ")
            result = validate_password(password)
            print(f"Результат: {result}")

        elif choice == '5':
            email = input("Введите email: ")
            domains = ['gmail.com', 'yandex.ru', 'edu.ru']
            result = validate_email(email, domains)
            print(f"Результат: {result}")
            print(f"Разрешённые домены: {', '.join(domains)}")

        elif choice == '6':
            phone = input("Введите телефон: ")
            result = normalize_phone(phone)
            if result is None:
                print("Ошибка: некорректный номер. Введите 10 цифр (9991234567) или 11 цифр (8/7 + 10 цифр).") 
            else:
                print(f"Результат: {result}")

        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
