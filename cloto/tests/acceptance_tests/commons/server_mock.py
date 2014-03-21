__author__ = 'arobres'


from bottle import route, run, template, Bottle, request, response, auth_basic
from collections import defaultdict
import ujson

app = Bottle()
statistics = {'num_scale_up': 0,
              'num_scale_down': 0,
              'num_notifications': 0}


@app.post("/scale_up/")
def scale_up():
    statistics['num_scale_up'] += 1


@app.post("/scale_down/")
def scale_up():
    statistics['num_scale_down'] += 1
    print statistics


@app.post("/notification/")
def scale_up():
    statistics['num_notifications'] += 1


@app.get("/reset_stats/")
def reset_stats():
    for x in statistics.keys():
        statistics[x] = 0


@app.get("/stats/")
def get_stats():

    return statistics

run(app, host='0.0.0.0', port=8080, reloader=True)



