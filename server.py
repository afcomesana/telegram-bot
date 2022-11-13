from flask import Flask, request, jsonify
from bot_modules.telegram_bot import TelegramBot
import unidecode

server = Flask(__name__)

@server.post('/')
def handle_telegram_request():
    
    # Receive request and prepare response for Telegram:
    data             = request.json
    webhook_response = (b'{}', 200)
    
    # Provissionaly, only response process 'message' info
    if 'message' not in data.keys(): return webhook_response
    
    message = data['message']
    
    # Initialize response dict, always gonna have the chat id and the parse is gonna be HTML:
    response = {
        'chat_id': message['chat']['id'],
        'parse_mode': 'HTML'
    }
    
    # The message is sent from a group, then we reply to that specific message:
    if message['chat']['type'] == 'group':
        # If the message is from a group, only response if we are mentioned
        if special_key_word_to_listen_for not in message['text'].lower(): return webhook_response
        response['reply_to_message_id'] = message['message_id']
        
    # The message is from private chat, prepare an answer consisting provissionaly on a greeting plus de user name:
    response['text'] = "Hola%s" % (' %s.' % message['from']['first_name'] if 'first_name' in message['from'].keys() else '.')
    
    # If we want a response depending on a name from a specific friend (not the best solution):
    predefined_answers = {
        'name1': 'Response for user with name1',
        'name2': 'Response for user with name2',
        'name3': 'Response for user with name3',
        'name4': 'Response for user with name4'
    }
    match_name = list(filter(lambda name: name in unidecode.unidecode(message['from']['first_name'].lower()), predefined_answers.keys()))
    if len(match_name) == 1:
        match_name = unidecode.unidecode(match_name[0])
        response['text'] += ' ' + predefined_answers[match_name]
        
    bot = TelegramBot()
    bot.send_message(response)

    return webhook_response