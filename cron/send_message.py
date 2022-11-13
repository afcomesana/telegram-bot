import sys
import os
import getopt

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from bot_modules.telegram_bot import TelegramBot
from bot_modules.db_manager import DatabaseManager

try:
    # Get parameters when executed from term
    term_params = getopt.getopt(sys.argv[1:], 'i:t:m:', ['message=', 'chat-id', 'chat-title'])[0]

    for option, value in term_params:
        
        if   option in ['-m', '--message']:    message = value
            
        elif option in ['-i', '--chat-id']:    chat_id = value
            
        elif option in ['-t', '--chat-title']: chat_id = DatabaseManager().get_chat_by_title(value)[0][0]
            
    
    
    TelegramBot().send_message(
        {
            'chat_id': chat_id,
            'parse_mode': 'HTML',
            'text': message
        }
    )
        
except getopt.GetoptError:
    print('ERROR: Not suported option.\nPlease, use -m or --message option to send a message.')
    
except NameError:
    print('ERROR: Missing arguments.\npython3 send_message.py -m <message> (-cid <chat_id>|-cn <chat_name>)')