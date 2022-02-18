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
bot = commands.Bot(command_prefix="~", intents=nextcord.Intents.all() )

test_guild_id = cfg['guild_id']
embed_color = nextcord.Colour.from_rgb(47, 49, 54)
error_color = nextcord.Colour.from_rgb(217, 95, 87)

error_embed = nextcord.Embed(
    title='Error',
    color=error_color
)
embed = nextcord.Embed(color=embed_color)

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
            `/help` - display a list of available commands\n\
            `/randompost <subreddit_name>` - get random post from subreddit\n\
            `/roll <(x)d(y)>` - rolls x dice, each with y sides\n\
            `/define <word>` - define a word (English only)',
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
        error_embed.description=f"r/{subreddit_name} doesn't exist.",

        await interaction.followup.send(embed=error_embed)
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


    # Customize embed
    embed.title = title
    embed.url = permalink
    embed.description = post_body
    embed.set_author(name=f'r/{submission.subreddit}', url=f'https://www.reddit.com/r/{submission.subreddit}')
    if url.endswith('.jpg') or url.endswith('.png') or url.endswith('.jpeg'): 
        embed.set_image(url=url)
    # embed.set_thumbnail(
    #     url='https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/apple/285/alien_1f47d.png'
    # )


    # Send embed
    await interaction.followup.send(embed=embed) 

    # Send confirmation message
    print(f'Sent post from {YLW}{submission.subreddit}{RES}: {submission.title}')


# Send the definition of the specified word
@bot.slash_command(guild_ids=[test_guild_id], description='Get the definition of a word')
async def define(interaction: Interaction, word: str = SlashOption(description="Word to define")):
    print(f'{CY}Define{RES} command used!')

    api_url = f"http://api.dictionaryapi.dev/api/v2/entries/en/{word}"

    # Get the json data for the specified word
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, ssl=False) as resp:
                data = await resp.json()
    except Exception as ex: 
        error_embed.description = f'API Error. Please contact developer.'
        await interaction.response.send_message(embed=error_embed) 
        print(f'{RED}[ERROR]: {ex}{RES}')
        return
    
    try:
        content = data[0]['meanings']
    except KeyError: # Send error embed if the word isn't found
        error_embed.description = f'Can\'t find "{word}" in dictionary'
        await interaction.response.send_message(embed=error_embed)
        print(f'{RED}Can\'t find "{word}" in dictionary.{RES}')
        return

    
    # Customize embed with title and thumbnail   
    embed.title=f'"{word.lower().capitalize()}"'
    embed.set_thumbnail(
        url='https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/apple/285/open-book_1f4d6.png'
    )

    # Iterate through and create fields
    for item in content:
        part_of_speech = item['partOfSpeech']
        combined_definitions = ''

        for subitem in item['definitions'][:3]:
            definition = subitem['definition']
            definition_index = item['definitions'][:3].index(subitem) + 1
            combined_definitions += f"{definition_index}. {definition}\n"
        
        embed.add_field(name=part_of_speech.upper(), value=combined_definitions, inline=False)


    # Send embed
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

    # Check for invalid input format
    if len(dice_split) != 2 or dice.isalpha() or dice.isnumeric():
        error_embed.description='`dice` input should be formatted like **2d20** or **1d4**'
        await interaction.response.send_message(embed=error_embed)
        print(f'{RED}Invalid dice input{RES}')
        return
    else:
        num_rolls = int(dice_split[0])
        num_sides = int(dice_split[1])

        for x in range(num_rolls):
            this_roll = randint(1, num_sides + 1)
            total += this_roll
            embed.add_field(name=f'Roll {x + 1}', value=f'{this_roll}', inline=True)

        # Update embed with dice and total
        embed.title = f'Rolled {dice}'
        embed.description = f'Dice total: **{total}**'
        embed.set_thumbnail(
            url='https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/apple/285/game-die_1f3b2.png'
        )
    
    
    # Send embed
    await interaction.response.send_message(embed=embed)

    # Send confirmation message
    print(f'Rolled {YLW}{dice}{RES} for a total of {YLW}{total}{RES}!')
    



bot.run(cfg['token'])