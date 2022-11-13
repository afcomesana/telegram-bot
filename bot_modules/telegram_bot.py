import os
import requests
from dotenv import load_dotenv

class TelegramBot():
    
    def __init__(self):
        load_dotenv()
        self.bot_token = os.getenv('BOT_TOKEN')
        
    def get_request_url(self, method_name):
        return 'https://api.telegram.org/bot%s/%s' % (self.bot_token, method_name)
    
    def telegram_api_request(self, method_name, http_method = 'GET', data = None):
        
        url = self.get_request_url(method_name)
        
        if http_method == 'GET':
            response = requests.get(url, data)
        elif http_method == 'POST':
            # headers = {'Content-Type': 'application/json'}
            response = requests.post(url,json = data)
        
        # HTTP response code is not of success:
        if ( response.status_code != 200 ):
            response = response.json()
            raise Exception('Telegram API responded with status code: %s\nError message: %s' % (response['error_code'], response['description']))
        
        # Telegram allways sends back JSON format
        response = response.json()
        
        # Telegram request was not OK
        if not response['ok']:
            raise Exception('Telegram response was not OK. Message: %s' % response['message'])

        return response['result']
    
    def get_updates(self):
        return self.telegram_api_request('getUpdates')

    def send_message(self, data):
        return self.telegram_api_request('sendMessage', 'POST', data)
    
    def set_webhook(self):
        return self.telegram_api_request(
            'setWebhook',
            'POST',
            {
                'url': 'https://%s' % os.getenv('BOT_DOMAIN'),
                'secret_token': os.getenv('TELEGRAM_WEBHOOK_TOKEN')
            }
        )
        
    def get_chat(self, chat_id):
        return self.telegram_api_request('getChat', 'GET', {'chat_id': chat_id})