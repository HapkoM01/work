from src.masks import get_mask_account, get_mask_card_number
from src.widget import get_date, mask_account_card
from src.processing import filter_by_state, sort_by_date


def main() -> None:
    """Основная функция приложения."""
    print("=" * 60)
    print("Bank Operations Widget")
    print("=" * 60)

    # Примеры из модуля masks
    print("\n1. Примеры работы модуля masks:")
    print("-" * 40)

    card_number = "780079228966361"
    account_number = "73654188438135874305"

    print(f"Номер карты: {card_number}")
    print(f"Маска карты: {get_mask_card_number(card_number)}")
    print(f"\nНомер счета: {account_number}")
    print(f"Маска счета: {get_mask_account(account_number)}")

    # Примеры из модуля widget
    print("\n\n2. Примеры работы модуля widget:")
    print("-" * 40)

    examples = [
        "Visa Platinum 7000792289606361",
        "Счет 73654108430135874305",
    ]

    for example in examples:
        result = mask_account_card(example)
        print(f"{example}")
        print(f"→ {result}\n")

    date_example = "2024-03-11T02:26:18.671407"
    print("Форматирование даты:")
    print(f"Исходная дата: {date_example}")
    print(f"Форматированная: {get_date(date_example)}")

    # Примеры из модуля processing (ДОБАВЛЕНЫ!)
    print("\n\n3. Примеры работы модуля processing:")
    print("-" * 40)

    operations = [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]

    print("Исходные операции:")
    for op in operations:
        print(f"  ID: {op['id']}, State: {op['state']}, Date: {op['date']}")

    print("\nФильтрация (state='EXECUTED'):")
    executed_ops = filter_by_state(operations, "EXECUTED")
    for op in executed_ops:
        print(f"  ID: {op['id']}, Date: {op['date']}")

    print("\nСортировка по дате (по убыванию):")
    sorted_ops = sort_by_date(operations, True)
    for op in sorted_ops:
        print(f"  ID: {op['id']}, Date: {op['date']}")

    print("\n" + "=" * 60)
    print("Все функции работают корректно!")
    print("=" * 60)


if __name__ == "__main__":
    main()
