"""Compares how early two local signals report that agent select has started.

Run this, then queue for a match. It only reads from the local Riot Client, and
it never picks or locks an agent:

    .venv\\Scripts\\python.exe -m pip install websocket-client
    .venv\\Scripts\\python.exe tools\\detection_probe.py

For each match it prints when polling and the websocket each saw PREGAME.
Press Ctrl+C to stop.
"""
import base64
import json
import os
import ssl
import threading
import time

import requests
import urllib3
import websocket

urllib3.disable_warnings()

POLL_DELAY = 0.01
LOCKFILE = os.path.expandvars(r"%LOCALAPPDATA%\Riot Games\Riot Client\Config\lockfile")


def read_lockfile():
    with open(LOCKFILE, encoding="utf-8") as file:
        _, _, port, password, _ = file.read().split(":")
    return port, password


def loop_state(presence):
    """Return the session state in one presence entry, or None."""
    try:
        private = json.loads(base64.b64decode(presence["private"]))
        return private["matchPresenceData"]["sessionLoopState"]
    except (KeyError, TypeError, ValueError):
        return None


class Race:
    """Remembers when each source first saw PREGAME in the current match."""

    def __init__(self):
        self.lock = threading.Lock()
        self.seen = {}

    def report(self, source, state):
        now = time.perf_counter()
        with self.lock:
            if state != "PREGAME":
                self.seen.clear()
            elif source not in self.seen:
                self.seen[source] = now
                if len(self.seen) == 2:
                    gap = (self.seen["websocket"] - self.seen["poll"]) * 1000
                    winner = "poll" if gap > 0 else "websocket"
                    print(f"PREGAME: {winner} was first by {abs(gap):.0f} ms")


def own_puuid(session, base):
    return session.get(base + "/chat/v1/session", timeout=5).json()["puuid"]


def poll(race, session, base, puuid):
    while True:
        presences = session.get(base + "/chat/v4/presences", timeout=5).json().get("presences", [])
        for presence in presences:
            if presence.get("puuid") == puuid:
                state = loop_state(presence)
                if state:
                    race.report("poll", state)
                break
        time.sleep(POLL_DELAY)


def listen(race, port, password, puuid):
    token = base64.b64encode(f"riot:{password}".encode()).decode()
    socket = websocket.create_connection(
        f"wss://127.0.0.1:{port}", header=[f"Authorization: Basic {token}"],
        sslopt={"cert_reqs": ssl.CERT_NONE})
    socket.send(json.dumps([5, "OnJsonApiEvent_chat_v4_presences"]))
    print("Websocket connected. Queue for a match now.")
    while True:
        message = socket.recv()
        if not message:
            continue
        event = json.loads(message)
        for presence in event[2]["data"].get("presences", []):
            if presence.get("puuid") == puuid:
                state = loop_state(presence)
                if state:
                    race.report("websocket", state)


def main():
    port, password = read_lockfile()
    base = f"https://127.0.0.1:{port}"
    session = requests.Session()
    session.auth = ("riot", password)
    session.verify = False
    puuid = own_puuid(session, base)
    race = Race()
    threading.Thread(target=poll, args=(race, session, base, puuid), daemon=True).start()
    listen(race, port, password, puuid)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
