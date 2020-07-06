from Logics import currency, cities
import logging
import re
from datetime import datetime

default_region = "Москва"


class parsed_message:
    """Парсер сообщений. Ищет упоминания о валюте, городе или дате."""

    def __init__(self, message):
        """Конструктор

        :param message: сообщение в нижнем регистре, в котором ищем ключевые слова.
        """
        self.message = message.lower()
        self.currency = "all"
        self.location = default_region
        self.date_search = False
        self.date = None
        self.trigger = False
        self.region_found = False

    def parse(self):
        """Функция поиска ключевых слов/фраз."""
        cnt = 0
        for curr in currency.currency:
            if any(x in self.message for x in currency.currency[curr]):
                self.currency = curr
                cnt = cnt + 1
                logging.info("Currency detected: %s" % curr)
        current_date = re.search(r'(0?[1-9]|[12][0-9]|3[01])([\.\\\/-])(0?[1-9]|1[012])\2(((19|20)\d\d)|(\d\d))',
                                 self.message)
        if current_date is None:
            self.date_search = False
            logging.info("No date detected")
        else:
            try:
                self.date_search = True
                self.date = datetime.strptime(current_date.group(0), '%d.%m.%Y').date()
                cnt = cnt + 1
                logging.info("Date detected: %s, further search goes by date" % (current_date.group(0)))
            except Exception:
                self.date_search = False
                logging.info("No date detected")
        for region in cities.regions:
            for name in cities.regions[str(region)]:
                if self.message.find(name) != -1:
                    global default_region
                    default_region = region
                    self.region_found = True
                    self.location = region
                    cnt = cnt + 1
                    logging.info("Region match: %s => %s" % (name, region))
        if self.message.find('курс') != -1:
            cnt = cnt + 1
            logging.info("Search for the exchange rate of all currencies in the region")
        if cnt > 1:
            self.trigger = True