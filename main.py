import json
from pathlib import Path

from src.utils import get_financial_transactions
from src.readers import read_csv_transactions, read_excel_transactions
from src.processing import filter_by_state, sort_by_date
from src.search import process_bank_search, process_bank_operations
from src.widget import mask_account_card, get_date


def get_safe_amount(op):
    """Безопасно получает сумму, возвращает 'Неизвестно' при отсутствии поля."""
    try:
        return op["operationAmount"]["amount"]
    except (KeyError, TypeError):
        return "Неизвестно"


def get_safe_currency(op):
    """Безопасно получает валюту."""
    try:
        return op["operationAmount"]["currency"]["code"]
    except (KeyError, TypeError):
        return "???"


def main():
    print("Программа: Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input("Пожалуйста, выберите пункт меню: ").strip()

    if choice not in ["1", "2", "3"]:
        print("Программа: Неверный выбор. Завершение работы.")
        return

    file_path = input("Введите путь к файлу: ").strip()
    if not Path(file_path).exists():
        print("Программа: Файл не найден.")
        return

    # Чтение данных
    if choice == "1":
        print("Программа: Для обработки выбран JSON-файл.")
        transactions = get_financial_transactions(file_path)
    elif choice == "2":
        print("Программа: Для обработки выбран CSV-файл.")
        transactions = read_csv_transactions(file_path)
    else:
        print("Программа: Для обработки выбран XLSX-файл.")
        transactions = read_excel_transactions(file_path)

    if not transactions:
        print("Программа: Не найдено ни одной транзакции в файле.")
        return

    # Фильтрация по статусу
    print("Программа: Введите статус, по которому необходимо выполнить фильтрацию.")
    print("Доступные для фильтрации статусы: EXECUTED, CANCELED, PENDING")
    status = input("Пожалуйста, введите статус: ").strip().upper()

    valid_statuses = {"EXECUTED", "CANCELED", "PENDING"}
    while status not in valid_statuses:
        print(f"Программа: Статус операции \"{status}\" недоступен.")
        status = input("Пожалуйста, введите статус: ").strip().upper()

    print(f"Программа: Операции отфильтрованы по статусу \"{status}\"")
    filtered = filter_by_state(transactions, status)

    if not filtered:
        print("Программа: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    # Сортировка по дате
    sort_choice = input("Программа: Отсортировать операции по дате? Да/Нет\n").strip().lower()
    if sort_choice in ("да", "yes", "y", "д"):
        order = input("Программа: Отсортировать по возрастанию или по убыванию?\n").strip().lower()
        descending = order in ("по убыванию", "убыванию", "desc", "down", "у", "уб")
        filtered = sort_by_date(filtered, descending=descending)

    # Только рублёвые
    rub_only = input("Программа: Выводить только рублёвые транзакции? Да/Нет\n").strip().lower()
    if rub_only in ("да", "yes", "y", "д"):
        filtered = [
            t for t in filtered
            if t.get("operationAmount", {}).get("currency", {}).get("code") == "RUB"
        ]

    # Поиск по слову
    search_choice = input("Программа: Отфильтровать список транзакций по определённому слову в описании? Да/Нет\n").strip().lower()
    if search_choice in ("да", "yes", "y", "д"):
        word = input("Введите слово для поиска: ").strip()
        filtered = process_bank_search(filtered, word)

    # Статистика категорий
    categories = ["Перевод", "Оплата", "Открытие вклада", "Покупка"]  # можно сделать вводимыми
    category_counts = process_bank_operations(filtered, categories)
    print("\nПрограмма: Статистика по категориям:")
    for cat, count in category_counts.items():
        print(f"{cat}: {count} операций")

    # Вывод итогового списка
    print("\nПрограмма: Распечатываю итоговый список транзакций...")
    print(f"Всего банковских операций в выборке: {len(filtered)}")

    if not filtered:
        print("Программа: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    for op in filtered:
        date_str = op.get("date", "Неизвестно")
        description = op.get("description", "Операция")
        from_acc = op.get("from", "")
        amount = op.get("operationAmount", {}).get("amount", "Неизвестно")
        currency = op.get("operationAmount", {}).get("currency", {}).get("code", "???")

        try:
            masked = mask_account_card(f"{description} {from_acc}")
        except ValueError as e:
            masked = f"{description} {from_acc} (ошибка маскировки: {e})"

        date_formatted = get_date(date_str) if date_str != "Неизвестно" else date_str

        print(f"{date_formatted} {masked}")
        print(f"Сумма: {amount} {currency}")
        print("-" * 40)


if __name__ == "__main__":
    main()
