# import discord
import os
import json
# from discord.ext import commands
from dotenv import load_dotenv


# load and extract bot token and channel id from env file
load_dotenv()
# BOT_TOKEN = os.getenv('BOT_TOKEN')
# CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
STRAVA_CLIENT_ID = os.getenv('STRAVA_CLIENT_ID')
STRAVA_CLIENT_SECRET = os.getenv('STRAVA_CLIENT_SECRET')
STRAVA_REFRESH_TOKEN = os.getenv('STRAVA_REFRESH_TOKEN')

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

auth_url = "https://www.strava.com/api/v3/oauth/token"
activities_url = "https://www.strava.com/api/v3/athlete/activities"

payload = {
    'client_id': STRAVA_CLIENT_ID,
    'client_secret': STRAVA_CLIENT_SECRET,
    'refresh_token': STRAVA_REFRESH_TOKEN,
    'grant_type': "refresh_token",
    'f': 'json'
}

# print("Requesting the token...")

res = requests.post(auth_url, data=payload, verify=False)
access_token = res.json().get('access_token')
# print("Access Token = {}".format(access_token))

header = {'Authorization': 'Bearer ' + access_token}
param = {'per_page': 1, 'page': 1}
print("Fetching activities...")
my_dataset = requests.get(activities_url, headers=header, params=param).json()

# print(my_dataset[0])

distance_miles = round((my_dataset[0]['distance']/1000)*0.62137, 2)
elevation_feet = round((my_dataset[0]['total_elevation_gain'])*3.28084, 1)
avg_speed = round((my_dataset[0]['average_speed'])*2.23694, 1)

print("Title: " + my_dataset[0]['name'])
print("Type: " + my_dataset[0]['type'])
print("Distance: " + str(distance_miles) + " miles")
print("Elevation Gain: " + str(elevation_feet) + " feet")
print("Average Speed: " + str(avg_speed) + "mph")











#bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

#def get_latest_activity():
    

# @bot.event
# async def on_ready():
#     print('Bot is ready!')
#     channel = bot.get_channel(CHANNEL_ID)

#     # Fetch latest activity from Strava
#     latest_activity = get_latest_activity()

#     if latest_activity is not None:
#         activity_name = latest_activity['name']
#         activity_distance = latest_activity['distance']
#         activity_time = latest_activity['moving_time']

#         message = f"🚴‍♂️ Just finished a ride!\n**{activity_name}**\nDistance: {activity_distance} meters\nTime: {activity_time} seconds"
#     else:
#         message = "No recent activities found."

#     await channel.send(message)

# bot.run(BOT_TOKEN)
