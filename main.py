"""Система планирования путешествия группой. Точка входа (ПР3)."""

from storage import (
    load_trips, save_trips,
    load_participants, save_participants,
)
from models import Trip, TravelGroup
from models.trips import (
    add_trip, find_trip_by_name, get_trip_by_id, sort_trips_by_budget,
)
from models.participants import (
    add_participant, get_participants_by_trip,
)
from utils import input_int, input_float, input_date


def show_trips(trips: list[Trip]) -> None:
    """Вывести список путешествий."""
    if not trips:
        print("Путешествий пока нет.")
        return
    print("\n--- Список путешествий ---")
    for t in trips:
        print(t)


def show_participants(participants: list) -> None:
    """Вывести список участников."""
    if not participants:
        print("Участников пока нет.")
        return
    print("\n--- Список участников ---")
    for p in participants:
        print(p)


def main() -> None:
    trips = load_trips()
    participants = load_participants(trips)

    while True:
        print("\n=== Система планирования путешествия группой ===")
        print("1. Показать путешествия")
        print("2. Добавить путешествие")
        print("3. Найти путешествие по названию")
        print("4. Показать участников")
        print("5. Добавить участника")
        print("6. Проверить готовность путешествия")
        print("7. Сортировать путешествия по бюджету")
        print("0. Выход")

        choice = input("\nВыберите действие: ").strip()

        if choice == "1":
            show_trips(trips)

        elif choice == "2":
            name = input("Название путешествия: ").strip()
            start = input_date("Дата начала (ГГГГ-ММ-ДД): ")
            budget = input_float("Бюджет (руб.): ")
            min_p = input_int("Минимальное количество участников: ")
            trip = add_trip(trips, name, start, budget, min_p)
            save_trips(trips)
            print(f"Путешествие «{trip.name}» добавлено (ID={trip.id}).")

        elif choice == "3":
            query = input("Введите часть названия: ").strip()
            show_trips(find_trip_by_name(trips, query))

        elif choice == "4":
            show_participants(participants)

        elif choice == "5":
            show_trips(trips)
            trip_id = input_int("ID путешествия: ")
            trip = get_trip_by_id(trips, trip_id)
            if not trip:
                print("Путешествие с таким ID не найдено.")
                continue
            name = input("Имя участника: ").strip()
            p = add_participant(participants, name, trip)
            save_participants(participants)
            print(f"Участник «{p.name}» добавлен.")

        elif choice == "6":
            show_trips(trips)
            trip_id = input_int("ID путешествия: ")
            trip = get_trip_by_id(trips, trip_id)
            if not trip:
                print("Путешествие не найдено.")
                continue
            group = TravelGroup(trip)
            for p in get_participants_by_trip(participants, trip):
                group.add_participant(p)
            print(f"\n{group}")

        elif choice == "7":
            show_trips(sort_trips_by_budget(trips))

        elif choice == "0":
            save_trips(trips)
            save_participants(participants)
            print("Данные сохранены. Выход.")
            break

        else:
            print("Неверный пункт меню.")


if __name__ == "__main__":
    main()
