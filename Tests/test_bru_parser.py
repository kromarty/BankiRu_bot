from unittest import TestCase
from Logics.bru_parser import bru_parser
from bs4 import BeautifulSoup as BS
from datetime import datetime


class Testbru_parser(TestCase):
    def test_default_parse_get_usd_price(self):
        check = bru_parser('https://www.google.ru/')
        file = open('Tests/USD_SpB.html', 'r', encoding='utf-8')
        check.soup = BS(file, "html5lib")
        check.default_parse()
        self.assertEqual(check.cb, '70,52')
        self.assertEqual(check.buy, '70,65')
        self.assertEqual(check.sell, '70,81')
        self.assertEqual(check.for_n_currency, ' рублей за доллар США')
        self.assertEqual(check.bankname_for_buy, ' Плюс Банк - Кредитно-кассовый офис "Парк Победы"  ')
        self.assertEqual(check.bankname_for_sell, ' НЕЙВА БАНК - ККО "Санкт-Петербург"  ')
        self.assertTrue(check.best_price_found)
        file.close()

    def test_default_parse_get_usd_price(self):
        check = bru_parser('https://www.google.ru/')
        file = open('Tests/CNY_Ivanovo.html', 'r', encoding='utf-8')
        check.soup = BS(file, "html5lib")
        check.default_parse()
        self.assertEqual(check.cb, '99,80')
        self.assertIsNone(check.buy)
        self.assertIsNone(check.sell)
        self.assertEqual(check.for_n_currency, ' рублей за 10 китайских юаней')
        self.assertIsNone(check.bankname_for_buy)
        self.assertIsNone(check.bankname_for_sell)
        self.assertFalse(check.best_price_found)
        file.close()

    def test_date_parse_jpy(self):
        check = bru_parser('https://www.google.ru/')
        file = open('Tests/CB_date_parsing.html', 'r', encoding='utf-8')
        check.soup = BS(file, "html5lib")
        check.date_parse('JPY' ,datetime.strptime('01.01.1990', '%d.%m.%Y').date())
        self.assertEqual(check.date_parse('JPY' ,datetime.strptime('01.01.2020', '%d.%m.%Y').date()), "курс JPY на дату: 0.655176")
