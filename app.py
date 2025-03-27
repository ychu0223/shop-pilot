import os
from flask import Flask, request, render_template
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    response_text = ""
    if request.method == "POST":
        user_input = request.form["message"]
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        )
        response_text = response.choices[0].message.content
    return render_template("chat.html", response=response_text)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)

