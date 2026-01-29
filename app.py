from flask import Flask, request
import requests

app = Flask(__name__)

VERIFY_TOKEN = "djezzy123"
PAGE_ACCESS_TOKEN = "EAAUvcXvXsl8BQsbvxWZAwlRZA6OQ8MFNUVkKsEBr8CZAo9mYxthH26L6F4ZClkTXIpJMAwRRIG7ApszcxVOXyZAaGUcHUZClnbFtwr9kcsZA6lPLwaxI3PlXPUFZAZBYrcbifrKwZCPAq9o98cJjPOO7YQHET2LLwNP4L8WgCzixk0thMebWM5UQ0V386jjbEdvRLAxMFsZAwZDZD"

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if token == VERIFY_TOKEN:
            return challenge
        return "Forbidden", 403

    data = request.json
    for entry in data.get("entry", []):
        for event in entry.get("messaging", []):
            sender_id = event.get("sender", {}).get("id")
            text = event.get("message", {}).get("text", "")
            if sender_id and text:
                reply(sender_id, text)
    return "ok", 200

def reply(user_id, text):
    text = text.strip().lower()
    if text == "رصيدي":
        msg = (
            "مرحبا 👋\n"
            "📱 رقمك: 07********\n"
            "💳 رصيدك: 235 دج\n"
            "📶 الشريحة: Djezzy Prépayée\n"
            "⚠️ بيانات تجريبية"
        )
    else:
        msg = "اكتب: رصيدي"
    send(user_id, msg)

def send(user_id, text):
    url = "https://graph.facebook.com/v18.0/me/messages"
    params = {"access_token": PAGE_ACCESS_TOKEN}
    payload = {"recipient": {"id": user_id}, "message": {"text": text}}
    requests.post(url, params=params, json=payload)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
