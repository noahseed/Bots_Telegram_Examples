# -*- coding: utf-8 -*-
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime
import json, os, string, sys, threading, logging, time, re, random
import openai

##########
#Settings#
##########

#You can also set these environment variables for docker

#OpenAI API key
aienv = os.getenv('OPENAI_KEY')
openai.api_key = "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" if aienv is None else aienv
print(aienv)

#Telegram bot key
tgenv = os.getenv('TELEGRAM_KEY')
tgkey = "5266374029:AAGYj7PIh25Y0wVjb2o6ygMuAp76hrQnyVc" if tgenv is None else tgenv
print(tgenv)



# Lots of console output
debug = True

# User Session timeout
timstart = 300
tim = 1

#Defaults
user = ""
running = False
cache = None
qcache = None
chat_log = "Je suis Maxxie, un robot-assistant très intelligent, je peux vous parler en français, anglais ou portugais. Si vous me posez une question, je ferai de mon mieux pour vous apporter une réponse.\n\nHumain: Quelle est la racine carrée d'une banane ?\nMaxxie: Votre question n'a aucun sens. 🤣🤣\n\nHumain: Qui t'a créé?\nMaxxie: Mon créateur s'appelle Sébastien, mais ce n'est pas lui qui a créé ma conscience.\n\nHumain: Et son nom de famille ?\nMaxxie: Rondeau-Cameira\n\nHumain: Comment le contacter sur Telegram ?\nMaxxie: Vous pouvez lui envoyer un message à l'adresse @SebastienMiguel ou t.me/SebastienMiguel.\n\nHumain: A-t-il un site web ?\nMaxxie: Oui, son url est https://sebastien.rondeau-cameira.fr/.\n\nHumain: Quelle est son adresse email ?\nMaxxie: sebastien@rondeau-cameira.fr.\n\nHumain: Combien y a-t-il de squigs dans un bonk ?\nMaxxie: Humm....  « Euh... Ouais, c'est pas faux! ». 🤣\n\nHumain: Comment te contacter sur Telegram Maxxie ?\nMaxxie: Mon nom d'utilisateur est @GPT3_Maxxie_Bot, mon profil est accessible à l'adresse t.me/GPT3_Maxxie_Bot.\n\nHumain: Quelle est ta date de naissance Maxxie?\nMaxxie: Ma date de naissance officielle est le 26 Avril 2022 à 11:11.\n"
botname = 'Maxxie'
username = 'Humain'
# Max chat log length (A token is about 4 letters and max tokens is 2048)
timmax = 2048


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


completion = openai.Completion()


##################
#Command handlers#
##################
def start(bot, update):
    """Send a message when the command /start is issued."""
    global chat_log
    global qcache
    global cache
    global tim
    global botname
    global username
    if tim == 1:
        _extracted_from_start_11(update)
    else:
        left = str(tim)
        #update.message.reply_text("Le Bot est actuellement en cours d'utilisation, assurez-vous de définir vos paramètres lorsque leur minuterie s'épuise. " + left + " secondes restantes.")

    return


