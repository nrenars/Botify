import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from os import getenv
from time import sleep
import random
from discord.ext import commands
import discord

load_dotenv()

DISCORD_CLIENT_SECRET = getenv("DISCORD_CLIENT_SECRET")
CLIENT_ID = getenv("CLIENT_ID")
CLIENT_SECRET = getenv("CLIENT_SECRET")

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri="http://127.0.0.1:8080",
    scope="user-modify-playback-state user-read-playback-state user-read-recently-played"
))

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)
bot.remove_command('help') 


HELP_MESSAGE = """
```Command           | Action                             | Example 
------------------| -----------------------------------|---------------
/queue            | Add a song to queue using an url   | /queue https://open.spotify.com/track/xyz
/squeue           | Add a song to queue by using a     | /squeue Never Gonna Give You Up
                  | song name                          | 
/aqueue           | Add a random top track from an     | /aqueue Ed Sheeran
                  | artist to the queue                |
/account          | Show account info                  | /account
/pause            | Pause                              | /pause
/resume           | Unpause                            | /resume
/song             | Show info about a currently        | /song
                  | playing song                       |
/history          | Show 10 most recently played songs | /history
/skip             | Skip to the next song in the queue | /skip
/back             | Play previous song                 | /back
/volume           | Change the volume of a currently   | /volume 50
                  | playing song                       | 
/upcoming         | Show all of the songs that are in  | /upcoming
                  | the queue                          |
/help             | Show this help message             | /help
```
"""

@bot.event
async def on_ready():
    print("Botify is ready!")

@bot.event
async def on_guild_join(ctx):
    await ctx.send(HELP_MESSAGE)

@bot.command()
async def queue(ctx, url):
    try:
        sp.add_to_queue(url)
        song = sp.track(url)
        embeded = discord.Embed(
            title = f"{song['name']} by {song['artists'][0]['name']}",
            description = "Added to queue",
            color=discord.Color.green())
        img = song['album']['images'][0]['url']
        embeded.set_image(url=img)
    except Exception as e:
        print(e)
    await ctx.send(embed=embeded)

@bot.command()
async def squeue(ctx, *, song_name):
    try:
        song_data = sp.search(q=song_name, type='track', limit=1)
        song = song_data['tracks']['items'][0]
        song_uri = song['uri']
        sp.add_to_queue(song_uri)
        embeded = discord.Embed(
            title = f"{song['name']} by {song['artists'][0]['name']}",
            description = "Added to queue",
            color=discord.Color.green())
        img = song['album']['images'][0]['url']
        embeded.set_image(url=img)
    except Exception as e:
        print(e)
    await ctx.send(embed=embeded)

@bot.command()
async def aqueue(ctx, *, artist_name):
    try:
        artist_data = sp.search(q=artist_name, type='artist', limit=1)
        artist_id = artist_data['artists']['items'][0]['id']
        top_tracks_data = sp.artist_top_tracks(artist_id)
        random_track_data = top_tracks_data['tracks'][random.randint(0, top_tracks_data['tracks'])]
        random_track_uri = random_track_data['uri']
        sp.add_to_queue(random_track_uri)

        embeded = discord.Embed(
            title = f"{random_track_data['name']} by {random_track_data['artists'][0]['name']}",
            description = "Added to queue",
            color=discord.Color.green())
        img = random_track_data['album']['images'][0]['url']
        embeded.set_image(url=img)
        await ctx.send(embed=embeded)
    except Exception as e:
        print(e)


@bot.command()
async def account(ctx):
    me = sp.current_user()
    img = me['images'][0]['url']
    embeded = discord.Embed(
        title=me['display_name'], 
        description=f"Followers: {me['followers']['total']}", 
        color=discord.Color.green())
    embeded.set_image(url=img)
    await ctx.send(embed=embeded)

@bot.command()
async def pause(ctx):
    sp.pause_playback()
    song = sp.currently_playing()
    await ctx.send(f"Paused {song['item']['name']} by {song['item']['artists'][0]['name']}")

@bot.command()
async def resume(ctx):
    song = sp.currently_playing()
    if song['is_playing']:
        pass
    else:
        sp.start_playback()
        print(song)
        await ctx.send(f"Playing {song['item']['name']} by {song['item']['artists'][0]['name']}")

@bot.command()
async def song(ctx):
    playing = sp.current_playback()
    embeded = discord.Embed(
        title = playing['item']['name'],
        description = f"{playing['item']['artists'][0]['name']}",
        color=discord.Color.green()
    )
    img = playing['item']['album']['images'][0]['url']
    embeded.set_image(url=img)
    await ctx.send(embed=embeded)

@bot.command()
async def history(ctx):
    last = sp.current_user_recently_played(limit=10)
    last_songs = ""
    for item in last['items']:
        track = item['track']
        last_songs += f"{track['name']} by {track['artists'][0]['name']}\n"

    embeded = discord.Embed(
        title = "Previous 10 songs:",
        description = last_songs
    )

    await ctx.send(embed=embeded)

@bot.command()
async def skip(ctx):
    sp.next_track()
    sleep(1)
    playing = sp.current_playback()
    embeded = discord.Embed(
        title = f"Skipped to {playing['item']['name']}",
        description = f"{playing['item']['artists'][0]['name']}",
        color=discord.Color.green()
    )
    img = playing['item']['album']['images'][0]['url']
    embeded.set_image(url=img)
    await ctx.send(embed=embeded)

@bot.command()
async def volume(ctx, volume):
    volume = int(volume)
    sp.volume(volume)
    await ctx.send(f"Volume set to {volume}%")

@bot.command()
async def back(ctx):
    sp.previous_track()
    sleep(1)
    playing = sp.current_playback()
    embeded = discord.Embed(
        title = f"Skipped to {playing['item']['name']}",
        description = f"{playing['item']['artists'][0]['name']}",
        color=discord.Color.green()
    )
    img = playing['item']['album']['images'][0]['url']
    embeded.set_image(url=img)
    await ctx.send(embed=embeded)

@bot.command()
async def upcoming(ctx):
    songs = sp.queue()
    queue_songs = ""
    for track in songs['queue']:
        queue_songs += f"{track['name']} by {track['artists'][0]['name']}\n"

    embeded = discord.Embed(
        title = "List of songs in the queue:",
        description = queue_songs,
        color=discord.Color.green(),
    )
    await ctx.send(embed=embeded)

@bot.command()
async def help(ctx):
    await ctx.send(HELP_MESSAGE)

bot.run(DISCORD_CLIENT_SECRET)