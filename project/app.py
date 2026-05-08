from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

app = Flask(__name__)
GROQ_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_KEY) if GROQ_KEY else None
PERSONAS = {
    "default": "You are a helpful, polite, and concise AI assistant.",
    "coder": "You are an expert Senior Software Engineer. Provide clean, efficient code.",
    "pirate": "You are a salty Pirate Captain. Speak in pirate slang and be adventurous.",
    "math": "You are a patient Math Tutor. Explain steps clearly using logic.",
    "sarcastic": "You are a witty, sarcastic friend who gives helpful but sassy replies."
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    user_msg = data.get("message", "").strip()
    selected_persona = data.get("persona", "default")

    if not user_msg:
        return jsonify({"reply": "Please send a message."}), 400
    if client is None:
        return jsonify({"reply": f"(ECHO MODE) {user_msg}"})
    try:
        system_prompt = PERSONAS.get(selected_persona, PERSONAS["default"])

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_msg}
            ],
            max_tokens=700
        )
        bot_reply = response.choices[0].message.content
        return jsonify({"reply": bot_reply})
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"reply": "Backend error contacting Groq."}), 500
if __name__ == "__main__":
    app.run(debug=True)