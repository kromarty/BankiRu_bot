import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging
import html5lib

class bru_parser:
    """Парсер сайта banki.ru"""
    def __init__(self, link):
        """Конструктор.
        :param link: ссылка на страницу.
        """
        self.link = link
        self.best_price_found = None
        self.sell = None
        self.buy = None
        self.cb = None
        self.bankname_for_sell = None
        self.bankname_for_buy = None
        self.for_n_currency = None
        self.soup = None

    def default_parse(self):
        """Поиск информации о валюте в городе.
        :returns: сообщение с курсом валюты в регионе
        """
        s = requests.session()
        logging.info("Opening %s" % self.link)
        # noinspection PyBroadException
        try:
            con = s.get(self.link)
        except BaseException:
            logging.error("Failed to open %s!" % self.link)
            return
        if (self.soup is None):
            self.soup = BeautifulSoup(con.text, features="html5lib")
        if not (str(self.soup).find('error404') == -1):
            logging.error("Error 404 - page %s not found!" % self.link)
            return
        table = self.soup.find_all('div', class_="currency-table__large-text")
        self.best_price_found = True
        self.cb = str(table[0].contents)[2:-2]
        if len(table) < 2:
            self.best_price_found = False
        else:
            self.buy = str(table[1].contents)[2:-2]
            self.sell = str(table[2].contents)[2:-2]

        info = self.soup.find_all('div', class_="currency-table__rate__text")
        self.for_n_currency = str(info[0].contents).replace('[', "").replace(']', "").replace('\\n', " ").replace("\\t",
                                                                                                                  "").replace(
            "'", "")
        pos = max(self.for_n_currency.rfind(i) for i in "01234456789")
        self.for_n_currency = self.for_n_currency[1:pos + 1] + " " + self.for_n_currency[pos + 1:-1]
        while self.for_n_currency[0] == ' ':
            self.for_n_currency = self.for_n_currency[1:]
        self.for_n_currency = " " + self.for_n_currency
        message = 'Курс цб: ' + self.cb + self.for_n_currency + '\n'
        if self.best_price_found:
            self.bankname_for_buy = str(info[1].contents).replace('[', "").replace(']', "").replace('\\n', " ").replace(
                "\\t", "").replace("'", "")
            self.bankname_for_sell = str(info[2].contents).replace('[', "").replace(']', "").replace('\\n',
                                                                                                     " ").replace("\\t",
                                                                                                                  "").replace(
                "'", "")
            cnt = 0
            for c in self.bankname_for_buy:
                cnt = cnt + 1
                if c == ',':
                    self.bankname_for_buy = self.bankname_for_buy[0:cnt - 1]
                    break
            cnt = 0
            for c in self.bankname_for_sell:
                cnt = cnt + 1
                if c == ',':
                    self.bankname_for_sell = self.bankname_for_sell[0:cnt - 1]
                    break
            message = message + 'Оптимальный курс покупки: ' + self.buy + self.for_n_currency + ' ' + self.bankname_for_buy + '\n' + 'Оптимальный курс продажи: ' + self.sell + self.for_n_currency + ' ' + self.bankname_for_sell
        else:
            message = message + "Нет информации по курсу покупки и продаж"
        return message
        logging.info("Message %s parsed")

    def date_parse(self, cur, current_date):
        """Поиск курса цб о валюте по дате.
        :param cur: Искомая валюта
        :param current_date: Искомая дата
        :returns: сообщение с курсом валюты на дату
        """
        if current_date > datetime.today().date() or current_date < datetime.strptime('01.01.2005', '%d.%m.%Y').date():
            self.parsed = False
            return "Дата должна быть в диапазоне от 01.01.2005 до сегодняшнего дня"
            logging.warning("Data format inappropriate")
        else:
            self.link = self.link + current_date.strftime("%d.%m.%Y") + '/'
            s = requests.session()
            # noinspection PyBroadException
            try:
                con = s.get(self.link)
            except BaseException:
                logging.error("Failed to open %s!" % self.link)
            if (self.soup is None):
                self.soup = BeautifulSoup(con.text, features="html5lib")
            currency_list = self.soup.find('tbody')
            split = currency_list.find_all('tr')

            for sp in split:
                if not (str(sp.find_all('td')[0].contents[2]).find(cur) == -1):
                    return "курс " + cur + " на дату: " + str(float(
                        str(sp.find_all('td')[3].contents).replace('[', '').replace(']', '').replace("'",
                                                                                                     "")) / float(
                        str(sp.find_all('td')[1].contents).replace('[', '').replace(']', '').replace("'", "")))