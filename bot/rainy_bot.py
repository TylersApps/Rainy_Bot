from colorama import Fore, Style, init
import config
import nextcord
from nextcord import Interaction
from nextcord.ext import commands


# Initialize console colors
CY = Fore.CYAN
GR = Fore.GREEN
BLU = Fore.BLUE
RES = Style.RESET_ALL


bot = commands.Bot(
    command_prefix="!",
    intents=nextcord.Intents.all()
)

test_guild_id = config.cfg['guild_id']


# Sends a message to console when bot is online in server(s).
@bot.event
async def on_ready():
    print(f'\n{GR}Logged in as {bot.user}{RES}\n')

# Send a list of available commands to the channel where this command is sent.
@bot.slash_command(guild_ids=[test_guild_id])
async def help(interaction: Interaction):
    print(f'{BLU}Help command used!{RES}')
    await interaction.response.send_message('How can I help?')


bot.run(config.cfg['token'])