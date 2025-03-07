"""

Spinning off some threads to ping both resources in the API in api.py.

Running this on the async resource gives the same results, but it takes 10 seconds
instead of six seconds.

"""

import time
import threading

from model import get_url


def run(url: str):
    result = {}
    threads = [threading.Thread(target=get_url, args=[url, result]) for n in range(5)]
    for thread in threads:
        thread.start()
        # adding some space so that we don't get the starts all on the same second
        time.sleep(1)
    for thread in threads:
        thread.join()
    return result


if __name__ == '__main__':

    url1 = 'http://127.0.0.1:8000'
    url2 = 'http://127.0.0.1:8000/async'

    for url in (url1, url2):
        print(f'\nPinging {url}\n')
        t0 = time.time()
        results = run(url)
        t1 = time.time()
        print(f'\ntime elapsed: {int(t1 - t0)} seconds\n\n{results}\n')
        for thread in threading.enumerate():
            print(thread.name)