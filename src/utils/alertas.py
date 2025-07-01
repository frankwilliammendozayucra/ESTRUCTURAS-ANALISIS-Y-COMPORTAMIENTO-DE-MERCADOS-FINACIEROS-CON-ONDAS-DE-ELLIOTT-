import requests

def enviar_alerta_telegram(token, chat_id, mensaje):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": mensaje
    }
    response = requests.post(url, data=payload)
    return response.status_code == 200
