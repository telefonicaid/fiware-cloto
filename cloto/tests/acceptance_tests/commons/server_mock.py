__author__ = 'arobres'


from bottle import run, Bottle, request, response
from configuration import MOCK_IP, MOCK_PORT
from constants import MOCK_NOTIFICATION, MOCK_RESET_ERRORS, MOCK_RESET_STATS, MOCK_RESPONSE_SAVE, MOCK_SCALE_DOWN, \
    MOCK_SCALE_UP, MOCK_STATS, MOCK_NUM_NOTIFICATIONS, MOCK_NUM_SCALE_DOWN, MOCK_NUM_SCALE_UP
from collections import deque
import ujson

app = Bottle()
statistics = {MOCK_NUM_SCALE_UP: 0,
              MOCK_NUM_SCALE_DOWN: 0,
              MOCK_NUM_NOTIFICATIONS: 0}

responses_error = deque()


@app.post(MOCK_RESPONSE_SAVE)
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


@app.get(MOCK_RESET_ERRORS)
def reset_errors():

    responses_error.clear()


@app.post(MOCK_SCALE_UP)
def scale_up():
    if responses_error:
        response.status = int(responses_error.popleft())
        return {"message": "Error response: {}".format(response.status)}
    else:
        statistics['num_scale_up'] += 1


@app.post(MOCK_SCALE_DOWN)
def scale_up():
    statistics['num_scale_down'] += 1


@app.post(MOCK_NOTIFICATION)
def scale_up():
    statistics['num_notifications'] += 1


@app.get(MOCK_RESET_STATS)
def reset_stats():
    for x in statistics.keys():
        statistics[x] = 0


@app.get(MOCK_STATS)
def get_stats():

    return statistics


run(app, host=MOCK_IP, port=MOCK_PORT, reloader=True)
