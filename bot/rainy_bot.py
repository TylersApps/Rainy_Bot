import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands

from colorama import Fore, Style, init
import asyncpraw
import random
import json
import aiohttp, asyncio

from config import reddit, cfg


# Initialize console colors
CY = Fore.CYAN
GR = Fore.GREEN
BLU = Fore.BLUE
RED = Fore.RED
RES = Style.RESET_ALL

# Initialize bot
bot = commands.Bot(command_prefix="!", intents=nextcord.Intents.all() )

test_guild_id = cfg['guild_id']
embed_color = nextcord.Colour.from_rgb(47, 49, 54)

# Sends a message to console when bot is online in server(s).
@bot.event
async def on_ready():
    print(f'\n{GR}[Logged in as {bot.user}]{RES}')


# Send a list of available commands to the channel where this command is sent.
@bot.slash_command(guild_ids=[test_guild_id], description="Get a list of Rainy Bot's commands")
async def help(interaction: Interaction):
    print(f'{CY}Help{RES} command used!')

    embed = nextcord.Embed(
        title='Rainy Bot Commands',
        description='\
            `/help` displays a list of all available commands\n\
            `/randompost <subreddit_name>` gets a random post from a specific subreddit.',
        color=embed_color
    )

    await interaction.response.send_message(embed=embed)


# Send a random post from specified subreddit as an embed
@bot.slash_command(guild_ids=[test_guild_id], description='Get a random post from a subreddit')
async def randompost(interaction: Interaction, subreddit_name: str = SlashOption(description="Subreddit Choice")):
    await interaction.response.defer()

    print(f'{CY}RandomPost{RES} command used!')

    if subreddit_name.startswith(('/r/', 'r/')):
        subreddit_name = subreddit_name.split('r/')[-1]
    
    # If specified subreddit doesn't exist, send error embed.
    try:
        subreddit = await reddit.subreddit(subreddit_name, fetch=True)
    except Exception: 
        embed = nextcord.Embed(
            description=f"r/{subreddit_name} doesn't exist.",
            color=nextcord.Colour.from_rgb(217, 95, 87)
        )
        await interaction.followup.send(embed=embed)
        return

    # Initialize submission and url variables
    submission = await subreddit.random()
    url = submission.url

    # Initialize title and shorten to max 253 characters
    title = submission.title
    if len(title) > 250:
        title = title[:250] + " ..."
    
    # Initialize post_body and shorten to max 500 characters
    post_body = submission.selftext
    if len(post_body) > 500:
        post_body = post_body[:497]
        post_body += " ..."

    # Send confirmation message
    print(f'Sending the following post from {CY}{submission.subreddit}{RES}: {submission.title}') 

    # Create embed
    embed = nextcord.Embed(
        title=title,
        url=url,
        description=post_body,
        color=embed_color
    )
    embed.set_author(name=f'r/{submission.subreddit}', url=f'https://www.reddit.com/r/{submission.subreddit}')

    if url.endswith('.jpg') or url.endswith('.png') or url.endswith('.jpeg'):
        embed.set_image(url=url)

    # Send embed to channel
    await interaction.followup.send(embed=embed)


bot.run(cfg['token'])