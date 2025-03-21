"""

Spinning off some threads to ping the API defined in api.py.

There are two differences with thread1.py. One is that we only ping one of the
resources and the other is that we add a timeout on the join() method. Some threads
finish after the timeout and their results will not be in the results dictionary.

"""

import time
import threading

from model import get_url


def run(url: str):
    result = {}
    threads = [threading.Thread(target=get_url, args=[url, result]) for n in range(5)]
    for thread in threads:
        thread.start()
        time.sleep(1)
    for thread in threads:
        thread.join(timeout=1)
    return result


if __name__ == '__main__':

    url = 'http://127.0.0.1:8000'
    print(f'\nPinging {url}\n')
    results = run(url)
    for thread in threading.enumerate():
        print(thread.name)