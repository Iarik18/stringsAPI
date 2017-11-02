__author__ = 'Iaroslav'

from flask import Flask, jsonify,  make_response, abort
import requests

app = Flask(__name__)

words = []

@app.route('/', methods=['GET'])
def get_random_word1():
    response = requests.get('http://setgetgo.com/randomword/get.php')
    return response.text

@app.route('/get_random_word/', methods=['GET'])
def get_random_word():
    response = requests.get('http://setgetgo.com/randomword/get.php')
    word = response.text
    words.append(word)
    return word

#Get N most popular words
@app.route('/most_popular_words/<int:N>')
def most_populat_words(N):
    count = {}
    for word in words:
        if word in count:
            count[word] += 1
        else:
            count[word] = 1
    sortedWords = [(k, count[k]) for k in sorted(count, key=count.get, reverse=True)]
    return str(sortedWords[:N])


@app.route('/get_word_info/<string:word>', methods=['GET'])
def get_word_info(word):
    response = requests.get('https://en.wikipedia.org/w/api.php',
                            params={
                                'action': 'query',
                                'format': 'json',
                                'titles': word,
                                'prop': 'extracts',
                                'exintro': 'False',
                                'explaintext': 'True',
                                }).json()
    page = next(iter(response['query']['pages'].values()))
    if 'missing' in page:
        abort(404)
    return page['extract']


@app.route('/get_random_joke/', methods=['GET'])
@app.route('/get_random_joke/<firstName>;<lastName>', methods=['GET'])
@app.route('/get_random_joke/<firstName>', methods=['GET'])
@app.route('/get_random_joke/;<lastName>', methods=['GET'])
def get_random_joke(**kwargs):
    response = requests.get('https://api.icndb.com/jokes/random', params=kwargs)
    joke = response.json()
    return joke['value']['joke']

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error' : 'Not found'}), 404)

if __name__ == '__main__':
    app.run()