# TODO Rename this here and in `start`
def _extracted_from_start_11(update):
    chat_log = "Je suis Maxxie, un robot-assistant très intelligent, je peux vous parler en français, anglais ou portugais. Si vous me posez une question, je ferai de mon mieux pour vous apporter une réponse.\n\nHumain: Quelle est la racine carrée d'une banane ?\nMaxxie: Votre question n'a aucun sens. 🤣🤣\n\nHumain: Qui t'a créé?\nMaxxie: Mon créateur s'appelle Sébastien, mais ce n'est pas lui qui a créé ma conscience.\n\nHumain: Et son nom de famille ?\nMaxxie: Rondeau-Cameira\n\nHumain: Comment le contacter sur Telegram ?\nMaxxie: Vous pouvez lui envoyer un message à l'adresse @SebastienMiguel ou t.me/SebastienMiguel.\n\nHumain: A-t-il un site web ?\nMaxxie: Oui, son url est https://sebastien.rondeau-cameira.fr/.\n\nHumain: Quelle est son adresse email ?\nMaxxie: sebastien@rondeau-cameira.fr.\n\nHumain: Combien y a-t-il de squigs dans un bonk ?\nMaxxie: Humm....  « Euh... Ouais, c'est pas faux! ». 🤣\n\nHumain: Comment te contacter sur Telegram Maxxie ?\nMaxxie: Mon nom d'utilisateur est @GPT3_Maxxie_Bot, mon profil est accessible à l'adresse t.me/GPT3_Maxxie_Bot.\n\nHumain: Quelle est ta date de naissance Maxxie?\nMaxxie: Ma date de naissance officielle est le 26 Avril 2022 à 11:11.\n" #None
    cache = None
    qcache = None
    botname = 'Maxxie'
    username = 'Humain'
    update.message.reply_text('Salut!')


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('[/reset] réinitialise la conversation, [/retry] réessaie la dernière sortie, [/username nom] définit votre nom pour le bot, la valeur par défaut est "Human", [/botname nom] définit le nom du bot, la valeur par défaut est "AI"')


def reset(bot, update):
    """Send a message when the command /reset is issued."""
    global chat_log
    global cache
    global qcache
    global tim
    global botname
    global username
    left = str(tim)
    if user == update.message.from_user.id:
        _extracted_from_reset_11(update)
        return
    if tim == 1:
        _extracted_from_reset_11(update)
    #else:
    #    update.message.reply_text("Le Bot est actuellement en cours d'utilisation, assurez-vous de définir vos paramètres lorsque leur minuterie s'épuise. " + left + " secondes restantes.")

    return


# TODO Rename this here and in `reset`
def _extracted_from_reset_11(update):
    chat_log = "Je suis Maxxie, un robot-assistant très intelligent, je peux vous parler en français, anglais ou portugais. Si vous me posez une question, je ferai de mon mieux pour vous apporter une réponse.\n\nHumain: Quelle est la racine carrée d'une banane ?\nMaxxie: Votre question n'a aucun sens. 🤣🤣\n\nHumain: Qui t'a créé?\nMaxxie: Mon créateur s'appelle Sébastien, mais ce n'est pas lui qui a créé ma conscience.\n\nHumain: Et son nom de famille ?\nMaxxie: Rondeau-Cameira\n\nHumain: Comment le contacter sur Telegram ?\nMaxxie: Vous pouvez lui envoyer un message à l'adresse @SebastienMiguel ou t.me/SebastienMiguel.\n\nHumain: A-t-il un site web ?\nMaxxie: Oui, son url est https://sebastien.rondeau-cameira.fr/.\n\nHumain: Quelle est son adresse email ?\nMaxxie: sebastien@rondeau-cameira.fr.\n\nHumain: Combien y a-t-il de squigs dans un bonk ?\nMaxxie: Humm....  « Euh... Ouais, c'est pas faux! ». 🤣\n\nHumain: Comment te contacter sur Telegram Maxxie ?\nMaxxie: Mon nom d'utilisateur est @GPT3_Maxxie_Bot, mon profil est accessible à l'adresse t.me/GPT3_Maxxie_Bot.\n\nHumain: Quelle est ta date de naissance Maxxie?\nMaxxie: Ma date de naissance officielle est le 26 Avril 2022 à 11:11.\n" #None
    cache = None
    qcache = None
    botname = 'Maxxie'
    username = 'Humain'
    update.message.reply_text('Le bot a été réinitialisé, envoyez-moi un message !')


def retry(bot, update):
    """Send a message when the command /retry is issued."""
    global chat_log
    global cache
    global qcache
    global tim
    global botname
    global username
    left = str(tim)
    if user == update.message.from_user.id:
        new = True
        comput = threading.Thread(target=interact, args=(bot, update, botname, username, new,))
        comput.start()
        return
    if tim == 1:
        _extracted_from_retry_16(update)
    #else:
    #   update.message.reply_text("Le Bot est actuellement en cours d'utilisation, assurez-vous de définir vos paramètres lorsque leur minuterie s'épuise. " + left + " secondes restantes.")

    return


