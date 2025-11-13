from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import allure
import time

class GoogleFormPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)
    
    # Локаторы полей
    TEXT_INPUTS = (By.CSS_SELECTOR, "input[jsname='YPqjbf'][type='text']")
    TEXTAREAS = (By.CSS_SELECTOR, "textarea[jsname='YPqjbf']")
    
    @allure.step("Открыть Google Form")
    def open_form(self, url):
        self.driver.get(url)
        time.sleep(2)
        return self
    
    @allure.step("Заполнить поле Name: {name}")
    def fill_name(self, name):
        inputs = self.wait.until(EC.presence_of_all_elements_located(self.TEXT_INPUTS))
        if len(inputs) > 0:
            inputs[0].clear()
            inputs[0].send_keys(name)
        return self
    
    @allure.step("Заполнить поле Email: {email}")
    def fill_email(self, email):
        inputs = self.driver.find_elements(*self.TEXT_INPUTS)
        if len(inputs) > 1:
            inputs[1].clear()
            inputs[1].send_keys(email)
        return self
    
    @allure.step("Заполнить поле Address: {address}")
    def fill_address(self, address):
        textareas = self.driver.find_elements(*self.TEXTAREAS)
        if len(textareas) > 0:
            textareas[0].clear()
            textareas[0].send_keys(address)
        return self
    
    @allure.step("Заполнить поле Phone: {phone}")
    def fill_phone(self, phone):
        inputs = self.driver.find_elements(*self.TEXT_INPUTS)
        if len(inputs) > 2:
            inputs[2].clear()
            inputs[2].send_keys(phone)
        return self
    
    @allure.step("Заполнить поле Comments: {comments}")
    def fill_comments(self, comments):
        textareas = self.driver.find_elements(*self.TEXTAREAS)
        if len(textareas) > 1:
            textareas[1].clear()
            textareas[1].send_keys(comments)
        return self
    
    @allure.step("Заполнить всю форму")
    def fill_complete_form(self, name, email, address, phone="", comments=""):
        (self.fill_name(name)
         .fill_email(email)
         .fill_address(address)
         .fill_phone(phone)
         .fill_comments(comments))
        return self
    
    @allure.step("Найти и проанализировать кнопку Submit")
    def analyze_submit_button(self):
        """Анализирует все возможные кнопки отправки"""
        print("\n=== АНАЛИЗ КНОПКИ SUBMIT ===")
        
        # Все возможные локаторы кнопки
        button_locators = [
            ("XPATH Submit текст", By.XPATH, "//span[text()='Submit']"),
            ("XPATH Отправить текст", By.XPATH, "//span[text()='Отправить']"),
            ("CSS button", By.CSS_SELECTOR, "button[type='submit']"),
            ("CSS div button", By.CSS_SELECTOR, "div[role='button']"),
            ("XPATH любой элемент с Submit", By.XPATH, "//*[contains(text(), 'Submit')]"),
            ("XPATH любой элемент с Отправить", By.XPATH, "//*[contains(text(), 'Отправить')]"),
        ]
        
        found_buttons = []
        
        for name, by, locator in button_locators:
            try:
                elements = self.driver.find_elements(by, locator)
                for i, element in enumerate(elements):
                    if element.is_displayed():
                        button_info = {
                            'name': f"{name} #{i}",
                            'element': element,
                            'text': element.text,
                            'location': element.location,
                            'size': element.size,
                            'enabled': element.is_enabled(),
                            'displayed': element.is_displayed(),
                            'tag': element.tag_name
                        }
                        found_buttons.append(button_info)
                        print(f"✅ Найдена: {button_info}")
            except Exception as e:
                print(f"❌ {name}: {e}")
        
        return found_buttons
    
    @allure.step("Попробовать все способы нажатия кнопки")
    def try_all_submit_methods(self):
        """Пробует все возможные способы отправки формы"""
        
        buttons = self.analyze_submit_button()
        
        if not buttons:
            print("❌ Не найдено ни одной подходящей кнопки!")
            return False
        
        # Сохраним скриншот перед попыткой отправки
        self.driver.save_screenshot("before_submit_attempts.png")
        
        # Метод 1: Обычный click
        print("\n=== МЕТОД 1: ОБЫЧНЫЙ CLICK ===")
        for button in buttons:
            try:
                print(f"Пробуем нажать: {button['name']}")
                button['element'].click()
                print("✅ Успешно!")
                time.sleep(3)
                return True
            except Exception as e:
                print(f"❌ Ошибка: {e}")
        
        # Метод 2: JavaScript click
        print("\n=== МЕТОД 2: JAVASCRIPT CLICK ===")
        for button in buttons:
            try:
                print(f"Пробуем JS click: {button['name']}")
                self.driver.execute_script("arguments[0].click();", button['element'])
                print("✅ Успешно!")
                time.sleep(3)
                return True
            except Exception as e:
                print(f"❌ Ошибка: {e}")
        
        # Метод 3: ActionChains
        print("\n=== МЕТОД 3: ACTIONCHAINS ===")
        for button in buttons:
            try:
                print(f"Пробуем ActionChains: {button['name']}")
                actions = ActionChains(self.driver)
                actions.move_to_element(button['element']).click().perform()
                print("✅ Успешно!")
                time.sleep(3)
                return True
            except Exception as e:
                print(f"❌ Ошибка: {e}")
        
        # Метод 4: Enter в последнем поле
        print("\n=== МЕТОД 4: ENTER В ПОЛЕ ===")
        try:
            textareas = self.driver.find_elements(*self.TEXTAREAS)
            if textareas:
                last_field = textareas[-1]
                last_field.send_keys(Keys.ENTER)
                print("✅ Enter отправлен!")
                time.sleep(3)
                return True
        except Exception as e:
            print(f"❌ Ошибка: {e}")
        
        return False
    
    @allure.step("Проверить успешность отправки формы")
    def verify_submission_success(self):
        """Проверяет, была ли форма успешно отправлена"""
        
        time.sleep(3)  # Ждем возможного редиректа
        
        current_url = self.driver.current_url
        page_source = self.driver.page_source.lower()
        
        print(f"\n=== ПРОВЕРКА ОТПРАВКИ ===")
        print(f"Текущий URL: {current_url}")
        
        # Признаки успешной отправки
        success_indicators = [
            "formresponse" in current_url,
            "thankyou" in current_url,
            "спасибо" in page_source,
            "your response has been recorded" in page_source,
            "ответ записан" in page_source,
        ]
        
        if any(success_indicators):
            print("✅ Форма успешно отправлена!")
            self.driver.save_screenshot("success_submission.png")
            return True
        else:
            print("❌ Форма не была отправлена")
            self.driver.save_screenshot("failed_submission.png")
            return False
    
    @allure.step("Полная проверка формы")
    def debug_form_state(self):
        """Выводит полную отладочную информацию о форме"""
        print("\n" + "="*50)
        print("ПОЛНАЯ ДИАГНОСТИКА ФОРМЫ")
        print("="*50)
        
        # Информация о полях
        inputs = self.driver.find_elements(*self.TEXT_INPUTS)
        textareas = self.driver.find_elements(*self.TEXTAREAS)
        
        print(f"\nПОЛЯ ВВОДА:")
        print(f"Текстовые поля: {len(inputs)}")
        print(f"Многострочные поля: {len(textareas)}")
        
        for i, inp in enumerate(inputs):
            value = inp.get_attribute('value')
            print(f"  Input {i}: '{value}'")
        
        for i, ta in enumerate(textareas):
            value = ta.get_attribute('value')
            print(f"  Textarea {i}: '{value}'")
        
        # Анализ кнопок
        self.analyze_submit_button()
        
        # Информация о странице
        print(f"\nИНФОРМАЦИЯ О СТРАНИЦЕ:")
        print(f"URL: {self.driver.current_url}")
        print(f"Заголовок: {self.driver.title}")