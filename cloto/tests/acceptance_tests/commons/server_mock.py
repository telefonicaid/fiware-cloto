__author__ = 'arobres'


from bottle import run, Bottle, request, response
from configuration import MOCK_IP, MOCK_PORT
from collections import deque
import ujson

app = Bottle()
statistics = {'num_scale_up': 0,
              'num_scale_down': 0,
              'num_notifications': 0}

responses_error = deque()

@app.post('/save_response/')
def save_response():

    body = "".join(request.body)
    try:
        body = ujson.loads(body)
    except:
        response.status = 400
        return {"message": "The JSON format is not correct"}

    if 'error_code' not in body.keys():
        response.status = 400
        return {"message": "Error code is not included in the request"}
    else:
        responses_error.append(body['error_code'])


@app.get('/reset_errors/')
def reset_errors():

    responses_error.clear()


@app.post("/scale_up/")
def scale_up():
    if responses_error:
        response.status = int(responses_error.popleft())
        return {"message": "Error response: {}".format(response.status)}
    else:
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


run(app, host=MOCK_IP, port=MOCK_PORT, reloader=True)
