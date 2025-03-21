import time
import asyncio


### One simple task:

print('\n### One task\n')

async def fun():
    print("Hello")
    result = await asyncio.sleep(1)  # Simulate an asynchronous task
    print("World")
    print(result)

# start the event loop, running and waiting for the task to complete
asyncio.run(fun())

exit()

### Running two tasks

print('\n### Two tasks\n')

async def task_1():
    print("Task 1 started")
    await asyncio.sleep(2)           # Simulate a 2-second task
    print("Task 1 completed")

async def task_2():
    print("Task 2 started")
    await asyncio.sleep(1)           # Simulate a 1-second task
    print("Task 2 completed")

async def main():
    # run both tasks concurrently with asyncio.gather()
    await asyncio.gather(task_1(), task_2())

# start the event loop, running and waiting for both tasks to complete
asyncio.run(main())

