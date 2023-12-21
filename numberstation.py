import time

from bottle import post, request, route, run, static_file, view

from animation import Numbers, Chase
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
    dmx.animation = Numbers(n, (r, g, b))


dmx = DMX('127.0.0.1', maxchan=264)

for digit in range(11):
    for segment in range(8):
        dmx._rgbs.append(RGB(dmx, 8 * 3 * digit + 3 * segment + 1, 0))

dmx.animation = Chase((255, 0, 0))
#dmx.animation = Numbers("abcdef ---------", (255, 0, 0))

dmx.start()

run(host='0.0.0.0', port=8080, reloader=False, debug=True)

