import colorama
import config
import disnake
from disnake.ext import commands


client = disnake.Client()
bot = commands.Bot(
    command_prefix='!',
    test_guilds=[123456789], # Optional
    sync_commands_debug=True
)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


# NEEDS FURTHER TESTING
@bot.slash_command(description='Responds with list of available commands.')
async def help(inter):
    await inter.response.send_message("Test successful!")



client.run(config.cfg['token'])