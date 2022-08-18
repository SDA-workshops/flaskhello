import redis
from flask import Flask
from tenacity import retry, stop_after_attempt, wait_fixed

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)


@retry(stop=stop_after_attempt(5), wait=wait_fixed(0.5))
def get_hit_count():
    return cache.incr('hits')


@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello World! I have been seen {} times.\n'.format(count)
