import telebot
import logging
from Logics import parsed_message, bru_parser, links, currency, configure

logging.basicConfig(filename="logs.log", level=logging.INFO, filemode="w")

client = telebot.TeleBot(configure.config['token'])


@client.message_handler(commands=['start'])
def welcome(message):
    """Приветствие, реагирует на /start"""
    client.send_message(message.chat.id, "Добро пожаловать, " + str(
        message.from_user.first_name) + "!\n Я бот, который выводит информацию о курсе доллара, евро, "
                                        "фунта-стерлинга, йены и юани. Чем я могу помочь?")
    logging.info("bot started")


@client.message_handler(commands=['help'])
def help(message):
    client.send_message(message.chat.id,
                        "Для того чтобы узнать курс валюты/всех валют в городе на сегодня, сообщение должно содержать город и валюту (для конкретной валюты) \n "
                        "Для того чтобы узнать курс валюты/всех валют на конкретную дату, введите дату в формате дд.мм.гггг")


@client.message_handler(content_types=['text'])
def bankiru_search(message):
    """Обработка сообщений и генерация ответа. Если бот находится в беседе, то он не реагирует на сообщения, в которых не находит ключевых слов.
    :param message: сообщение
    """
    message_data = parsed_message.parsed_message(message.text.lower())
    logging.info("message with id: %s received: %s" % (message.message_id, message.text))
    message_data.parse()
    if message_data.trigger:
        if not message_data.date_search:
            client.send_message(message.chat.id, "Поиск по городу, дата не обнаружена")
            if message_data.currency != 'all':
                parser_link = bru_parser.bru_parser(
                    'https://www.banki.ru/products/currency/cash/' + message_data.currency.lower() + '/' +
                    links.citylinks[
                        message_data.location])
                parser_link.default_parse()
                client.send_message(message.chat.id,
                                    message_data.currency + '\n' + parser_link.default_parse())
                logging.info("Sent message with %s currency to the chat %s" % (message_data.currency, message.chat.id))
            else:
                for c in currency.currency:
                    parser_link = bru_parser.bru_parser(
                        'https://www.banki.ru/products/currency/cash/' + c.lower() + '/' + links.citylinks[
                            message_data.location])
                    parser_link.default_parse()
                    client.send_message(message.chat.id, c + '\n' + parser_link.default_parse())
        else:
            client.send_message(message.chat.id, "Поиск по дате")
            if message_data.currency == 'all':
                for cur in currency.currency:
                    msg = bru_parser.bru_parser(
                        'https://www.banki.ru/products/currency/cb/').date_parse(cur, message_data.date)
                    client.send_message(message.chat.id, msg)
                    if msg == "Дата должна быть в диапазоне от 01.01.2005 до сегодняшнего дня":
                        break
            else:
                client.send_message(message.chat.id,
                                    bru_parser.bru_parser('https://www.banki.ru/products/currency/cb/').date_parse(
                                        message_data.currency, message_data.date))
    else:
        logging.warning("No information detected")
        if message.chat.type == 'private':
            client.send_message(message.chat.id, "Неверный формат данных")
    logging.info("Responded")


client.polling(none_stop=True)
