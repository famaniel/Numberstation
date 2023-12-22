import time
import threading
from random import random

from bottle import post, request, route, run, static_file, view
from queue import Queue

from animation import Numbers, Chase, hsv_to_rgb
from dmx import DMX, RGB

@route('/')
@view('index')
def index():
    return {'foo': 'bar'}


@route('/number')
def number():
    n = request.query.number or request.query.n or ''
    r = request.query.r or 0
    g = request.query.g or 0
    b = request.query.b or 0
    token = request.query.token or 0
    if token == 'geheim':
        priorityQueue.put(lambda: set_animation(Numbers(n, (r, g, b))))
    else:
        backgroundQueue.put(lambda: set_animation(Numbers(n, (r, g, b))))


def set_animation(n: Numbers) -> None:
    dmx.animation = n


def queue_worker() -> None:
    while True:
        if not priorityQueue.empty():
            func = priorityQueue.get()
            func()
        elif not backgroundQueue.empty():
            func = backgroundQueue.get()
            func()
        else:
            # dmx.animation = Chase((255,0,0))
            set_animation(Numbers(f'{random()*100000000000:011.0f}', (hsv_to_rgb(random(), 1, 1))))
        time.sleep(5)


backgroundQueue = Queue(maxsize = 500)
priorityQueue = Queue(maxsize = 250)
dmx = DMX('127.0.0.1', maxchan=264)

for digit in range(11):
    for segment in range(8):
        dmx._rgbs.append(RGB(dmx, 8 * 3 * digit + 3 * segment + 1, 0))

threading.Thread(target = queue_worker, daemon = True).start()

dmx.start()

run(host='0.0.0.0', port=8080, reloader=False, debug=True)

