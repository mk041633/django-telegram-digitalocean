import requests

def send_message_to_telegram(token, username, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    message = f"{username}, я получил от тебя сообщение: \n{message}"
    data = {
        'chat_id': chat_id,
        'text': message,
    }
    response = requests.post(url, json=data)
    return response
