import pytest
import allure
from pages.yandex_form_page import YandexFormPage

@allure.suite("Тестирование поиска Яндекс")
class TestYandexSearch:
    
    @allure.title("Тест поиска и проверки результатов")
    @allure.description("Этот тест проверяет функциональность поиска на Яндекс")
    @pytest.mark.parametrize("search_query,expected_text", [
        ("Selenium WebDriver", "Selenium"),
        ("Python автоматизация тестирования", "Python"),
        ("Тестирование программного обеспечения", "тестирование")
    ])
    def test_yandex_search_functionality(self, browser, base_url, search_query, expected_text):
        with allure.step(f"Открыть главную страницу Яндекс"):
            form_page = YandexFormPage(browser)
            form_page.open_page(base_url)
        
        with allure.step(f"Выполнить поиск запроса: {search_query}"):
            form_page.perform_search(search_query)
        
        with allure.step("Проверить наличие результатов поиска"):
            first_result = form_page.get_first_result_text()
            assert first_result is not None, "Результаты поиска не отобразились"
            assert expected_text.lower() in first_result.lower(), \
                f"Ожидаемый текст '{expected_text}' не найден в результате: '{first_result}'"
    
    @allure.title("Тест отображения подсказок при вводе")
    def test_suggest_display(self, browser, base_url):
        with allure.step("Открыть главную страницу Яндекс"):
            form_page = YandexFormPage(browser)
            form_page.open_page(base_url)
        
        with allure.step("Ввести текст в поисковую строку"):
            form_page.enter_search_text("автоматизация тестирования")
        
        with allure.step("Проверить отображение подсказок"):
            # Метод wait_for_suggest выбросит исключение если подсказки не появятся
            form_page.wait_for_suggest()
    
    @allure.title("Тест очистки поисковой строки")
    def test_search_input_clear(self, browser, base_url):
        with allure.step("Открыть главную страницу Яндекс"):
            form_page = YandexFormPage(browser)
            form_page.open_page(base_url)
        
        with allure.step("Ввести текст и очистить поле"):
            form_page.enter_search_text("текст для очистки")
            
            # Получить элемент и очистить его
            search_input = browser.find_element(*form_page.SEARCH_INPUT)
            search_input.clear()
            
            value_after_clear = search_input.get_attribute('value')
        
        with allure.step("Проверить что поле очищено"):
            assert value_after_clear == '', f"Поле не очищено, значение: '{value_after_clear}'"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
