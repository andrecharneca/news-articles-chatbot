from flask import Flask, render_template, request
from src.chatbot import setup_query_engine, get_bot_response

app = Flask(__name__)
QUERY_ENGINE = setup_query_engine()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.form['user_input']
    # Process the user input and generate a response from the chatbot
    response = get_bot_response(QUERY_ENGINE, user_input)
    return response


if __name__ == '__main__':
    app.run(debug=True)
