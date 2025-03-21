import asyncio

print('\n### Creating new task in the middle of another task\n')

async def task1():
    print("task1 - one")
    print('task1 - creating task2')
    task = asyncio.create_task(task2())
    print('task1 - four')
    await asyncio.sleep(1)
    print('task1 - five')
 
async def task2():
    print("task2 - two")
    await asyncio.sleep(1)
    print("task2 - three")

asyncio.run(task1())
