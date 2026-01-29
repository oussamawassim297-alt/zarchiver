from flask import Flask, request
import requests

app = Flask(__name__)

PAGE_ACCESS_TOKEN = "EAAUvcXvXsl8BQsbvxWZAwlRZA6OQ8MFNUVkKsEBr8CZAo9mYxthH26L6F4ZClkTXIpJMAwRRIG7ApszcxVOXyZAaGUcHUZClnbFtwr9kcsZA6lPLwaxI3PlXPUFZAZBYrcbifrKwZCPAq9o98cJjPOO7YQHET2LLwNP4L8WgCzixk0thMebWM5UQ0V386jjbEdvRLAxMFsZAwZDZD"
VERIFY_TOKEN = "wassim_chikor_2026"

def get_user_name(user_id):
    url = f"https://graph.facebook.com/{user_id}?fields=first_name&access_token={PAGE_ACCESS_TOKEN}"
    try:
        response = requests.get(url).json()
        return response.get("first_name", "خويا")
    except:
        return "خويا"

def send_buttons(user_id):
    user_name = get_user_name(user_id)
    url = f"https://graph.facebook.com/v18.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    payload = {
        "recipient": {"id": user_id},
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": f"مرحبا {user_name}، كيفاه تحب نعاونك ليوم؟ 😊",
                    "buttons": [
                        {"type": "postback", "title": "💰 رصيدي", "payload": "CHECK_BALANCE"},
                        {"type": "postback", "title": "📱 نوع شريحتي", "payload": "CHECK_SIM"}
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
        for entry in data.get('entry', []):
            for messaging_event in entry.get('messaging', []):
                user_id = messaging_event['sender']['id']
                if 'postback' in messaging_event:
                    payload = messaging_event['postback']['payload']
                    if payload == "CHECK_BALANCE":
                        send_text(user_id, "باش نشوفلك رصيدك في جيزي، لازم نبعتلك رمز تأكيد (SMS) للهاتف تاعك. أرسل رقم هاتفك الآن 👇")
                    elif payload == "CHECK_SIM":
                        send_text(user_id, "شريحتك حالياً هي: جيزي دقة (مثال)")
                elif 'message' in messaging_event and 'text' in messaging_event['message']:
                    user_msg = messaging_event['message']['text']
                    if user_msg.isdigit() and len(user_msg) >= 10:
                        send_text(user_id, f"جاري إرسال الرمز للرقم {user_msg}... (انتظر لحظة)")
                    else:
                        send_buttons(user_id)
        return "ok", 200

if __name__ == '__main__':
    app.run(port=5000)
