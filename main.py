"""
Система планирования путешествия группой.
Точка входа и консольное меню (ПР2).
"""

from storage import load_json, save_json
from trips import (
    add_trip,
    find_trip_by_name,
    get_trip_by_id,
    sort_trips_by_budget,
)
from participants import (
    add_participant,
    count_participants,
    can_start_planning,
)
from utils import input_int, input_float, input_date


def show_trips(trips: list) -> None:
    """Вывести список путешествий."""
    if not trips:
        print("Путешествий пока нет.")
        return
    print("\n--- Список путешествий ---")
    for t in trips:
        print(
            f"ID: {t['id']} | {t['name']} | "
            f"Дата: {t['start_date']} | "
            f"Бюджет: {t['budget']} руб. | "
            f"Мин. участников: {t['min_participants']}"
        )


def show_participants(participants: list, trips: list) -> None:
    """Вывести список участников."""
    if not participants:
        print("Участников пока нет.")
        return
    print("\n--- Список участников ---")
    for p in participants:
        trip = get_trip_by_id(trips, p["trip_id"])
        trip_name = trip["name"] if trip else "—"
        print(f"ID: {p['id']} | {p['name']} | Путешествие: {trip_name}")


def main() -> None:
    trips = load_json("trips.json")
    participants = load_json("participants.json")

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
            save_json("trips.json", trips)
            print(f"Путешествие «{trip['name']}» добавлено (ID={trip['id']}).")

        elif choice == "3":
            query = input("Введите часть названия: ").strip()
            found = find_trip_by_name(trips, query)
            show_trips(found)

        elif choice == "4":
            show_participants(participants, trips)

        elif choice == "5":
            show_trips(trips)
            trip_id = input_int("ID путешествия: ")
            trip = get_trip_by_id(trips, trip_id)
            if not trip:
                print("Путешествие с таким ID не найдено.")
                continue
            name = input("Имя участника: ").strip()
            p = add_participant(participants, name, trip_id)
            save_json("participants.json", participants)
            print(f"Участник «{p['name']}» добавлен.")

        elif choice == "6":
            show_trips(trips)
            trip_id = input_int("ID путешествия: ")
            trip = get_trip_by_id(trips, trip_id)
            if not trip:
                print("Путешествие не найдено.")
                continue
            current = count_participants(participants, trip_id)
            ready = can_start_planning(trip, participants)
            print(f"\nПутешествие: {trip['name']}")
            print(f"Участников сейчас: {current}")
            print(f"Нужно минимум: {trip['min_participants']}")
            if ready:
                print("Статус: можно начинать планирование!")
            else:
                print("Статус: ещё недостаточно участников.")

        elif choice == "7":
            sorted_trips = sort_trips_by_budget(trips)
            show_trips(sorted_trips)

        elif choice == "0":
            save_json("trips.json", trips)
            save_json("participants.json", participants)
            print("Данные сохранены. Выход.")
            break

        else:
            print("Неверный пункт меню.")


if __name__ == "__main__":
    main()
