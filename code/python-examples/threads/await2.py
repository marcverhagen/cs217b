import time
import asyncio

print('\n### One task in the middle of another\n')

async def task1():
    print("task1 - one")
    await asyncio.sleep(1)
    await task2()
    print('task1 - three')
    await asyncio.sleep(1)
 
async def task2():
    await asyncio.sleep(1)
    print("task2 - two")

asyncio.run(task1())


print('\n### But the previous is really the same as this\n')

def reg_task1():
    print("task1 - one")
    time.sleep(1)
    reg_task2()
    print('task1 - three')
    time.sleep(1)
 
def reg_task2():
    time.sleep(1)
    print("task2 - two")

reg_task1()
