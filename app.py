import os
from flask import Flask, request, render_template, session, redirect, url_for
from openai import OpenAI

app = Flask(__name__)
app.secret_key = "your_secret_key"  # 🔒 Replace this with a strong secret key in production

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/", methods=["GET", "POST"])
def home():
    # Initialize chat history if it doesn't exist
    if "history" not in session:
        session["history"] = []

    if request.method == "POST":
        user_input = request.form["message"]

        # Prepare full message context for GPT
        full_messages = [{"role": "user", "content": h["user"]} for h in session["history"]]
        full_messages.append({"role": "user", "content": user_input})

        # Get response from OpenAI
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=full_messages
        )
        response_text = response.choices[0].message.content

        # Save chat to session
        session["history"].append({"user": user_input, "bot": response_text})
        session.modified = True

        # Prevent form resubmission on refresh
        return redirect(url_for("home"))

    return render_template("chat.html", history=session["history"])


# ✅ Required for Render to bind to its dynamic port
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
