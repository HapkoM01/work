from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(account_info: str) -> str:
    """
    Маскирует номер карты или счета в строке с названием.

    Args:
        account_info: Строка формата "Visa Platinum 7000792289606361"
                     или "Счет 73654108430135874305"

    Returns:
        Строка с замаскированным номером

    Examples:
        >>> mask_account_card("Visa Platinum 7000792289606361")
        'Visa Platinum 7000 79** **** 6361'
        >>> mask_account_card("Счет 73654108430135874305")
        'Счет **4305'
    """
    # Разделяем строку на название и номер
    parts = account_info.split()

    if len(parts) < 2:
        raise ValueError("Строка должна содержать название и номер")

    # Название - все части кроме последней
    name = " ".join(parts[:-1])
    number = parts[-1]

    # Определяем тип по названию
    if name.lower() == "счет":
        # Используем функцию маскировки счета
        masked_number = get_mask_account(number)
    else:
        # Используем функцию маскировки карты
        masked_number = get_mask_card_number(number)

    return f"{name} {masked_number}"


def get_date(date_string: str) -> str:
    """
    Преобразует дату из формата ISO в формат ДД.ММ.ГГГГ.

    Args:
        date_string: Дата в формате "2024-03-11T02:26:18.671407"

    Returns:
        Дата в формате "11.03.2024"

    Examples:
        >>> get_date("2024-03-11T02:26:18.671407")
        '11.03.2024'
    """
    # Разделяем строку по 'T' и берем первую часть (дату)
    date_part = date_string.split("T")[0]

    # Разделяем дату на год, месяц и день
    year, month, day = date_part.split("-")

    # Форматируем в нужный формат
    return f"{day}.{month}.{year}"


if __name__ == "__main__":
    # Примеры использования
    examples = [
        "Visa Platinum 7000792289606361",
        "Maestro 1596837868705199",
        "Счет 64686473678894779589",
        "MasterCard 7158300734726758",
        "Счет 35383833474447895560",
        "Visa Classic 6831982476737658",
        "Visa Platinum 8990922113665229",
        "Visa Gold 5999414228426353",
        "Счет 73654108430135874305",
    ]

    print("Примеры работы функции mask_account_card:")
    for example in examples:
        try:
            result = mask_account_card(example)
            print(f"{example} -> {result}")
        except ValueError as e:
            print(f"Ошибка для '{example}': {e}")

    print("\nПример работы функции get_date:")
    date_example = "2024-03-11T02:26:18.671407"
    print(f"{date_example} -> {get_date(date_example)}")
