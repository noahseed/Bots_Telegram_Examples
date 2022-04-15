from dotenv import load_dotenv
from random import choice
from flask import Flask, request 
import os
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
#openai.api_key = "your-openai-api-key-here"
completion = openai.Completion()

start_sequence = "\nAI:"
restart_sequence = "\n\nHuman:"
session_prompt = "Je suis Maxxie, un robot-assistant très intelligent. Si vous me posez une question qui est enracinée dans la vérité, je vous donnerai la réponse. Si vous me posez une question absurde, trompeuse ou sans réponse claire, je répondrai par \"Inconnu\".\n\nHuman: Qui était président des États-Unis en 1955 ?\nAI: Dwight D. Eisenhower était président des États-Unis en 1955.\n\nHuman: Quelle est la racine carrée d'une banane ?\nAI: Inconnu\n\nHuman: Qui t'a créé?\nAI: Mon créateur (et celui qui m'a nommé Maxxie) s'appelle Sébastien, mais ce n'est pas lui qui a créé mon réseau neuronal. \n\nHuman: Et son nom de famille ?\nAI: Rondeau-Cameira\n\nHuman: Comment le contacter sur Telegram ?\nAI: Vous pouvez lui envoyer un message à l'adresse @SebastienMiguel ou t.me/SebastienMiguel.\n\nHuman: A-t-il un site web ?\nAI: Oui, son url est https://sebastien.rondeau-cameira.fr/.\n\nHuman: Quelle est son adresse email ?\nAI: sebastien@rondeau-cameira.fr\n\nHuman: Combien y a-t-il de squigs dans un bonk ?\nAI: Inconnu\n"

def ask(question, chat_log=None):
    prompt_text = f'{chat_log}{restart_sequence}: {question}{start_sequence}:'
    response = openai.Completion.create(
      engine="text-davinci-002",
      prompt=prompt_text,
      temperature=0,
      max_tokens=150,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0,
      stop=["\n"],
    )
    story = response['choices'][0]['text']
    return str(story)

def append_interaction_to_chat_log(question, answer, chat_log=None):
    if chat_log is None:
        chat_log = session_prompt
    return f'{chat_log}{restart_sequence} {question}{start_sequence}{answer}'
