"""Вспомогательные функции безопасного ввода."""

from datetime import datetime, date


def input_int(prompt: str) -> int:
    """Запросить у пользователя целое число с повтором при ошибке."""
    while True:
        raw = input(prompt).strip()
        try:
            return int(raw)
        except ValueError:
            print("Ошибка: введите целое число.")


def input_float(prompt: str) -> float:
    """Запросить у пользователя число (float) с повтором при ошибке."""
    while True:
        raw = input(prompt).strip().replace(",", ".")
        try:
            return float(raw)
        except ValueError:
            print("Ошибка: введите число.")


def input_date(prompt: str) -> date:
    """Запросить дату в формате ГГГГ-ММ-ДД."""
    while True:
        raw = input(prompt).strip()
        try:
            return datetime.strptime(raw, "%Y-%m-%d").date()
        except ValueError:
            print("Ошибка: введите дату в формате ГГГГ-ММ-ДД.")
