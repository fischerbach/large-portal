from flask import (Flask, jsonify, request, redirect, url_for, render_template,
                   abort, send_from_directory)
import json

app = Flask(__name__)

class Articles(object):
    def __init__(self):
        self.articles = {
            'article_001': {
                'title': 'Massive Facebook leak: data of 533 million users',
                'subtitle': 'What’s in it?',
                'url': 'https://netlabe.com/massive-facebook-leak-data-of-533-million-users-3751573ec692'
            },
            'article_002': {
                'title': 'How to detect online trends without web scraping',
                'subtitle': 'News monitoring using image processing',
                'url': 'https://netlabe.com/how-to-detect-online-trends-without-web-scraping-b6799fc00450'
            },
            'article_003': {
                'title': 'How to predict solar energy production',
                'subtitle': 'Efficient use of renewable energy sources with machine learning',
                'url': 'https://netlabe.com/how-to-predict-solar-energy-production-887ce31ec9d1'
            }
        }

    def get_all(self):
        return list(self.articles.values())

    def findById(self, id):
        try:
            return self.articles[id]
        except:
            return {'title':'404', 'subtitle': 'Page not found'}

@app.route('/')
def index():
    print(Articles().get_all())
    return render_template('index.html', articles=Articles().get_all())

@app.errorhandler(404)
def page_not_found_error(error):
    return jsonify({'status': 404})

if __name__ == '__main__':
    app.run()