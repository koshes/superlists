from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):
    '''Тест нового пользователя'''

    def setUp(self):
        '''Установка'''
        self.browser = webdriver.Firefox()

    def tearDown(self):
        '''Демонтаж'''
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        '''тест: можно ли начать список и получить его позже'''

        # Посещение домашней страницы приложения
        self.browser.get('http://localhost:8000')

        # Видим, что заголовок и шапка страницы говорят о to-do-list
        self.assertIn('To-Do', self.browser.title)
        self.fail('Закончить тест')

        # Предложение ввести элемент списка

        # Ввод в текстовом поле "simple test request"

        # При подтверждении страница обновляется и теперь она содержит "simple test request" в качестве элемента списка

        # Текстовое поле по-прежнему приглашает добавить еще один элемент. Ввод "another test request"

        # Страница обновляется и теперь показывает оба элемента списка

        # Проверяем сохранил ли сайт этот список. Видим, что сайт сгенерировал уникальный  url-адрес - об этом выводится
        # небольшой текст с объяснениями

        # Заходим на данный url и видим, что список по-прежнему там


if __name__ =='__main__':
    unittest.main(warnings='ignore')