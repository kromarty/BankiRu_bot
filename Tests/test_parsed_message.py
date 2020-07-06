from unittest import TestCase
from Logics import parsed_message
from datetime import datetime

class Testparsed_message(TestCase):
    def test_parse_dollar_and_city(self):
        message = 'Курс доллара в вологде'
        message = message.lower()
        check = parsed_message.parsed_message(message)
        check.parse()
        self.assertTrue(check.trigger)
        self.assertEqual(check.currency, 'USD')
        self.assertIsNone(check.date)
        self.assertEqual(check.location, 'Вологда')

    def test_parse_yuan_with_default_city(self):
        message = 'Почём сейчас китайский юань?'
        message = message.lower()
        check = parsed_message.parsed_message(message)
        check.parse()
        self.assertTrue(check.trigger)
        self.assertEqual(check.currency, 'CNY')
        self.assertIsNone(check.date)
        self.assertEqual(check.location, 'Вологда')

    def test_parse_all_currencies_and_city(self):
        message = "Какой курс в Иваново?"
        message= message.lower()
        check = parsed_message.parsed_message(message)
        check.parse()
        self.assertTrue(check.trigger)
        self.assertEqual(check.currency, 'all')
        self.assertIsNone(check.date)
        self.assertEqual(check.location, 'Иваново')

    def test_parse_all_currencies_with_default_city(self):
        message = "Какой курс на сегодня?"
        message = message.lower()
        check = parsed_message.parsed_message(message)
        check.parse()
        self.assertTrue(check.trigger)
        self.assertEqual(check.currency, 'all')
        self.assertIsNone(check.date)
        self.assertEqual(check.location, 'Иваново')
    def test_parse_euro_and_date(self):
        message = 'Какой был курс евро на 01.05.2016'
        message = message.lower()
        check = parsed_message.parsed_message(message)
        check.parse()
        self.assertTrue(check.trigger)
        self.assertEqual(check.currency, 'EUR')
        self.assertEqual(check.date, datetime.strptime('01.05.2016', '%d.%m.%Y').date())
        self.assertTrue(check.date_search)

    def test_parse_all_currencies_and_date(self):
        message = 'Какой был курс на 01.05.2016'
        message = message.lower()
        check = parsed_message.parsed_message(message)
        check.parse()
        self.assertTrue(check.trigger)
        self.assertEqual(check.currency, 'all')
        self.assertEqual(check.date, datetime.strptime('01.05.2016', '%d.%m.%Y').date())
        self.assertTrue(check.date_search)