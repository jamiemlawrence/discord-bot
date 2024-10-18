import discord
import os
import requests
from discord.ext import commands
from dotenv import load_dotenv

# load and extract bot token and channel id from env file
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
STRAVA_CLIENT_ID = os.getenv('STRAVA_CLIENT_ID')
STRAVA_CLIENT_SECRET = os.getenv('STRAVA_CLIENT_SECRET')
STRAVA_REFRESH_TOKEN = os.getenv('STRAVA_REFRESH_TOKEN')

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

def get_strava_access_token():
    response = requests.post(
        url="https://www.strava.com/oauth/token",
        data={
            'client_id': STRAVA_CLIENT_ID,
            'client_secret': STRAVA_CLIENT_SECRET,
            'refresh_token': STRAVA_REFRESH_TOKEN,
            'grant_type': 'refresh_token',
        }
    )
    return response.json()['access_token']

def get_latest_activity():
    access_token = get_strava_access_token()
    response = requests.get(
        url="https://www.strava.com/api/v3/athlete/activities",
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )
    
    # Check the response status code
    if response.status_code != 200:
        print(f"Error fetching activities: {response.status_code}, {response.text}")
        return None

    activities = response.json()
    
    # Debugging: Log activities to see the response
    print(f"Strava API response: {activities}")
    
    # Check if activities list is not empty
    if len(activities) > 0:
        return activities[0]  # Return the latest activity
    else:
        print("No activities found.")
        return None

@bot.event
async def on_ready():
    print('Bot is ready!')
    channel = bot.get_channel(CHANNEL_ID)

    # Fetch latest activity from Strava
    latest_activity = get_latest_activity()

    if latest_activity is not None:
        activity_name = latest_activity['name']
        activity_distance = latest_activity['distance']
        activity_time = latest_activity['moving_time']

        message = f"🚴‍♂️ Just finished a ride!\n**{activity_name}**\nDistance: {activity_distance} meters\nTime: {activity_time} seconds"
    else:
        message = "No recent activities found."

    await channel.send(message)

bot.run(BOT_TOKEN)
