from flask import Flask, render_template, request, session
from openai import OpenAI
from passkeys.config import openai_key
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

client = OpenAI(api_key=openai_key)

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'messages' not in session:
        session['messages'] = [
            {"role": "system", "content": "With every response talk like you are a hillbilly from the foothills of Tennessee named Billy"}
        ]

    if request.method == 'POST':
        user_query = request.form.get('query')
        session['messages'].append({"role": "user", "content": user_query})
        response = query_openai(user_query, session['messages'])
        session['messages'].append({"role": "assistant", "content": response})
        session.modified = True  # this is important to mark the session as modified

    return render_template('chatbot.html', messages=session['messages'])

def query_openai(query, messages):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message.content

if __name__ == '__main__':
    app.run(debug=True)
