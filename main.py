from src.masks import get_mask_card_number, get_mask_account


def main() -> None:
    """Основная функция приложения."""
    # Примеры использования
    card_number = "780079228966361"
    account_number = "73654188438135874305"

    print("Примеры работы функций:")
    print(f"Номер карты: {card_number}")
    print(f"Маска карты: {get_mask_card_number(card_number)}")
    print()
    print(f"Номер счета: {account_number}")
    print(f"Маска счета: {get_mask_account(account_number)}")


if __name__ == "__main__":
    main()
