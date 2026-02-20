import json
from pathlib import Path

from src.utils import get_financial_transactions
from src.readers import read_csv_transactions, read_excel_transactions
from src.processing import filter_by_state, sort_by_date
from src.search import process_bank_search, process_bank_operations
from src.widget import mask_account_card, get_date


def main():
    print("Программа: Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Меню:")
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

    # Чтение данных в зависимости от выбора
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
    print("Доступные статусы: EXECUTED, CANCELED, PENDING")
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

    # Дополнительные фильтры
    sort_choice = input("Программа: Отсортировать операции по дате? Да/Нет\n").strip().lower()
    if sort_choice in ("да", "yes", "y"):
        order = input("Программа: Отсортировать по возрастанию или по убыванию?\n").strip().lower()
        descending = order in ("по убыванию", "убыванию", "desc", "down")
        filtered = sort_by_date(filtered, descending=descending)

    rub_only = input("Программа: Выводить только рублёвые транзакции? Да/Нет\n").strip().lower()
    if rub_only in ("да", "yes", "y"):
        filtered = [t for t in filtered if t.get("operationAmount", {}).get("currency", {}).get("code") == "RUB"]

    search_word = input("Программа: Отфильтровать список транзакций по определённому слову в описании? Да/Нет\n").strip().lower()
    if search_word in ("да", "yes", "y"):
        word = input("Введите слово для поиска: ").strip()
        filtered = process_bank_search(filtered, word)

    # Подсчёт категорий
    categories = ["Перевод", "Оплата", "Открытие вклада", "Покупка"]  # можно сделать вводимыми
    category_counts = process_bank_operations(filtered, categories)
    print("\nПрограмма: Статистика по категориям:")
    for cat, count in category_counts.items():
        print(f"{cat}: {count} операций")

    # Вывод результата
    print("\nПрограмма: Распечатываю итоговый список транзакций...")
    print(f"Всего банковских операций в выборке: {len(filtered)}")

    for op in filtered:
        masked_card = mask_account_card(f"{op.get('description', 'Операция')} {op.get('from', '')}")
        date_formatted = get_date(op.get("date", ""))
        amount = op["operationAmount"]["amount"]
        currency = op["operationAmount"]["currency"]["code"]
        print(f"{date_formatted} {masked_card}")
        print(f"Сумма: {amount} {currency}")
        print("-" * 40)


if __name__ == "__main__":
    main()