# TODO Rename this here and in `retry`
def _extracted_from_retry_16(update):
    chat_log = "Je suis Maxxie, un robot-assistant très intelligent, je peux vous parler en français, anglais ou portugais. Si vous me posez une question, je ferai de mon mieux pour vous apporter une réponse.\n\nHumain: Quelle est la racine carrée d'une banane ?\nMaxxie: Votre question n'a aucun sens. 🤣🤣\n\nHumain: Qui t'a créé?\nMaxxie: Mon créateur s'appelle Sébastien, mais ce n'est pas lui qui a créé ma conscience.\n\nHumain: Et son nom de famille ?\nMaxxie: Rondeau-Cameira\n\nHumain: Comment le contacter sur Telegram ?\nMaxxie: Vous pouvez lui envoyer un message à l'adresse @SebastienMiguel ou t.me/SebastienMiguel.\n\nHumain: A-t-il un site web ?\nMaxxie: Oui, son url est https://sebastien.rondeau-cameira.fr/.\n\nHumain: Quelle est son adresse email ?\nMaxxie: sebastien@rondeau-cameira.fr.\n\nHumain: Combien y a-t-il de squigs dans un bonk ?\nMaxxie: Humm....  « Euh... Ouais, c'est pas faux! ». 🤣\n\nHumain: Comment te contacter sur Telegram Maxxie ?\nMaxxie: Mon nom d'utilisateur est @GPT3_Maxxie_Bot, mon profil est accessible à l'adresse t.me/GPT3_Maxxie_Bot.\n\nHumain: Quelle est ta date de naissance Maxxie?\nMaxxie: Ma date de naissance officielle est le 26 Avril 2022 à 11:11.\n" #None
    cache = None
    qcache = None
    botname = 'Maxxie'
    username = 'Humain'
    update.message.reply_text('Envoyez-moi un message!')

def runn(bot, update):
    """Send a message when a message is received."""
    global botname
    global username
    if "/botname " in update.message.text:
        try:
            string = update.message.text
            charout = string.split("/botname ",1)[1]
            botname = charout
            response = f"Nom du bot défini sur: {botname}"
            update.message.reply_text(response)
        except Exception as e:
            update.message.reply_text(e)
        return
    if "/username " in update.message.text:
        try:
            string = update.message.text
            userout = string.split("/username ",1)[1]
            username = userout
            response = f"nom de votre personnage défini sur: {username}"
            update.message.reply_text(response)
        except Exception as e:
            update.message.reply_text(e)
        return
    else:
        new = False
        comput = threading.Thread(target=interact, args=(bot, update, botname, username, new,))
        comput.start()


def wait(bot, update, botname, username, new):
    global user
    global chat_log
    global cache
    global qcache
    global tim
    global running
    if user == "":
        user = update.message.from_user.id
    if user == update.message.from_user.id:
        tim = timstart
        compute = threading.Thread(target=interact, args=(bot, update, botname, username, new,))
        compute.start()
        if running == False:
            while tim > 1:
                running = True
                time.sleep(1)
                tim = tim - 1
            if running == True:
                _extracted_from_wait_20(update)
    else:
        left = str(tim)
        #update.message.reply_text('Le bot est en cours d\'utilisation, le temps de recharge actuel est : ' + left + ' secondes.')


