################################################################################
#                                                                              #
#  room_client.py                                                              #
#                                                                              #
#  This file defines a client application for the escape room leaderboard      #
#  which runs in the background on the escape room EC2 instance. It handles    #
#  the display shown in each room to show a realtime leaderboard, and sends    #
#  updates to the state daemon to update the shared state between the two      #
#  rooms.                                                                      #
#                                                                              #
#  Author: Edward Speer                                                        #
#  Date:   04/20/2025
#                                                                              #
################################################################################

################################################################################
#  IMPORTS                                                                     #
################################################################################

import asyncio
import aioconsole
import json
import sys
import os

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

ROOM = None

################################################################################
#  FUNCTIONS                                                                   #
################################################################################

"""
show_display(step_a, step_b)

This function is used to display the current leaderboard in the room. It takes
in the current step for each room and displays it in a formatted string.
"""
def show_display(step_a, step_b):
    os.system('clear')
    print("╔══════════════════════════════════════════════╗")
    print("║                                              ║")
    print("║             ESCAPE ROOM PROGRESS             ║")
    print("╠══════════════════════════════════════════════╣")
    print("║                                              ║")
    if ROOM == "A":
        print(f"║ YOU:[" + "#" * 3 * step_a + " " * 3 * (6 - step_a) + "]                     ║")
        print(f"║ OPP:[" + "#" * 3 * step_b + " " * 3 * (6 - step_b) + "]                     ║")
    else:
        print(f"║ OPP:[" + "#" * 3 * step_a + " " * 3 * (6 - step_a) + "]                     ║")
        print(f"║ YOU:[" + "#" * 3 * step_b + " " * 3 * (6 - step_b) + "]                     ║")
    print("║                                              ║")
    print("╚══════════════════════════════════════════════╝")
    
"""
send_progress(writer)

This function is used to send progress updates to the daemon running on the 
server to update the state of the leaderboard displayed in both rooms.
"""
async def send_progress(writer):
    while True:
        try:
            step_str = await aioconsole.ainput(f"[{ROOM}] Enter current step number: ")
            step = int(step_str)
            msg = json.dumps({
                "type": "progress_update",
                "room": ROOM,
                "step": step}
            ) + "\n"
            writer.write(msg.encode())
            await writer.drain()
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

"""
receive_updates(reader)

This function is used to receive updates from the daemon running on the server
and display the current state of the leaderboard in the room.
"""
async def receive_updates(reader):
    while True:
        data = await reader.readline()
        if not data:
            break
        msg = json.loads(data.decode())
        if msg["type"] == "state":
            os.system('clear')
            room_a_step = msg["data"]["A"]["step"]
            room_b_step = msg["data"]["B"]["step"]
            show_display(room_a_step, room_b_step)
            print("Enter the step completed:", end=" ", flush=True)
        else:
            print("Unknown message type received.")

################################################################################
#  MAIN EXECUTABLE                                                             #
################################################################################

async def main():
    global ROOM
    if (len(sys.argv) < 2):
        print("Usage: python3 room_client.py <room>")
        sys.exit(1)

    ROOM = sys.argv[1].upper()
    if ROOM not in ["A", "B"]:
        print("Room must be 'A' or 'B'")
        sys.exit(1)

    reader, writer = await asyncio.open_connection(LO, PORT)

    # Start up the sender and receiver
    await asyncio.gather(
        send_progress(writer),
        receive_updates(reader),
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Client stopped.")
    except Exception as e:
        print(f"Error starting client: {e}")
    finally:
        print("Client exiting.")
