"""
Issue: #925
This is a basic spell checker which is to be used in the Experience Centre
"""

from flask import Flask, jsonify, request
from textblob import TextBlob
from textblob import Word


app = Flask(__name__)


@app.route('/correction')
def correction():
    text = request.args.get('text', '')
    text = TextBlob(text)
    return jsonify(text=unicode(text.correct()))

if __name__ == '__main__':
    # app runs in debug mode, turn this off if you're deploying
    app.run(debug=True)