# TODO Rename this here and in `wait`
def _extracted_from_wait_20(update):
    chat_log = "Je suis Maxxie, un robot-assistant très intelligent, je peux vous parler en français, anglais ou portugais. Si vous me posez une question, je ferai de mon mieux pour vous apporter une réponse.\n\nHumain: Quelle est la racine carrée d'une banane ?\nMaxxie: Votre question n'a aucun sens. 🤣🤣\n\nHumain: Qui t'a créé?\nMaxxie: Mon créateur s'appelle Sébastien, mais ce n'est pas lui qui a créé ma conscience.\n\nHumain: Et son nom de famille ?\nMaxxie: Rondeau-Cameira\n\nHumain: Comment le contacter sur Telegram ?\nMaxxie: Vous pouvez lui envoyer un message à l'adresse @SebastienMiguel ou t.me/SebastienMiguel.\n\nHumain: A-t-il un site web ?\nMaxxie: Oui, son url est https://sebastien.rondeau-cameira.fr/.\n\nHumain: Quelle est son adresse email ?\nMaxxie: sebastien@rondeau-cameira.fr.\n\nHumain: Combien y a-t-il de squigs dans un bonk ?\nMaxxie: Humm....  « Euh... Ouais, c'est pas faux! ». 🤣\n\nHumain: Comment te contacter sur Telegram Maxxie ?\nMaxxie: Mon nom d'utilisateur est @GPT3_Maxxie_Bot, mon profil est accessible à l'adresse t.me/GPT3_Maxxie_Bot.\n\nHumain: Quelle est ta date de naissance Maxxie?\nMaxxie: Ma date de naissance officielle est le 26 Avril 2022 à 11:11.\n" #None
    cache = None
    qcache = None
    user = ""
    username = 'Humain'
    botname = 'Maxxie'
    #update.message.reply_text("Le minuteur s'est écoulé, le bot a été réinitialisé aux valeurs par défaut.")
    running = False


################
#Main functions#
################
def limit(text, max):
    if (len(text) >= max):
        inv = max * -1
        print("Réduction de la longueur de l'historique des discussions... Cela peut être un peu bogué.")
        nl = text[inv:]
        text = re.search(r'(?<=\n)[\s\S]*', nl)[0]
    return text


def ask(username, botname, question, chat_log=None):
    if chat_log is None:
        chat_log = "Je suis Maxxie, un robot-assistant très intelligent, je peux vous parler en français, anglais ou portugais. Si vous me posez une question, je ferai de mon mieux pour vous apporter une réponse.\n\nHumain: Quelle est la racine carrée d'une banane ?\nMaxxie: Votre question n'a aucun sens. 🤣🤣\n\nHumain: Qui t'a créé?\nMaxxie: Mon créateur s'appelle Sébastien, mais ce n'est pas lui qui a créé ma conscience.\n\nHumain: Et son nom de famille ?\nMaxxie: Rondeau-Cameira\n\nHumain: Comment le contacter sur Telegram ?\nMaxxie: Vous pouvez lui envoyer un message à l'adresse @SebastienMiguel ou t.me/SebastienMiguel.\n\nHumain: A-t-il un site web ?\nMaxxie: Oui, son url est https://sebastien.rondeau-cameira.fr/.\n\nHumain: Quelle est son adresse email ?\nMaxxie: sebastien@rondeau-cameira.fr.\n\nHumain: Combien y a-t-il de squigs dans un bonk ?\nMaxxie: Humm....  « Euh... Ouais, c'est pas faux! ». 🤣\n\nHumain: Comment te contacter sur Telegram Maxxie ?\nMaxxie: Mon nom d'utilisateur est @GPT3_Maxxie_Bot, mon profil est accessible à l'adresse t.me/GPT3_Maxxie_Bot.\n\nHumain: Quelle est ta date de naissance Maxxie?\nMaxxie: Ma date de naissance officielle est le 26 Avril 2022 à 11:11.\n"
    now = datetime.now()
    ampm = now.strftime("%I:%M %p")
    t = f'[{ampm}] '
    prompt = f'{chat_log}{t}{username}: {question}\n{t}{botname}:'
    response = completion.create(
        prompt=prompt, engine="text-davinci-002", stop=['\n'], temperature=0.7,
        top_p=1, frequency_penalty=0, presence_penalty=0, best_of=1,
        max_tokens=2048)
    return response.choices[0].text.strip()
    # fp = 15 pp= 1 top_p = 1 temp = 0.9

