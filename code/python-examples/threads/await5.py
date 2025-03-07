"""

This will produce:

Function 1 started..
Function 2 started..
Function 3 started..
Function 3 ended
Function 1 ended
Function 2 ended
Main ended..
[None, None, None]

If you take away the asynchronous sleep call from func1 (or replaced it with a
call to time.sleep) then it will end before func2 starts.

"""

import asyncio

async def func1():
    print("Function 1 started..")
    await asyncio.sleep(2)
    print("Function 1 ended")
 
async def func2():
    print("Function 2 started..")
    await asyncio.sleep(3)
    print("Function 2 ended")

async def func3():
    print("Function 3 started..")
    await asyncio.sleep(1)
    print("Function 3 ended")
 
async def main():
    L = await asyncio.gather(func1(), func2(), func3())
    print("Main ended..")
    print(L)
 
asyncio.run(main())
