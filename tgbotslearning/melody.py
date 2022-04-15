# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import time
import config
import telebot

bot = telebot.TeleBot(config.token)

# отсылаем файл
@bot.message_handler(commands=['test'])
def find_file_ids(message):
	for file in os.listdir('./music'):
		if file.split('.')[-1] == 'ogg':
			f = open(f'./music{file}', 'rb')
			msg = bot.send_voice(message.chat.id, f, None)
			# отсылаем его id
			bot.send_message(message.chat.id, msg.voice.file_id, reply_to_message_id = msg.message_id)
		time.sleep(3)

	if __name__ == '__main__':
		bot.polling(none_stop=True)
