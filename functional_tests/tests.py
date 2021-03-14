import time

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys


MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):
    '''Тест нового пользователя'''

    def setUp(self):
        '''Установка'''
        self.browser = webdriver.Firefox()

    def tearDown(self):
        '''Демонтаж'''
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        '''ожидать строку в таблице списка'''
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_for_one_user(self):
        '''тест: можно начать список для одного пользователя'''

        # Посещение домашней страницы приложения
        self.browser.get(self.live_server_url)

        # Видим, что заголовок и шапка страницы говорят о to-do-list
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # Предложение ввести элемент списка
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Введите задание в to-do лист'
        )
        # Ввод в текстовом поле "simple test request"
        inputbox.send_keys('simple test request')

        # При нажатии enter страница обновляется и теперь она содержит "simple test request" в качестве элемента списка
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: simple test request')

        # Текстовое поле по-прежнему приглашает добавить еще один элемент. Ввод "another test request"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('another test request')
        inputbox.send_keys(Keys.ENTER)

        # Страница обновляется и теперь показывает оба элемента списка
        self.wait_for_row_in_list_table('2: another test request')
        self.wait_for_row_in_list_table('1: simple test request')
    
    
    def test_multiple_user_can_start_lists_at_different_urls(self):
        '''тест: многочисленные пользователи могут начать списки по разным url'''
        # Начинаем новый список
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('simple test request')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: simple test request')

        # Видим, что список имеет унимальный url
        user_list_url = self.browser.current_url
        self.assertRegex(user_list_url, 'lists/.+')

        # Другой пользователь (ВТОРОЙ) заходит на сайт

        ## Мы используем новый сеанс браузера, тем самым обеспечивая, чтобы никакая
        ## информация от ПЕРВОГО пользователя не прошла через данные куки и прочие.
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # ВТОРОЙ посещает домашнюю страницу. Нет никаких признаков списка ПЕРВОГО
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('simple test request', page_text)
        self.assertNotIn('another test request', page_text)

        # ВТОРОЙ начинает новый список, вводя новый элемент
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('find mind')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: find mind')

        # ВТОРОЙ получает уникальный url
        second_user_list_url = self.browser.current_url
        self.assertRegex(second_user_list_url, 'lists/.+')
        self.assertNotEqual(second_user_list_url, user_list_url)

        # Проверяем следы первого пользователя
        page_text = self.browser.find_element_by_name('body').text
        self.assertNotIn('simple test request', page_text)
        self.assertIn('find mind', page_text)

        # Сеанс закончен

        self.fail('Закончить тест')
 
