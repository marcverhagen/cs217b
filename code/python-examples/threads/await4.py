import asyncio

async def custom_async_task(task_num):
    print(f"Task {task_num} started")
    await asyncio.sleep(3)
    print(f"Task {task_num} completed")

async def main():
    # forcing sequential processing
    await custom_async_task(1)
    await custom_async_task(2)

asyncio.run(main())
