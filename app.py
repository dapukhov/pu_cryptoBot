import telebot
from config import TOKEN, exchange
from extensions import ApiException, CryptoConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start_help(message: telebot.types.Message):
    text = 'Приветствую Тебя, Мамкин Инвестор! \n \
Если ты решил поменять валюту, которую сейчас хрен купишь - этот бот для тебя! \
Чтобы начать работу, введите команду в следующем формате:\n \
<имя валюты> <в какую валюту перевести> <Количество переводимой валюты>\n \
Пример: доллар рубль 100\n \
Посмотреть список доступных валют можно командой /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in exchange.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        quote, base, amount = message.text.split()
    except ValueError as err:
        bot.reply_to(message, f'Неверное количество параметров!\n {err}')

    try:
        total_base = CryptoConverter.get_price(quote, base, amount)
    except ApiException as err:
        bot.reply_to(message, f'Ошбка данных пользователя\n {err}')
    except Exception as err:
        bot.reply_to(message, f'Не удалось обработать команду\n {err}')
    else:
        text = f'Цена {amount} {quote} в 1 {base} - {total_base}'
        bot.send_message(message.chat.id, text)


if __name__ == '__main__':
    bot.polling()
