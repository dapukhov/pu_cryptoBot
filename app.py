import telebot

TOKEN = '5989822061:AAH-KtA5MbQZn5PdmCt2nDvS-JUSucRo53o'
bot = telebot.TeleBot(TOKEN)

keys = {
    'биткоин': 'BTC',
    'эфириум': 'ETH',
    'доллар': 'USD',
}


# Обрабатываются все сообщения, содержащие команды '/start' or '/help'.
@bot.message_handler(commands=['start', 'help'])
def start_help(message: telebot.types.Message):
    text = 'Чтобы начать работу, введите команду в следующем формате:\n \
<имя валюты> <в какую валюту перевести> <Количество переводимой валюты>\n \
Пример: доллар рубль 100\n \
Посмотреть список доступных валют можно командой /values'
    bot.reply_to(message, text)


bot.polling()
