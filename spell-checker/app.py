"""
Issue: #925
This is a basic spell checker which is to be used in the Experience Centre
"""

from flask import Flask, jsonify, request, render_template
from textblob import TextBlob
from textblob import Word


app = Flask(__name__)

@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/correction')
def correction():
    text = request.args.get('search', '')
    text = TextBlob(text)
    corr_text = text.correct()
    return jsonify(str(corr_text))

if __name__ == '__main__':
    # app runs in debug mode, turn this off if you're deploying
    app.run(debug=True)
