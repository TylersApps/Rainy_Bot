from email.policy import default
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
brand_color = nextcord.Colour.from_rgb(65, 157, 193)

error_template = nextcord.Embed(color=error_color)
embed_template = nextcord.Embed(color=embed_color)
upcoming_embed = nextcord.Embed(color=brand_color, title='Feature coming soon', description="That command isn't supported yet.")




@bot.event
async def on_ready():
    print(f'\n{GR}[Logged in as {bot.user}]{RES}')


class GitHubButton(nextcord.ui.View): ## Format from nextcord examples on GitHub
    """Function necessary to add link button to help command embed"""
    def __init__(self):
        super().__init__()
        url = 'https://github.com/tholley7/Rainy_Bot'

        # Link buttons cannot be made with the decorator
        # Therefore we have to manually create one.
        # We add the quoted url to the button, and add the button to the view.
        self.add_item(nextcord.ui.Button(label='GitHub', url=url))

@bot.slash_command(guild_ids=[test_guild_id], description="Get a list of Rainy Bot's commands")
async def help(interaction: Interaction):
    """Send a list of available commands to the channel where this command is sent."""
    print(f'{CY}Help{RES} command used!')

    embed = embed_template.copy()

    embed.description = '\
            `/help`\n Display a list of available commands\n\n\
            `/randompost <subreddit_name>`\n Get random post from subreddit\n\n\
            `/roll <(x)d(y)>`\n Roll x dice, each with y sides\n\n\
            `/define <word>`\n Define a word (English only)'

    embed.title = 'Rainy Bot Commands'
    embed.color = brand_color
    embed.set_thumbnail(url='https://i.imgur.com/bhbTUOe.png')

    await interaction.response.send_message(embed=embed, view=GitHubButton())
    


@bot.slash_command(guild_ids=[test_guild_id], description='Get a random post from a subreddit')
async def randompost(interaction: Interaction, subreddit_name: str = SlashOption(description="Subreddit Choice")):
    """Send a random post from specified subreddit as an embed"""
    await interaction.response.defer()

    print(f'{CY}RandomPost{RES} command used!')

    if subreddit_name.startswith(('/r/', 'r/')):
        subreddit_name = subreddit_name.split('r/')[-1]
    

    # If specified subreddit doesn't exist, send error embed.
    try:
        subreddit = await reddit.subreddit(subreddit_name, fetch=True)
    except Exception: 
        error_embed = error_template.copy()
        error_embed.title = 'Invalid input'
        error_embed.description=f"r/{subreddit_name} doesn't exist."

        await interaction.followup.send(embed=error_embed)
        print(f'{RED}Invalid subreddit input{RES}')
        return

    try:
        submission = await subreddit.random()
        print(submission)
        url = submission.url
        permalink = f'https://www.reddit.com{submission.permalink}'
    except AttributeError as url_error:
        error_embed = error_template.copy()
        error_embed.title = 'Something went wrong'
        error_embed.description=f"Couldn't get post url"

        await interaction.followup.send(embed=url_error_embed)
        print(f'{RED}[ERRROR]: {url_error}{RES}')
        return

    

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
    embed = embed_template.copy()
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



@bot.slash_command(guild_ids=[test_guild_id], description='Get the definition of a word')
async def define(interaction: Interaction, word: str = SlashOption(description="Word to define")):
    """Send the definition of the specified word"""
    print(f'{CY}Define{RES} command used!')

    api_url = f"http://api.dictionaryapi.dev/api/v2/entries/en/{word}"

    # Get the json data for the specified word
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, ssl=False) as resp:
                data = await resp.json()
    except Exception as ex: 
        error_embed = error_template.copy()
        error_embed.title = "Word not found"
        error_embed.description = f'API Error. Please contact developer.'
        await interaction.response.send_message(embed=error_embed) 
        print(f'{RED}[ERROR]: {ex}{RES}')
        return
    
    try:
        content = data[0]['meanings']
    except KeyError: # Send error embed if the word isn't found
        error_embed = error_template.copy()
        error_embed.title = "Invalid input"
        error_embed.description = f'Can\'t find "{word}" in dictionary'
        await interaction.response.send_message(embed=error_embed)
        print(f'{RED}Can\'t find "{word}" in dictionary.{RES}')
        return

    
    # Customize embed with title and thumbnail   
    embed = embed_template.copy()
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



@bot.slash_command(guild_ids=[test_guild_id], description='Command not yet supported')
async def urban(interaction: Interaction):
    """Define a word or term with Urban Dictionary"""
    await interaction.response.send_message(embed=upcoming_embed)
    print(f'{RED}[NOT SUPPORTED]: Urban command not supported yet.{RES}')



@bot.slash_command(guild_ids=[test_guild_id], description='Roll a specific amount of dice with a specific amount of sides.')
async def roll(interaction: Interaction, dice: str=SlashOption(description="Specified dice")):
    """Rolls die/dice with NdN format"""
    print(f'{CY}Roll{RES} command used!')

    # Make dice lowercase
    dice = dice.lower()
    
    # Split input into rolls and sides
    try:
        rolls, sides = map(int, dice.split('d'))
    except Exception as invalid_input:
        error_embed = error_template.copy()
        error_embed.title = 'Invalid input'
        error_embed.description = '`dice` input should be formatted like **NdN**\n\
            Each N must be a non-negative, non-zero integer'
        await interaction.response.send_message(embed=error_embed)
        print(f'{RED}[INVALID]: Incorrect roll input format{RES}')
        return

    # Send error if sides = 0 
    if sides == 0:
        error_embed = error_template.copy()
        error_embed.title = 'Invalid input'
        error_embed.description = '`dice` input should be formatted like **NdN**\n\
            Each N must be a non-negative, non-zero integer'
        await interaction.response.send_message(embed=error_embed)
        print(f'{RED}[INVALID]: Sides was 0{RES}')
        return

    embed = embed_template.copy()

    total = 0
    for r in range(rolls):
        this_roll = randint(1, sides)
        total += this_roll
        embed.add_field(name=f'Roll {r + 1}', value=f'{this_roll}', inline=True)

    embed.title = f'{dice} | Total = {total}'

    
    # Send embed and confirmation output
    await interaction.response.send_message(embed=embed)
    print(f'Rolled {YLW}{dice}{RES} for a total of {YLW}{total}{RES}!')



@bot.slash_command(guild_ids=[test_guild_id], description='Command not yet supported')
async def notion(interaction: Interaction):
    """Allow user to edit of notion databases that the user has access to"""
    await interaction.response.send_message(embed=upcoming_embed)
    print(f'{RED}[NOT SUPPORTED]: Notion command not supported yet.{RES}')



@bot.slash_command(guild_ids=[test_guild_id], description='Command not yet supported')
async def menu(interaction: Interaction):
    """Send a menu of the specified type"""
    await interaction.response.send_message(embed=upcoming_embed)
    print(f'{RED}[NOT SUPPORTED]: Menu command not supported yet.{RES}')






bot.run(cfg['token'])