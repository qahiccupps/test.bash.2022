# Can multiple rooms be made in parallel?

import requests
import unittest
import random
import asyncio
from datetime import date, datetime

# make a room and check the server response for success
def make_a_room(roomName):
    global cookies_token

    payload_room = {
    "roomName": roomName,
    "type": "Suite",
    "accessible": True,
    "roomPrice": 100 
    }

    response_room = requests.post("https://automationintesting.online/room/", json=payload_room, cookies=cookies_token)

    tests = unittest.TestCase()
    tests.assertEqual(response_room.status_code, 201, "status code is CREATED")
    tests.assertEqual(response_room.json()["roomName"], roomName, "name is as set")

# given a list of room names, compare them to what the server reports exists
def check_rooms_exist(room_names_to_create):
    response_room_list = requests.get("https://automationintesting.online/room/", cookies=cookies_token)
    rooms_on_the_server = response_room_list.json()["rooms"]

    for test_room in room_names_to_create:
        found_room = False
        for room in rooms_on_the_server:
            if room["roomName"] == test_room:
                found_room = True

        print(test_room, found_room)

# === main ===

# Create a request to log in as an admin using the Auth API and save the Cookie that comes back in
payload_auth = {
  "username": "admin",
  "password": "password"
}

response_auth = requests.post("https://automationintesting.online/auth/login", json=payload_auth)
cookies_token=response_auth.cookies

# make a list of room names, using timestamp as a run identifier
# https://pynative.com/python-iso-8601-datetime/
room_names_to_create = []
number_of_rooms = 7
timestamp=datetime.now().isoformat()
for i in range(0,number_of_rooms):
    room_names_to_create.append(timestamp+"__"+str(random.randint(0,1000000)))

# call the API to make rooms in parallel
# https://stackoverflow.com/questions/43448042/parallel-post-requests-using-multiprocessing-and-requests-in-python
loop = asyncio.get_event_loop()
for room_name in room_names_to_create:
    loop.run_in_executor(None, make_a_room, room_name)

# Get the rooms from the server; check that our rooms exist ... twice
print("---- attempt 1 ----")
check_rooms_exist(room_names_to_create)

print("---- attempt 2 ----")
check_rooms_exist(room_names_to_create)

