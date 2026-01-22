# Проект HomeWork - Bank operations

## Описание проекта

Проект представляет собой виджет для обработки банковских операций клиента.
Реализованы функции фильтрации операций по статусу и сортировки по дате.


## Цель проекта

Создание удобного инструмента для работы с данными банковских операций, включая:

- Маскировку номеров карт и счетов
- Фильтрацию операций по статусу
- Сортировку операций по дате
- Форматирование данных для отображения

# Функционал проекта.

## Модуль masks

Содержит функции для наложения масок на конфиденциальные данные:

**get_mask_card_number(card_number: str) -> str**

Маскирует номер банковской карты в формате: XXXX XX** **** XXXX
Пример: 7000792289606361 → 7000 79** **** 6361

**get_mask_account(account_number: str) -> str**

Маскирует номер счета в формате: **XXXX
**Пример:** 73654108430135874305 → **4305

## Модуль widget

Содержит функции для работы с банковскими данными:

**mask_account_card(card_or_account_data: str) -> str**

Автоматически определяет тип данных (карта или счет) и применяет соответствующую маску.
**Пример для карты:** Visa Platinum 7000792289606361 → Visa Platinum 7000 79** **** 6361
**Пример для счета:** Счет 73654108430135874305 → Счет **4305

**get_date(data_info: str) -> str**
Функция берёт данные даты и времени в формате "2024-03-11T02:26:18.671407"
и возвращает только дату в формате 'ДД.ММ.ГГГГ'"""

## Модуль processing

Модуль processing предоставляет функции для фильтрации и сортировки банковских операций.

**filter_by_state(operations: list, state: str = 'EXECUTED') -> list**
Фильтрует список операций по статусу выполнения.

## Модуль generators

Новый модуль для работы с генераторами транзакций.

### Функции:

#### `filter_by_currency(transactions, currency_code)`

Фильтрует транзакции по коду валюты и возвращает итератор.

from src.generators import filter_by_currency

transactions = [...]  # список транзакций
usd_transactions = filter_by_currency(transactions, "USD")

**Пример:** usd_transactions = filter_by_currency(transactions, "USD")
for transaction in usd_transactions:
    print(transaction["id"])

#### `transaction_descriptions(transactions)`

Генератор, который возвращает описания транзакций.

**Пример:** descriptions = transaction_descriptions(transactions)
for description in descriptions:
    print(description)

# Получение первых двух транзакций
for _ in range(2):
    print(next(usd_transactions))

#### `card_number_generator(start, stop)`

Генератор номеров банковских карт в заданном диапазоне.

**Пример:** for card in card_number_generator(1, 5):
    print(card)
# Вывод:
# 0000 0000 0000 0001
# 0000 0000 0000 0002
# 0000 0000 0000 0003
# 0000 0000 0000 0004

## Покрытие тестами

Отчёт о покрытии сгенерирован с помощью pytest-cov.

- Общий процент покрытия: [посмотри в htmlcov/index.html → процент вверху]
- Полный HTML-отчёт: [htmlcov/index.html](htmlcov/index.html)

Чтобы открыть отчёт:
1. Скачай репозиторий
2. Открой файл `htmlcov/index.html` в браузере
   
## Тестирование

Проект использует `pytest` для тестирования.

### Запуск тестов

```bash
# Запуск всех тестов
poetry run pytest

# Запуск с детальным выводом
poetry run pytest -v

# Запуск конкретного модуля
poetry run pytest tests/test_masks_pytest.py -v

# Запуск с покрытием кода
poetry run pytest --cov=src --cov-report=html

## Установка:

1. Клонируйте репозиторий:

```
git@github.com:HapkoM01/work.git
```

2. Установите зависимости:

```
pip install -r requirements.txt
poetry init
poetry add requests
```

## Использование:

1. Перейдите на страницу в вашем веб-браузере.
2. Создайте новую учетную запись или войдите существующей.
3. Создайте новую запись в блоге или оставьте комментарий к существующей.

## Код написал:

HapkoM - Beginner Python-developer
