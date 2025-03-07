import datetime
import threading
import requests


def timestamp():
    return datetime.datetime.now().isoformat(timespec='seconds')


def get_url(url: str, result: dict) -> str:
    thread = threading.current_thread().name
    print(f'{timestamp()} -- {thread} started')
    response = requests.get(url)
    print(f'{timestamp()} -- {thread} returned')
    result[thread] = response.text
    return response.text
