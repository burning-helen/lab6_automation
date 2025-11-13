# lab6_automation
Лабораторная работа №6: Автоматизация тестирования веб-форм с использованием Selenium WebDriver
## Описание проекта
Автоматизированные тесты для проверки функциональности поиска на сайте Яндекс с использованием Selenium WebDriver и паттерна Page Object Model.

## Технологический стек
- Python 3.8+
- Selenium WebDriver
- pytest
- Allure Framework
- Page Object Pattern

## Установка зависимостей
pip install -r requirements.txt
Запуск тестов
# Обычный запуск
pytest tests/test_yandex_form.py -v

# Параллельный запуск
pytest tests/test_yandex_form.py -n 2 -v

# С генерацией Allure отчетов
pytest --alluredir=allure-results
allure serve allure-results
Структура проекта
lab6_automation/
├── pages/           # Page Object классы
├── tests/           # Тестовые сценарии
├── conftest.py      # Конфигурация pytest
└── requirements.txt # Зависимости проекта
