import time

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(LiveServerTestCase):
    '''Тест нового пользователя'''

    def setUp(self):
        '''Установка'''
        self.browser = webdriver.Firefox()

    def tearDown(self):
        '''Демонтаж'''
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        '''подтверждение строки в таблице списка'''
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        '''тест: можно ли начать список и получить его позже'''

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
        time.sleep(1)
        self.check_for_row_in_list_table('1: simple test request')

        # Текстовое поле по-прежнему приглашает добавить еще один элемент. Ввод "another test request"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('another test request')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # Страница обновляется и теперь показывает оба элемента списка
        self.check_for_row_in_list_table('1: simple test request')
        self.check_for_row_in_list_table('2: another test request')
        # Проверяем сохранил ли сайт этот список. Видим, что сайт сгенерировал уникальный  url-адрес - об этом выводится
        # небольшой текст с объяснениями
        self.fail('Закончить тест')
        # Заходим на данный url и видим, что список по-прежнему там