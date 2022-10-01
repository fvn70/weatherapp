from random import randint, shuffle

from flask import Flask, render_template, request
import sys

app = Flask(__name__)
dict = {'name': ['night', 'day', 'evening-morning'],
        'degrees': [9, 32, -15],
        'state': ['Chilly', 'Sunny', 'Cold'],
        'city': ['Boston', 'New York', 'Edmonton'] }

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        city_name = request.form['city_name']
        dict['name'].append('autumn')
        dict['degrees'].append(randint(-30, 30))
        shuffle(dict['state'])
        dict['state'].append(dict['state'][0])
        dict['city'].append(city_name)
    num = len(dict['name'])
    return render_template('index.html', weather=dict, card_num=num)

# don't change the following way to run flask:
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
