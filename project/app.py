# app.py
from flask import Flask, render_template, request, jsonify
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder="static", template_folder="templates")

# Load Groq API Key
GROQ_KEY = os.getenv("GROQ_API_KEY")
if GROQ_KEY:
    client = Groq(api_key=GROQ_KEY)
else:
    client = None
    print("⚠️ WARNING: GROQ_API_KEY not found. Running in ECHO mode.")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    user_msg = data.get("message", "").strip()

    if not user_msg:
        return jsonify({"reply": "Please send a non-empty message."}), 400

    if client is None:
        return jsonify({"reply": f"(ECHO) {user_msg}"})

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": user_msg}],
            max_tokens=700
        )

        # CORRECT way to extract message
        bot_reply = response.choices[0].message.content

        return jsonify({"reply": bot_reply})

    except Exception as e:
        print("⚠️ ERROR while calling Groq:", repr(e))
        return jsonify({"reply": "⚠️ Backend error contacting Groq. Check logs."}), 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
