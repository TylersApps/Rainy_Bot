import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands

from colorama import Fore, Style, init
import asyncpraw
import json
import aiohttp, asyncio
from random import randint

from config import reddit, cfg


# Initialize console colors
CY = Fore.CYAN
GR = Fore.GREEN
BLU = Fore.BLUE
RED = Fore.RED
YLW = Fore.YELLOW
RES = Style.RESET_ALL

# Initialize bot
bot = commands.Bot(command_prefix="!", intents=nextcord.Intents.all() )

test_guild_id = cfg['guild_id']
embed_color = nextcord.Colour.from_rgb(47, 49, 54)
error_color = nextcord.Colour.from_rgb(217, 95, 87)

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
            `/randompost <subreddit_name>` gets a random post from a specific subreddit.\n\
            `/roll <(x)d(y)>` rolls x dice with y sides (e.g. "/roll 4d6" rolls 4 6-sded dice)',
        color=embed_color
    )

    embed.set_thumbnail(url='https://i.imgur.com/bhbTUOe.png')

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
            title='Invalid input',
            description=f"r/{subreddit_name} doesn't exist.",
            color=error_color
        )
        await interaction.followup.send(embed=embed)
        print(f'{RED}Invalid subreddit input{RES}')
        return

    # Initialize submission and url variables
    submission = await subreddit.random()
    url = submission.url
    permalink = f'https://www.reddit.com{submission.permalink}'

    # Initialize title and shorten to max 253 characters
    title = submission.title
    if len(title) > 250:
        title = title[:250] + " ..."
    
    # Initialize post_body and shorten to max 500 characters
    post_body = submission.selftext
    if len(post_body) > 500:
        post_body = post_body[:497]
        post_body += " ..." 

    # Create embed
    embed = nextcord.Embed(
        title=title,
        url=permalink,
        description=post_body,
        color=embed_color
    )
    embed.set_author(name=f'r/{submission.subreddit}', url=f'https://www.reddit.com/r/{submission.subreddit}')

    if url.endswith('.jpg') or url.endswith('.png') or url.endswith('.jpeg'):
        embed.set_image(url=url)

    # Send embed to channel
    await interaction.followup.send(embed=embed) 

    # Send confirmation message
    print(f'Sent post from {YLW}{submission.subreddit}{RES}: {submission.title}')


# Send the definition of the specified word
@bot.slash_command(guild_ids=[test_guild_id], description='Get the definition of a word')
async def define(interaction: Interaction, word: str = SlashOption(description="Word to define")):
    print(f'{CY}Define{RES} command used!')

    api_url = f"http://api.dictionaryapi.dev/api/v2/entries/en/{word}"

    embed = nextcord.Embed(
        color=embed_color,
        title=f'Definition of "{word.lower()}":',
    )

    # Get the json data for the specified word
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, ssl=False) as resp:
                data = await resp.json()
    except Exception as ex: 
        print(f'{RED}[ERROR]: {ex}{RES}')
        return
    
    content = data[0]['meanings']

    for item in content:
        print(item['definitions'][0])


    await interaction.response.send_message(embed=embed)
    
    # Send confirmation message
    print(f'Sent definition of {YLW}{word}{RES}!')


# Roll die or dice based on input
@bot.slash_command(guild_ids=[test_guild_id], description='Roll a specific amount of dice with a specific amount of sides.')
async def roll(interaction: Interaction, dice: str=SlashOption(description="Specified dice")):
    print(f'{CY}Roll{RES} command used!')

    # Initialize function variables
    dice = dice.lower()
    dice_split = dice.split('d')
    total = 0

    # Initialize embed with default embed color
    embed = nextcord.Embed(color=embed_color)

    # Check for invalid input
    if len(dice_split) != 2 or dice.isalpha() or dice.isnumeric():
        embed.title='Invalid input'
        embed.description='`dice` input should be formatted like **2D20** or **1D4**'
        embed.color=error_color

        print(f'{RED}Invalid dice input{RES}')
    else:
        num_rolls = int(dice_split[0])
        num_sides = int(dice_split[1])

        # Roll dice and get total of all rolls
        for x in range(num_rolls):
            total += randint(0, num_sides)

        # Update embed with dice and total
        embed.title = f'Rolled {dice}'
        embed.description = f'Outcome: **{total}**'

        print(f'Rolled {YLW}{dice}{RES} for a total of {YLW}{total}{RES}!')


    await interaction.response.send_message(embed=embed)
    



bot.run(cfg['token'])