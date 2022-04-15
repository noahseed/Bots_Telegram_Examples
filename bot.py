#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
#import mysql import connector

#db = mysql.connector.connect(
#    host="localhost",
#    user="maxxiebot",
#    password="B82FK9Y7rI9b5bB",
#    database="maxxiebot"
#)

TOKEN = '5381444913:AAHzuEbcKyJ67um2Eq8enhshzRdsGt2PKsk'

def start(update, context):
    update.message.reply_text("""
Bienvenue sur le bot officiel de Robot Maxxie. 😊

Les commandes disponibles sont :
- /site pour obtenir l'adresse du site
- /facebook pour obtenir la page facebook
- /linkedin pour obtenir son profil Linkedin
    """)


def site(update, context):
    update.message.reply_text('https://sebastien.rondeau-cameira.fr')


def facebook(update, context):
    update.message.reply_text('https://www.facebook.com/sebastien.miguel.rondeau')


def linkedin(update, context):
    update.message.reply_text('https://www.linkedin.com/in/noahseed')


def pas_compris(update, context):
    update.message.reply_text("Je n'ai pas compris votre message ", update.message.text, "")


def main():
    # La classe Updater permet de lire en continu ce qu'il se passe sur le channel
    updater = Updater(TOKEN, use_context=True)

    # Pour avoir accès au dispatcher plus facilement
    dp = updater.dispatcher

    # On ajoute des gestionnaires de commandes
    # On donne a CommandHandler la commande textuelle et une fonction associée
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("site", site))
    dp.add_handler(CommandHandler("facebook", facebook))
    dp.add_handler(CommandHandler("linkedin", linkedin))

    # Pour gérer les autres messages qui ne sont pas des commandes
    dp.add_handler(MessageHandler(Filters.text, pas_compris))

    # Sert à lancer le bot
    updater.start_polling()

    # Pour arrêter le bot proprement avec CTRL+C
    updater.idle()


if __name__ == '__main__':
    main()
