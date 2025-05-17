import requests

TOKEN = 'TU_TOKEN_DEL_BOT'
CHAT_ID = 'TU_CHAT_ID'
MENSAJE = 'Hola! 🚀 Esto es una notificación desde tu bot de Telegram.'

url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
payload = {
    'chat_id': CHAT_ID,
    'text': MENSAJE
}

response = requests.post(url, data=payload)
print(response.json())
