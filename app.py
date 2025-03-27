import os
from flask import Flask, request, render_template, session, redirect, url_for
from openai import OpenAI

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Replace with a secure key for production

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/", methods=["GET", "POST"])
def home():
    # Initialize history in session if it doesn't exist
    if "history" not in session:
        session["history"] = []

    if request.method == "POST":
        user_input = request.form["message"]

        # Include previous messages for context
        full_messages = [{"role": "user", "content": h["user"]} for h in session["history"]]
        full_messages.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=full_messages
        )
        response_text = response.choices[0].message.content

        # Save both user input and response to session
        session["history"].append({"user": user_input, "bot": response_text})
        session.modified = True

        return redirect(url_for("home"))  # 🔁 Redirect to avoid form resubmission

    return render_template("chat.html", history=session["history"])
