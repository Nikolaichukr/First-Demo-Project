from flask import Flask, render_template
import random
import os

app = Flask(__name__)

quotes = [
    "The only limit to our realization of tomorrow will be our doubts of today.",
    "Success is not final, failure is not fatal: It is the courage to continue that counts.",
    "The future belongs to those who believe in the beauty of their dreams.",
    "In the middle of every difficulty lies opportunity.",
    "Life is really simple, but we insist on making it complicated.",
    "The best way to predict the future is to create it.",
    "In three words I can sum up everything I've learned about life: it goes on.",
    "Believe you can and you're halfway there.",
    "The secret of getting ahead is getting started.",
    "The only way to do great work is to love what you do.",
    "Don't watch the clock; do what it does. Keep going.",
    "To be yourself in a world that is constantly trying to make you something else is the greatest accomplishment.",
    "The only person you are destined to become is the person you decide to be.",
    "Success is walking from failure to failure with no loss of enthusiasm.",
    "It does not matter how slowly you go as long as you do not stop.",
    "If you're going through hell, keep going.",
    "The future depends on what you do today.",
    "The harder I work, the luckier I get.",
    "Dream big and dare to fail.",
    "Life is 10% what happens to us and 90% how we react to it."
]

@app.route('/')
def index():
    random_quote = random.choice(quotes)
    build_number = os.environ.get('BUILD_NUMBER')
    return render_template('index.html', quote=random_quote, build_number=build_number)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')