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
#  Date:   04/20/2025                                                          #
#                                                                              #
################################################################################

################################################################################
#  IMPORTS                                                                     #
################################################################################

import asyncio
import json
import os
import sys
# import threading
# import queue

from print_util import PrintQ

################################################################################
#  CONSTANTS                                                                   #
################################################################################

LO = '127.0.0.1'            # Address for local loopback interface
PORT = 5000                 # Port for the server to listen on
NUM_PINS = 4                # Number of pins in the lock
ROOM = None                 # Will be set to 'A' or 'B' via CLI args

CODES = ["WEIRDDONKEY", "SWISS", "SHRONKYOU", "TRINITY"]

################################################################################
#  GLOBALS                                                                     #
################################################################################

print_queue = PrintQ()  # Thread-safe print queue for display output

step = 0 # Current step in the lock override process

used_codes = [] # List of codes already used by player

def safe_print(msg=""):
    print_queue.put(msg)

################################################################################
#  INPUT FUNCTION                                                              #
################################################################################

async def ainput(prompt=''):
    safe_print(prompt)
    return await asyncio.get_event_loop().run_in_executor(None, input)

################################################################################
#  DISPLAY FUNCTION                                                            #
################################################################################

def show_display(step_a, step_b):
    os.system('cls' if os.name == 'nt' else 'clear')
    lines = []
    lines.append("╔════════════════════════════════════════════════╗")
    lines.append("║                                                ║")
    lines.append("║              DOOR OVERRIDE STATUS              ║")
    lines.append("╠════════════════════════════════════════════════╣")
    lines.append("║                                                ║")
    own_step = step_a if ROOM == "A" else step_b
    other_step = step_b if ROOM == "A" else step_a
    for i in range(NUM_PINS):
        if i < own_step:
            lines.append("║ ⚙━━                               ━━⚙ [CLEAR]  ║")
        else:
            lines.append("║ ⚙━━┄┄┄◉┄┄┄◉┄┄┄◉┄┄┄◉┄┄┄◉┄┄┄◉┄┄┄◉┄┄┄━━⚙ [LOCKED] ║")
        lines.append("║                                                ║")
    lines.append("╠════════════════════════════════════════════════╣")
    lines.append("║                                                ║")
    lines.append("║         OPPONENT DOOR OVERRIDE STATUS          ║")
    lines.append("╠════════════════════════════════════════════════╣")
    lines.append("║                                                ║")
    for i in range(NUM_PINS):
        if i < other_step:
            lines.append("║ ⚙━━                               ━━⚙ [CLEAR]  ║")
        else:
            lines.append("║ ⚙━━┄┄┄◉┄┄┄◉┄┄┄◉┄┄┄◉┄┄┄◉┄┄┄◉┄┄┄◉┄┄┄━━⚙ [LOCKED] ║")
        lines.append("║                                                ║")
    if own_step == NUM_PINS:
        lines.append("╠════════════════════════════════════════════════╣")
        lines.append("║                                                ║")
        lines.append("║   CONGRATULATIONS! YOU HAVE UNLOCKED THE DOOR! ║")
        lines.append("║                                                ║")
        lines.append("╚════════════════════════════════════════════════╝")
    else:
        lines.append("╚════════════════════════════════════════════════╝")
        lines.append("ENTER DUNGEON OVERRIDE CODE: ")
    for line in lines:
        safe_print(line)

################################################################################
#  NETWORK COROUTINES                                                          #
################################################################################

async def send_progress(writer):
    global step
    show_display(0, 0)
    while True:
        try:
            pass_str = await ainput(f"")
            if pass_str in CODES and pass_str not in used_codes:
                used_codes.append(pass_str)
                step += 1

                msg = json.dumps({
                    "type": "progress_update",
                    "room": ROOM,
                    "step": step
                }) + "\n"
                writer.write(msg.encode())
                await writer.drain()
            else:
                safe_print(f"Invalid code or already used: {pass_str}")
                continue
        except Exception as e:
            safe_print(f"[send_progress] error: {e}")
            break

async def receive_updates(reader):
    while True:
        try:
            data = await reader.readline()
            if not data:
                safe_print("[receive_updates] connection closed.")
                break
            msg = json.loads(data.decode())
            if msg["type"] == "state":
                a = msg["data"]["A"]["step"]
                b = msg["data"]["B"]["step"]
                show_display(a, b)
            else:
                safe_print("[receive_updates] unknown message type")
        except Exception as e:
            safe_print(f"[receive_updates] error: {e}")
            break

################################################################################
#  MAIN EXECUTABLE                                                             #
################################################################################

async def main():
    global ROOM
    if len(sys.argv) < 2:
        safe_print("Usage: python3 room_client.py <room>")
        sys.exit(1)

    ROOM = sys.argv[1].upper()
    if ROOM not in ["A", "B"]:
        safe_print("Room must be 'A' or 'B'")
        sys.exit(1)

    try:
        reader, writer = await asyncio.open_connection(LO, PORT)
    except Exception as e:
        safe_print(f"[main] Failed to connect to daemon: {e}")
        return

    try:
        send_task = asyncio.create_task(send_progress(writer))
        recv_task = asyncio.create_task(receive_updates(reader))

        done, pending = await asyncio.wait(
            [send_task, recv_task],
            return_when=asyncio.FIRST_EXCEPTION
        )

        for task in done:
            if task.exception():
                safe_print(f"[main] Task failed: {task.exception()}")
            else:
                safe_print("[main] Task completed normally.")

        for task in pending:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass

    except Exception as e:
        safe_print(f"[main] Unexpected top-level error: {e}")
    finally:
        try:
            writer.close()
            await writer.wait_closed()
        except Exception as e:
            safe_print(f"[main] Error during writer shutdown: {e}")

        safe_print("Client exiting.")
        print_queue.put(None)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print_queue.put("Keyboard interrupt. Exiting.")
        print_queue.shutdown()
