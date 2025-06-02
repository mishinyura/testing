В этом проекте мы потренируемся в mutation testing, создавая unit-тесты
для модуля расчёта платежей.

Ниже необходимо описать какие действия или стратегия доработок были выбраны во время выполнения задания

# Структура
Внес правки в Makefile, добавил путь к команде ```mutmut run --paths-to-mutate=billing```

# Тесты
Исправлены тесты:
- TestComputeBulkTotal.test_discount_compare
- TestValidateTaxNumber.test_valid
- TestRoundMoney.test_one_decimal

В тест TestApplyLoyaltyDiscount добавил:
- Позитивный кейс
- Кейс, когда discount больше gross
- Кейс, когда points == 0
- Кейс с нулевой ценой

В тест TestRoundMoney добавил
- Округления вниз и вверх
- Разных значений decimals

Исправил и добавил в TestIsWeekendRate:
- На будний и выходной день

Добавил в TestConvertCurrency:
- Тест, который явно проверяет правильный курс конвертации USD и EUR
- Правки в test_unknown_currency

Добавил в TestApplyCoupon:
- Тест, который проверяет, что скидка по купону "NEWUSER5" работает корректно
- Проверку скидки 25% по купону BLACKFRIDAY и кейс нижним регистром
- Тест, где купон не указан или равен None

Добаивл в TestPriceWithTax:
- Проверку на корректность текста ошибка
- Исправил test_negative_raises

Добавил в TestComputeTotal:
- Проверку без купона
- Проверку, что купон тоже применяется

# Результат
Coverage: 100%
Mutation Score: 86%

Сохранить пришлось в mut.txt потому что в json не перенаправляет, пробовал обновить mutmut, но безуспешно