import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from os import getenv
from time import sleep

from discord.ext import commands
import discord

load_dotenv()

discord_client_secret = getenv("DISCORD_CLIENT_SECRET")
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


# results = sp.search(q='weezer', limit=20)

# print(results)
# print("Number of tracks:", len(results['tracks']['items']))
# for idx, track in enumerate(results['tracks']['items']):
#     print(idx, track['name'])

# x = sp.user('4cbdkhwgf34wtzfq6pkmwo9ik')
# print(x)
# print(x['followers']['total'])

# y = sp.album('https://open.spotify.com/album/1NAmidJlEaVgA3MpcPFYGq?si=Lr8Xb_9qSg6LkkeT2mSOUw')
# print(y)

# z = sp.add_to_queue("https://open.spotify.com/track/0FIDCNYYjNvPVimz5icugS?si=fab28a48287342c0")
# print(z)

@bot.event
async def on_ready():
    q = sp.search(q='Bunkurs 13',type='track', limit=1)
    print(q)


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
async def squeue(ctx, *, name):
    try:
        song_data = sp.search(q=name, type='track', limit=1)
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
async def unpause(ctx):
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
        # track = track['track']
        queue_songs += f"{track['name']} by {track['artists'][0]['name']}\n"

    embeded = discord.Embed(
        title = "List of songs in the queue:",
        description = queue_songs,
        color=discord.Color.green()
    )
    await ctx.send(embed=embeded)



bot.run(discord_client_secret)