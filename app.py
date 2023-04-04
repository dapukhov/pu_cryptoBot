import telebot
from config import TOKEN, keys
from extensions import ConvertionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start_help(message: telebot.types.Message):
    text = 'Приветствую Тебя, Мамкин Инвестор! \n \
Чтобы начать работу, введите команду в следующем формате:\n \
<имя валюты> <в какую валюту перевести> <Количество переводимой валюты>\n \
Пример: доллар рубль 100\n \
Посмотреть список доступных валют можно командой /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Неверное количество параметров')

        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)
    except ConvertionException as err:
        bot.reply_to(message, f'Ошбка данных пользователя\n {err}')
    except Exception as err:
        bot.reply_to(message, f'Не удалось обработать команду\n {err}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


if __name__ == '__main__':
    bot.polling()
