import requests
from flask import Flask, render_template, jsonify
from bs4 import BeautifulSoup

app = Flask(__name__)


@app.route("/")
def index():
    return app.send_static_file('index.html')


@app.route("/<user_name>")
def user(user_name):
    soup = BeautifulSoup(requests.get('https://github.com/' + user_name).content, "html.parser")
    svg = soup.find('svg', {"class": "js-calendar-graph-svg"})
    firstg = svg.findChildren()[0]
    weeksg = firstg.find_all('g')
    result = []
    for weekg in weeksg:
        daysg = weekg.find_all('rect')
        week = []
        for dayrect in daysg:
            week.append({'data_count': int(dayrect['data-count']), 'data_date': dayrect['data-date']})
        result.append({'blocks': week})

    return jsonify(result)


if __name__ == '__main__':
    app.run()
