# If you had to build automation to confirm the Room API is able to create a room, how would you do it?

import requests
import unittest
import random

# Create a request to log in as an admin using the Auth API and save the Cookie that comes back in

payload_auth = {
  "username": "admin",
  "password": "password"
}

response_auth = requests.post("https://automationintesting.online/auth/login", json=payload_auth)

print(response_auth.status_code)
print(response_auth.content)

cookies_token=response_auth.cookies

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

response_room = requests.post("https://automationintesting.online/room/", json=payload_room, cookies=cookies_token)

print(response_room.status_code)
print(response_room.content)

# TODO room/ vs room??

# Assert that the room has been created and contains expected room details

tests = unittest.TestCase()
tests.assertEqual(response_room.status_code, 201, "status code is CREATED")
tests.assertEqual(response_room.json()["roomName"], roomName, "name is as set")

# Get the rooms from the server; check that our room exists

response_room_list = requests.get("https://automationintesting.online/room/", cookies=cookies_token)

print(response_room_list.status_code)
print(response_room_list.content)

room_list = response_room_list.json()["rooms"]

found_room = False
for room in room_list:
    if room["roomName"] == roomName:
        print(room)
        found_room = True

tests.assertTrue(found_room, "our room was created")