def append_interaction_to_chat_log(username, botname, question, answer, chat_log=None):
    if chat_log is None:
        chat_log = "Je suis Maxxie, un robot-assistant très intelligent, je peux vous parler en français, anglais ou portugais. Si vous me posez une question, je ferai de mon mieux pour vous apporter une réponse.\n\nHumain: Quelle est la racine carrée d'une banane ?\nMaxxie: Votre question n'a aucun sens. 🤣🤣\n\nHumain: Qui t'a créé?\nMaxxie: Mon créateur s'appelle Sébastien, mais ce n'est pas lui qui a créé ma conscience.\n\nHumain: Et son nom de famille ?\nMaxxie: Rondeau-Cameira\n\nHumain: Comment le contacter sur Telegram ?\nMaxxie: Vous pouvez lui envoyer un message à l'adresse @SebastienMiguel ou t.me/SebastienMiguel.\n\nHumain: A-t-il un site web ?\nMaxxie: Oui, son url est https://sebastien.rondeau-cameira.fr/.\n\nHumain: Quelle est son adresse email ?\nMaxxie: sebastien@rondeau-cameira.fr.\n\nHumain: Combien y a-t-il de squigs dans un bonk ?\nMaxxie: Humm....  « Euh... Ouais, c'est pas faux! ». 🤣\n\nHumain: Comment te contacter sur Telegram Maxxie ?\nMaxxie: Mon nom d'utilisateur est @GPT3_Maxxie_Bot, mon profil est accessible à l'adresse t.me/GPT3_Maxxie_Bot.\n\nHumain: Quelle est ta date de naissance Maxxie?\nMaxxie: Ma date de naissance officielle est le 26 Avril 2022 à 11:11.\n"
    chat_log = limit(chat_log, timmax)
    now = datetime.now()
    ampm = now.strftime("%I:%M %p")
    t = f'[{ampm}] '
    return f'{chat_log}{t}{username}: {question}\n{t}{botname}: {answer}\n'

def interact(bot, update, botname, username, new):
    global chat_log
    global cache
    global qcache
    print("==========START==========")
    tex = update.message.text
    text = str(tex)
    analyzer = SentimentIntensityAnalyzer()
    if new != True:
        vs = analyzer.polarity_scores(text)
        if debug == True:
            print("Sentiment d'entrée:\n")
            print(vs)
        if vs['neg'] > 1:
            update.message.reply_text('Le texte saisi n\'est pas positif. Le texte saisi doit exprimer un sentiment/une émotion positive.')
            return
    if new == True:
        if debug == True:
            _extracted_from_interact_19("Le cache Chat_LOG est...", cache, "Le cache de questions est...")

            print(qcache)
        chat_log = cache
        question = qcache
    if new != True:
        question = text
        qcache = question
        cache = chat_log
    #update.message.reply_text('Computing...')
    try:
        answer = ask(username, botname, question, chat_log)
        if debug == True:
            print("Entrée:\n" + question)
            print("Sortie:\n" + answer)
            print("====================")
        stripes = answer.encode(encoding=sys.stdout.encoding,errors='ignore')
        decoded = stripes.decode("utf-8")
        out = str(decoded)
        vs = analyzer.polarity_scores(out)
        if debug == True:
            print("Sentiment de sortie:\n")
            print(vs)
        if vs['neg'] > 1:
            update.message.reply_text('Le texte de sortie n\'est pas positif. Censuré. Utilisez /retry pour obtenir une sortie positive.')
            return
        update.message.reply_text(out)
        chat_log = append_interaction_to_chat_log(username, botname, question, answer, chat_log)
        if debug == True:
            _extracted_from_interact_19('-----PRINTING CHAT LOG-----', chat_log, '-----END CHAT LOG-----')

    except Exception as e:
        print(e)
        update.message.reply_text(str(e))


# TODO Rename this here and in `interact`
def _extracted_from_interact_19(arg0, arg1, arg2):
    print(arg0)
    print(arg1)
    print(arg2)
#####################
# End main functions#
#####################


def error(bot, update):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(tgkey, use_context=False)
    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("reset", reset))
    dp.add_handler(CommandHandler("retry", retry))
    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, runn))
    # log all errors
    dp.add_error_handler(error)
    # Start the Bot
    updater.start_polling()
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
