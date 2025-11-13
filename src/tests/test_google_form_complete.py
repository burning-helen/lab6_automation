import pytest
import allure
from pages.google_form_page import GoogleFormPage

@allure.suite("Комплексное тестирование Google Forms")
class TestGoogleFormComplete:
    
    FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLScuix7YuaE4-I0HPF_AE9zQ6nGysuxeCcM09qJf8IFyzHbKJA/viewform?usp=sharing&ouid=111699329858962831138"
    
    @allure.title("Полный тест отправки Google Form")
    @allure.description("Комплексная проверка заполнения и отправки формы")
    def test_complete_google_form_submission(self, browser):
        form_page = GoogleFormPage(browser)
        
        # Шаг 1: Открытие формы
        with allure.step("1. Открыть форму Google"):
            form_page.open_form(self.FORM_URL)
            browser.save_screenshot("1_form_opened.png")
        
        # Шаг 2: Диагностика начального состояния
        with allure.step("2. Диагностика формы"):
            form_page.debug_form_state()
        
        # Шаг 3: Заполнение формы
        with allure.step("3. Заполнить все поля формы"):
            form_page.fill_complete_form(
                name="Иван Тестовый",
                email="ivan.test@example.com",
                address="Москва, Красная площадь, 1",
                phone="+79991234567",
                comments="Автоматическое тестирование формы с помощью Selenium"
            )
            browser.save_screenshot("2_form_filled.png")
        
        # Шаг 4: Проверка заполнения
        with allure.step("4. Проверить заполнение полей"):
            form_page.debug_form_state()
        
        # Шаг 5: Попытка отправки
        with allure.step("5. Отправить форму"):
            submission_success = form_page.try_all_submit_methods()
            
            if submission_success:
                allure.attach("Форма отправлена", "Отправка прошла успешно")
            else:
                allure.attach("Не удалось отправить", "Все методы отправки не сработали")
                pytest.fail("Не удалось отправить форму ни одним из методов")
        
        # Шаг 6: Проверка результата
        with allure.step("6. Проверить результат отправки"):
            is_success = form_page.verify_submission_success()
            
            assert is_success, "Форма не была успешно отправлена"
            
        with allure.step("7. Финальная диагностика"):
            form_page.debug_form_state()
            
        allure.attach("Тест завершен", "Все шаги выполнены успешно")

    @allure.title("Быстрый тест отправки формы")
    def test_quick_form_submission(self, browser):
        """Упрощенный тест для быстрой проверки"""
        form_page = GoogleFormPage(browser)
        
        form_page.open_form(self.FORM_URL)
        form_page.fill_complete_form(
            name="Быстрый тест",
            email="quick@test.com", 
            address="Быстрый адрес"
        )
        
        # Пробуем отправить
        if form_page.try_all_submit_methods():
            assert form_page.verify_submission_success(), "Быстрая отправка не удалась"
        else:
            pytest.fail("Не удалось отправить форму в быстром тесте")