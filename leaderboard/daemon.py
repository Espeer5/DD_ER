################################################################################
#                                                                              #
#  daemon.py                                                                   #
#                                                                              #
#  This file defines a daemon for the escape room leaderboard application      #
#  which runs in the background on the escape room EC2 instance. It handles    #
#  the shared state between the two rooms in order to provide progress bars    #
#  to each room in the client applications to show a realtime leaderboard.     #
#                                                                              #
#  Author: Edward Speer                                                        #
#  Date:   04/21/2025                                                          #
#                                                                              #
################################################################################

################################################################################
#  IMPORTS                                                                     #
################################################################################

import asyncio
import json
from datetime import datetime

from print_util import PrintQ

################################################################################
#  CONSTANTS                                                                   #
################################################################################

# The address to the local loopback interface
LO = '127.0.0.1'

# The port for the server to listen on
PORT = 5000

################################################################################
#  GLOBALS                                                                     #
################################################################################

# The current status of each room and when it was last updated
STATE = {
    "A": {"step": 0, "last_updated": None},
    "B": {"step": 0, "last_updated": None},
}

# The set of connected client applications—should total 2
CLIENTS = set()

# Printing queue for non-blocking printing
PRINTQ = PrintQ()

################################################################################
#  FUNCTIONS                                                                   #
################################################################################

"""
handle_client(reader, writer)

For each client application connected from each of the escape rooms, monitors
the client's progress and maintains the shared state between the two rooms.
"""
async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    CLIENTS.add(writer)
    PRINTQ.put(f"Client connected from {addr}")

    try:
        while True:
            data = await reader.readline()
            if not data:
                break
            msg = json.loads(data.decode())

            if msg["type"] == "progress_update":
                room = msg["room"]
                step = msg["step"]
                STATE[room]["step"] = step
                STATE[room]["last_updated"] = datetime.now().isoformat()

                await broadcast_state()

    except Exception as e:
        PRINTQ.put(f"Error handling client {addr}: {e}")

    finally:
        CLIENTS.remove(writer)
        writer.close()
        await writer.wait_closed()
        PRINTQ.put(f"Client disconnected from {addr}")

"""
broadcast_state()

Broadcasts the current shared state of the rooms to all connected clients. Will
be called whenever the state is updated by any client.
"""
async def broadcast_state():
    state_json = json.dumps({"type": "state", "data": STATE}) + "\n"
    for client in CLIENTS:
        try:
            client.write(state_json.encode())
            await client.drain()
        except Exception as e:
            continue


################################################################################
#  MAIN EXECUTABLE                                                             #
################################################################################

async def main():
    server = await asyncio.start_server(handle_client, LO, PORT)
    PRINTQ.put(f"Daemon started on localhost:{PORT}")
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        PRINTQ.put("Daemon stopped.")
    except Exception as e:
        PRINTQ.put(f"Error starting daemon: {e}")
    finally:
        for client in CLIENTS:
            client.close()
        PRINTQ.put("All clients disconnected.")
