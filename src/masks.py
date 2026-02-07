import logging

from .logging_config import setup_module_logger

logger = setup_module_logger("masks", level=logging.DEBUG)


def get_mask_card_number(card_number: str) -> str:
    logger.debug(f"Начало маскирования номера карты: {card_number[:6]}...")

    clean_number = "".join(filter(str.isdigit, card_number))

    if len(clean_number) < 10:
        logger.error(f"Слишком короткий номер карты: {len(clean_number)} цифр")
        raise ValueError("Номер карты должен содержать минимум 10 цифр")

    first_six = clean_number[:6]
    last_four = clean_number[-4:]
    masked = f"{first_six[:4]} {first_six[4:]}** **** {last_four}"

    logger.info(f"Успешно замаскирован номер карты → {masked}")
    return masked


def get_mask_account(account_number: str) -> str:
    logger.debug(f"Маскирование номера счёта: ...{account_number[-6:]}")

    clean_number = "".join(filter(str.isdigit, account_number))

    if len(clean_number) < 4:
        logger.error(f"Слишком короткий номер счёта: {len(clean_number)} цифр")
        raise ValueError("Номер счета должен содержать минимум 4 цифры")

    masked = f"**{clean_number[-4:]}"
    logger.info(f"Успешно замаскирован номер счёта → {masked}")
    return masked
