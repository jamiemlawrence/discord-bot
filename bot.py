import discord
import os
import json
from discord.ext import commands
from dotenv import load_dotenv
import requests
import urllib3

# load and extract bot token and channel id from env file
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
STRAVA_CLIENT_ID = os.getenv('STRAVA_CLIENT_ID')
STRAVA_CLIENT_SECRET = os.getenv('STRAVA_CLIENT_SECRET')
STRAVA_REFRESH_TOKEN = os.getenv('STRAVA_REFRESH_TOKEN')
auth_url = "https://www.strava.com/api/v3/oauth/token"
activities_url = "https://www.strava.com/api/v3/athlete/activities"
payload = {
    'client_id': STRAVA_CLIENT_ID,
    'client_secret': STRAVA_CLIENT_SECRET,
    'refresh_token': STRAVA_REFRESH_TOKEN,
    'grant_type': "refresh_token",
    'f': 'json'
}
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print('Bot is ready!')
    channel = bot.get_channel(CHANNEL_ID)
    message = 'Bot is online!'
    await channel.send(message)

#request most updated access token
res = requests.post(auth_url, data=payload, verify=False)
access_token = res.json().get('access_token')
header = {'Authorization': 'Bearer ' + access_token}
param = {'per_page': 1, 'page': 1}

@bot.command()
async def strava(ctx):
    print("Fetching activities...")
    # Using updated access token, get user activity
    my_dataset = requests.get(activities_url, headers=header, params=param).json()

    distance_miles = round((my_dataset[0]['distance']/1000)*0.62137, 2)
    elevation_feet = round((my_dataset[0]['total_elevation_gain'])*3.28084, 1)
    avg_speed = round((my_dataset[0]['average_speed'])*2.23694, 1)

    title = my_dataset[0]['name']
    activity_type = my_dataset[0]['type']
    distance = str(distance_miles)
    elevation = str(elevation_feet)
    avg_speed = str(avg_speed)

    response = (
        "Here is the latest activity!\n"
        f"Title: {title}\n"
        f"Type: {activity_type}\n"
        f"Distance: {distance} miles\n"
        f"Elevation Gain: {elevation} feet\n"
        f"Average Speed: {avg_speed} mph"
    )

    await ctx.send(response)

bot.run(BOT_TOKEN)
