from flask import (Flask, jsonify, request, redirect, url_for, render_template,
                   abort, send_from_directory)
import json
import requests

app = Flask(__name__)

from cachetools import cached, TTLCache
cache = TTLCache(maxsize=25000, ttl=15*60)
class WeatherApiClient(object):
    def __init__(self, key='', base='http://api.weatherapi.com/v1'):
        self.key = key
        self.base = f"{base}"
    @cached(cache)
    def get_local(self, ip):
        url = f'{self.base}/current.json?key={self.key}&q={ip}'
        response = requests.get(url)
        return response.json()

weather_api = WeatherApiClient(key='81afd70710744cc380d213803210404')


class Articles(object):
    def __init__(self):
        self.articles = {
            'article_001': {
                'title': 'Massive Facebook leak: data of 533 million users',
                'subtitle': 'What\'s in it?',
                'url': 'https://netlabe.com/massive-facebook-leak-data-of-533-million-users-3751573ec692',
                'conditions': '',
            },
            'article_002': {
                'title': 'How to detect online trends without web scraping',
                'subtitle': 'News monitoring using image processing',
                'url': 'https://netlabe.com/how-to-detect-online-trends-without-web-scraping-b6799fc00450',
                'conditions': '',
            },
            'article_003': {
                'title': 'How to predict solar energy production',
                'subtitle': 'Efficient use of renewable energy sources with machine learning',
                'url': 'https://netlabe.com/how-to-predict-solar-energy-production-887ce31ec9d1',
                'conditions': '',
            },
            'article_004': {
                'title': 'Finally, the weather for sunbathing',
                'subtitle': 'How to protect yourself from sunburn?',
                'url': '#',
                'conditions': '["condition"]["text"]=="Sunny"',
            },
            'article_005': {
                'title': 'It\'s still raining',
                'subtitle': 'The 10 best activities for rainy weather',
                'url': '#',
                'conditions': '["condition"]["text"]=="Moderate rain"',
            }
        }

    def get_all(self):
        return list(self.articles.values())

    def findById(self, id):
        try:
            return self.articles[id]
        except:
            return {'title':'404', 'subtitle': 'Page not found'}
    
    def findByWeather(self, client_ip, weather_api):
        local_weather = weather_api.get_local(client_ip)
        articles = self.get_all()

        def apply(article, weather):

            if article['conditions'] != '':
                try:
                    return eval(f"weather['current']{article['conditions']}")
                except:
                    return False
            return True

        return list(filter(lambda article: apply(article, local_weather), articles))

def get_ip(app):
    if app.debug:
        if request.args.get('ip'):
            return request.args.get('ip')
        return '37.47.58.114'
    else:
        return request.remote_addr

@app.route('/')
def index():
    return render_template('index.html', articles=Articles().findByWeather(get_ip(app), weather_api))


@app.errorhandler(404)
def page_not_found_error(error):
    return jsonify({'status': 404})

if __name__ == '__main__':
    app.run()