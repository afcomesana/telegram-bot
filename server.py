import os
import re
import unidecode
import openai
from flask import Flask, request, jsonify
from bot_modules.telegram_bot import TelegramBot

openai.api_key = os.getenv('OPENAI_API_KEY')
server = Flask(__name__)

@server.post('/')
def handle_telegram_request():
    
    try:
        
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
            if not re.search(r'tu(m|n)(n|m)?us', message['text'].lower()):
                return webhook_response
            
            response['reply_to_message_id'] = message['message_id']
            
        openai_response = openai.Completion.create(
            model="text-davinci-003",
            prompt=re.sub(r'(señor)? ?tu(m|n)(n|m)?us', 'tú', message['text'], flags=re.IGNORECASE),
            temperature=0.9,
            frequency_penalty=0.0,
            max_tokens=500,
            presence_penalty=0.6
        )
        
        response['text'] = openai_response['choices'][0]['text']
            
        bot = TelegramBot()
        bot.send_message_beta(response)

        return webhook_response
    
    finally:
        return webhook_response