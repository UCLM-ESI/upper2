#!/usr/bin/env python3
# Copyright: See AUTHORS and COPYING
"Usage: {0} <host> <port> <n_clients>"

import sys
import asyncio

queries = "twenty tiny tigers take two taxis to town".split()


async def upper_client(host, port, index):
    reader, writer = await asyncio.open_connection(host, port)
    try:
        for query in queries:
            data = f"[{index:>3}] {query}".encode()
            writer.write(data)
            await writer.drain()
            reply = await reader.read(len(data))
            print("- Received: {0}".format(reply.decode()))

    except ConnectionResetError:
        print(f"Client [{index:>3}] connection lost")
        return False

    writer.close()
    await writer.wait_closed()
    return True


async def main(host, port, nclients):
    tasks = [upper_client(host, port, i) for i in range(nclients)]
    results = await asyncio.gather(*tasks)

    print('- Clients never served: {}'.format(
            results.count(False)))


if len(sys.argv) != 4:
    print(__doc__.format(sys.argv[0]))
    sys.exit(1)

try:
    asyncio.run(main(
        host=sys.argv[1],
        port=int(sys.argv[2]),
        nclients=int(sys.argv[3])))
except KeyboardInterrupt:
    pass
