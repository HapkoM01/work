def get_mask_card_number(card_number: str) -> str:
    """
    Возвращает маску номера банковской карты.

    Args:
        card_number: Номер карты в виде строки

    Returns:
        Маска номера карты в формате XXXX XX** XXXX

    Examples:
        >>> get_mask_card_number("780079228966361")
        '7800 79** **** 6361'
    """
    # Убираем пробелы и другие символы
    clean_number = "".join(filter(str.isdigit, card_number))

    # Проверяем длину номера
    if len(clean_number) < 10:  # 6 (первые видимые) + 4 (последние видимые)
        raise ValueError("Номер карты должен содержать минимум 10 цифр")

    # Берем первые 6 цифр и последние 4
    first_six = clean_number[:6]
    last_four = clean_number[-4:]

    # Собираем маску согласно примеру: XXXX XX** XXXX
    result = f"{first_six[:4]} {first_six[4:]}** **** {last_four}"

    return result


def get_mask_account(account_number: str) -> str:
    """
    Возвращает маску номера банковского счета.

    Args:
        account_number: Номер счета в виде строки

    Returns:
        Маска номера счета в формате **XXXX

    Examples:
        >>> get_mask_account("73654188438135874305")
        '**4305'
    """
    # Убираем пробелы и другие символы
    clean_number = "".join(filter(str.isdigit, account_number))

    # Проверяем длину номера
    if len(clean_number) < 4:
        raise ValueError("Номер счета должен содержать минимум 4 цифры")

    # Возвращаем маску
    return f"**{clean_number[-4:]}"


if __name__ == "__main__":
    # Примеры использования
    print("Маска карты:", get_mask_card_number("780079228966361"))
    print("Маска счета:", get_mask_account("73654188438135874305"))
