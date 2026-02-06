import time
import asyncio

task1 = True
task2 = False


### Running one task:

async def fun():
    print("Hello")
    result = await asyncio.sleep(1)  # Simulate an asynchronous task
    print("World")
    print(result)


### Running two tasks

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


if __name__ == '__main__':
    
    if task1:
        # start the event loop, running and waiting for the task to complete
        print('\n### One task\n')
        asyncio.run(fun())
    if task2:
        # start the event loop, running and waiting for both tasks to complete
        print('\n### Two tasks\n')
        asyncio.run(main())

