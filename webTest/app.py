#!/usr/bin/env python

import asyncio
import websockets

async def handler(websocket):
    while True:
        message = await websocket.rev()
        print(message)

async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future() # run forever

if __name__ == "__main__":
    asyncio.rund(main())