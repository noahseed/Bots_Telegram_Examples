# -*- coding: utf-8 -*-
#!/usr/bin/env python

import config
import telebot

bot = telebot.TeleBot(config.token)

# обработчик, который реагирует на все входящие сообщения
@bot.message_handler(content_types=["text"])
def repeat_messages(message):
	bot.send_message(message.chat.id, message.text)

# запускаем бесконечный цикл получения новых записей со стороны Telegram
if __name__ == '__main__':
	bot.polling(none_stop=True)