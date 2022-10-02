# Can multiple rooms be made in short succession?

import requests
import unittest
import random

# Create a request to log in as an admin using the Auth API and save the Cookie that comes back in
payload_auth = {
  "username": "admin",
  "password": "password"
}

response_auth = requests.post("https://automationintesting.online/auth/login", json=payload_auth)
cookies_token=response_auth.cookies

# Loop on room creation
list_of_created_rooms = []
number_of_rooms = 10

for create_attempt in range(0, number_of_rooms):

    # Send a POST request to the Room API
    roomName = str(random.randint(0,1000000))

    payload_room = {
    "roomName": roomName,
    "type": "Suite",
    "accessible": True,
    "image": "https://blog.postman.com/wp-content/uploads/2014/07/logo.png",
    "description": "This is room 101, dare you enter?",
    "roomPrice": 100,
    "features": [
        "WiFi", "Safe"
    ]
    }

    # TODO room/ vs room??
    response_room = requests.post("https://automationintesting.online/room/", json=payload_room, cookies=cookies_token)

    # Assert that the room has been created and contains expected room details
    tests = unittest.TestCase()
    tests.assertEqual(response_room.status_code, 201, "status code is CREATED")
    tests.assertEqual(response_room.json()["roomName"], roomName, "name is as set")
    list_of_created_rooms.append(roomName)

print(list_of_created_rooms)

# Get the rooms from the server; check that our rooms exist
response_room_list = requests.get("https://automationintesting.online/room/", cookies=cookies_token)
room_list = response_room_list.json()["rooms"]

for created_room in list_of_created_rooms:
    found_room = False
    for room in room_list:
        if room["roomName"] == created_room:
            found_room = True

    tests.assertTrue(found_room, created_room + " room was created")