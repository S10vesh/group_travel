"""
Система планирования путешествия группой.
Начальный сценарий ПР1.
"""

from datetime import datetime


def get_trip_name() -> str:
    """Запрашивает название путешествия."""
    name = input("Введите название путешествия: ").strip()
    if not name:
        print("Название не может быть пустым. Установлено значение по умолчанию.")
        return "Групповое путешествие"
    return name


def get_participants_count() -> int:
    """Запрашивает и проверяет количество участников."""
    raw = input("Введите количество участников: ").strip()
    try:
        count = int(raw)
        if count < 1:
            print("Количество участников должно быть больше 0. Установлено 1.")
            return 1
        return count
    except ValueError:
        print("Ошибка ввода. Установлено значение 1.")
        return 1


def get_budget() -> float:
    """Запрашивает и проверяет бюджет."""
    raw = input("Введите общий бюджет (руб.): ").strip()
    try:
        budget = float(raw.replace(",", "."))
        if budget < 0:
            print("Бюджет не может быть отрицательным. Установлено 0.")
            return 0.0
        return budget
    except ValueError:
        print("Ошибка ввода. Установлено значение 0.")
        return 0.0


def get_start_date() -> str:
    """Запрашивает дату начала в формате ГГГГ-ММ-ДД."""
    raw = input("Введите дату начала (ГГГГ-ММ-ДД): ").strip()
    try:
        datetime.strptime(raw, "%Y-%m-%d")
        return raw
    except ValueError:
        print("Некорректный формат даты. Установлена сегодняшняя дата.")
        return datetime.now().strftime("%Y-%m-%d")


def check_participants(count: int) -> bool:
    """Проверяет, достаточно ли участников (минимум 3)."""
    return count >= 3


def check_budget(budget: float) -> bool:
    """Проверяет, достаточен ли бюджет (минимум 15000 руб.)."""
    return budget >= 15000.0


def check_date(date_str: str) -> bool:
    """Проверяет, что дата начала не в прошлом."""
    trip_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    today = datetime.now().date()
    return trip_date >= today


def main() -> None:
    print("=== Система планирования путешествия группой ===\n")

    trip_name = get_trip_name()
    participants = get_participants_count()
    budget = get_budget()
    start_date = get_start_date()

    print("\n--- Введённые данные ---")
    print(f"Название: {trip_name}")
    print(f"Участников: {participants}")
    print(f"Бюджет: {budget} руб.")
    print(f"Дата начала: {start_date}")

    print("\n--- Результаты проверки ---")

    participants_ok = check_participants(participants)
    budget_ok = check_budget(budget)
    date_ok = check_date(start_date)

    if participants_ok:
        print("Количество участников: достаточно")
    else:
        print("Количество участников: недостаточно (нужно минимум 3)")

    if budget_ok:
        print("Бюджет: достаточен")
    else:
        print("Бюджет: недостаточен (нужно минимум 15 000 руб.)")

    if date_ok:
        print("Дата начала: корректна")
    else:
        print("Дата начала: в прошлом")

    print("\n--- Итоговый статус ---")
    if participants_ok and budget_ok and date_ok:
        print(f"Путешествие «{trip_name}» можно планировать!")
    else:
        print(f"Путешествие «{trip_name}» пока нельзя планировать. Исправьте условия.")


if __name__ == "__main__":
    main()