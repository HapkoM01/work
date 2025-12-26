from src.masks import get_mask_card_number, get_mask_account
from src.widget import mask_account_card, get_date


def main() -> None:
    """Основная функция приложения."""
    print("=== Примеры работы из модуля masks ===")

    # Примеры из модуля masks
    card_number = "780079228966361"
    account_number = "73654188438135874305"

    print(f"\nНомер карты: {card_number}")
    print(f"Маска карты: {get_mask_card_number(card_number)}")
    print(f"\nНомер счета: {account_number}")
    print(f"Маска счета: {get_mask_account(account_number)}")

    print("\n=== Примеры работы из модуля widget ===")

    # Примеры для функции mask_account_card
    examples = [
        "Visa Platinum 7000792289606361",
        "Maestro 1596837868705199",
        "Счет 64686473678894779589",
        "MasterCard 7158300734726758",
        "Счет 35383833474447895560",
    ]

    print("\nМаскирование карт и счетов:")
    for example in examples[:3]:  # Показываем первые 3 примера
        result = mask_account_card(example)
        print(f"  {example}")
        print(f"  -> {result}\n")

    # Пример для функции get_date
    print("Форматирование даты:")
    date_example = "2024-03-11T02:26:18.671407"
    print(f"  {date_example}")
    print(f"  -> {get_date(date_example)}")


if __name__ == "__main__":
    main()
