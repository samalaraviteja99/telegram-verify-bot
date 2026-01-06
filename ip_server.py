
from flask import Flask, request
from database import add_user, ip_exists, save_ip, mark_verified

app = Flask(__name__)

@app.route("/verify")
def verify():
    user_id = int(request.args.get("uid"))
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)

    if ip_exists(ip):
        return "❌ This internet already used."

    add_user(user_id)
    save_ip(ip, user_id)
    mark_verified(user_id)
    return "✅ Verification successful. Go back to Telegram."

app.run(host="0.0.0.0", port=5000)
