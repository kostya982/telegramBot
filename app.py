import telebot
from config import TOKEN, values, help
from extensions import APIException, CryptoConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def startt(message):
    bot.send_message(message.chat.id, help + '\n /values')

@bot.message_handler(commands=['help'])
def helpp(message):
    bot.send_message(message.chat.id, help)

@bot.message_handler(commands=['values'])
def values_command(message):
    text = "Доступные валюты: Доллар, Евро, Рубль"
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert_result(message: telebot.types.Message):
    try:
        val = message.text.split(' ')

        if len(val) != 3:
            raise APIException('Не удалось обработать команду')

        base, quote, amount = val
        result = CryptoConverter.convert(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n {e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n {e}')
    else:
        text = f'{amount} {base} в {quote} равно: {result}'
        bot.send_message(message.chat.id, text)

bot.polling()