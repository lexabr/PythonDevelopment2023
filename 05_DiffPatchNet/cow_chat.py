import asyncio
import shlex
import cowsay


users = {}
user_cows = {}
cows_user = {}
cow_set = set(cowsay.list_cows())


async def handle_message(message, user_context):
    args = shlex.split(message)
    if len(args) == 0:
        return
    elif args[0] == "login":
        await login(args, user_context)
    elif args[0] == 'quit':
        await user_quit(user_context)
    elif args[0] == 'who':
        await who(user_context)
    elif args[0] == 'cows':
        await cows(user_context)
    elif args[0] == 'say':
        await say(args, user_context)
    elif args[0] == 'yield':
        await yld(args, user_context)


async def login(args, user_context):
    if user_context['me'] in users:
        user_context['writer'].write(f"You've already logged. Login: {user_cows[user_context['me']]}\n".encode())
        await user_context['writer'].drain()
    else:
        if args[1] in (cow_set - set(user_cows.values())):
            users[user_context['me']] = user_context['queue']
            user_cows[user_context['me']] = args[1]
            cows_user[args[1]] = user_context['me']

            print(f"[New user]: {args[1]}")
            user_context['writer'].write("Successful registration!\n".encode())
            await user_context['writer'].drain()
            await send_all(f"New user: {args[1]}")
        elif args[1] in user_cows.values():
            user_context['writer'].write("Login already in use, please, choose another\n".encode())
            await user_context['writer'].drain()
        else:
            user_context['writer'].write("Invalid login, please, choose another\n".encode())
            await user_context['writer'].drain()


async def user_quit(user_context):
    user_context['send'].cancel()
    user_context['recieve'].cancel()

    cow = user_cows[user_context['me']]
    print(f"[Quit user]: {cow}")
    user_context['writer'].write("Good bye!\n".encode())
    await user_context['writer'].drain()

    del users[user_context['me']]
    del user_cows[user_context['me']]
    del cows_user[cow]
    await send_all(f"User {cow} left the chat")

    user_context['writer'].close()
    await user_context['writer'].wait_closed()


async def who(user_context):
    me = user_cows[user_context['me']] if user_context['me'] in users else user_context['me']
    print(f"[User {me}]: who")
    user_context['writer'].write(f"Online users: {', '.join(user_cows.values())}\n".encode())
    await user_context['writer'].drain()


async def cows(user_context):
    me = user_cows[user_context['me']] if user_context['me'] in users else user_context['me']
    print(f"[User {me}]: cows")
    user_context['writer'].write(f"Online users: {', '.join([c for c in cowsay.list_cows() if c not in user_cows.values()])}\n".encode())
    await user_context['writer'].drain()


async def say(args, user_context):
    if user_context['me'] not in users:
        user_context['writer'].write("You can't send anything before login\n".encode())
        await user_context['writer'].drain()
    elif args[1] not in cows_user:
        user_context['writer'].write("This user is not registered\n".encode())
        await user_context['writer'].drain()
    else:
        print(f"[User {user_cows[user_context['me']]}]: {' '.join(args)}")
        us = cows_user[args[1]]
        await users[us].put(f"Private message from: {user_cows[user_context['me']]}\n{cowsay.cowsay(' '.join(args[2:]).strip(), cow=user_cows[user_context['me']])}")


async def yld(args, user_context):
    if user_context['me'] not in users:
        user_context['writer'].write("You can't send anything before login\n".encode())
        await user_context['writer'].drain()
    else:
        print(f"[User {user_cows[user_context['me']]}]: {' '.join(args)}")
        await send_all(f"User: {user_cows[user_context['me']]}\n{cowsay.cowsay(' '.join(args[1:]).strip(), cow=user_cows[user_context['me']])}")


async def send_all(message, except_user=None):
    for us, out in users.items():
        if us is not except_user:
            await out.put(message)


async def chat(reader, writer):
    me = "{}:{}".format(*writer.get_extra_info("peername"))
    queue_me = asyncio.Queue()

    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(queue_me.get())

    user_context = {
        'me': me,
        'queue': queue_me,
        'send': send,
        'recieve': receive,
        'reader': reader,
        'writer': writer
    }

    while not reader.at_eof():
        done, pending = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)
        for q in done:
            if q is send:
                send = asyncio.create_task(reader.readline())
                message = q.result().decode()
                await handle_message(message, user_context)
            elif q is receive:
                receive = asyncio.create_task(users[me].get())
                writer.write(f"{q.result()}\n".encode())
                await writer.drain()


async def main():
    server = await asyncio.start_server(chat, "0.0.0.0", 1337)
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())