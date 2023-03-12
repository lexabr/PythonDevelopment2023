import asyncio
import shlex
import cowsay


users = {}
user_cows = {}
cow_set = set(cowsay.list_cows())


async def handle_message(message, me, queue_me, reader, writer):
    args = shlex.split(message)

    if len(args) == 0:
        return
    elif args[0] == "login":
        if me in users:
            writer.write(f"You've already logged. Login: {user_cows[me]}\n".encode())
            await writer.drain()
        else:
            if args[1] in (cow_set - set(user_cows.values())):
                users[me] = queue_me
                user_cows[me] = args[1]

                print(f"[New user]: {args[1]}")
                writer.write("Successful registration!\n".encode())
                await writer.drain()
                await send_all(f"New user: {args[1]}")
            elif args[1] in user_cows.values():
                writer.write("Login already in use, please, choose another\n".encode())
                await writer.drain()
            else:
                writer.write("Invalid login, please, choose another\n".encode())
                await writer.drain()


async def send_all(message, except_user=None):
    for out in users.values():
        if out is not except_user:
            await out.put(message)


async def chat(reader, writer):
    me = "{}:{}".format(*writer.get_extra_info("peername"))
    queue_me = asyncio.Queue()

    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(queue_me.get())

    while not reader.at_eof():
        done, pending = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)
        for q in done:
            if q is send:
                send = asyncio.create_task(reader.readline())
                message = q.result().decode()
                await handle_message(message, me, queue_me, reader, writer)

                # for out in users.values():
                #     if out is not users[me]:
                #         await out.put(f"{me} {q.result().decode().strip()}")
            elif q is receive:
                receive = asyncio.create_task(users[me].get())
                writer.write(f"{q.result()}\n".encode())
                await writer.drain()
    send.cancel()
    receive.cancel()
    print(me, "DONE")
    del users[me]
    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(chat, "0.0.0.0", 1337)
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())