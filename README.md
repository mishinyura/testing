В этом проекте мы потренируемся в mutation testing, создавая unit-тесты
для модуля расчёта платежей.

Ниже необходимо описать какие действия или стратегия доработок были выбраны во время выполнения задания

# Зависимости
Обновил зависимости ```pip install --upgrade mutmut pony``` так как есть конфликт версий 

# Тесты
Исправлены тесты:
- TestComputeBulkTotal.test_discount_compare
- TestValidateTaxNumber.test_valid
- TestRoundMoney.test_one_decimal

# Структура
Внес правки в Makefile, добавил путь к команде ```mutmut run --paths-to-mutate=billing```