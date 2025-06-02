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
- тест, который явно проверяет правильный курс конвертации USD и EUR

Добавил в TestApplyCoupon:
- тест, который проверяет, что скидка по купону "NEWUSER5" работает корректно

Добаивл в TestPriceWithTax:
-Проверку на корректность текста ошибка

# Результат
Coverage: 86%
Mutation Score