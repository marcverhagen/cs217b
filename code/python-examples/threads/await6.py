import time
import asyncio

def sleep(seconds: int):
	time.sleep(seconds)
	return seconds

async def fun():
    print("Hello")
    # This would give an error:
    # TypeError: object int can't be used in 'await' expression
    # await sleep(1)
    try:
      await sleep(1)
    except TypeError as e:
      print('Sorry, cannot await "sleep(1)"')
      print(f'TypeError: {e}')

asyncio.run(fun())

