import nextcord
from nextcord.ext import commands
from colors import RES, GR
import os
from config import TOKEN, TEST_GUILD_ID

from buttons import RoleView



# Initialize bot
bot = commands.Bot(command_prefix="~", intents=nextcord.Intents.all() )

test_guild_id = TEST_GUILD_ID


@bot.event
async def on_ready():
    print(f'\n{GR}[Logged in as {bot.user}]{RES}')
    bot.add_view(RoleView())

for fn in os.listdir(os.path.join(os.getcwd(), 'cogs')):
    if fn.endswith('.py') and not fn.startswith('__init__'):
        bot.load_extension(f'cogs.{fn[:-3]}')

@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')
    await ctx.send('Loaded cog!')

@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    await ctx.send('Unloaded cog!')

@bot.command()
async def reload(ctx, extension):
    bot.reload_extension(f'cogs.{extension}')
    await ctx.send('Reloaded cog!')



bot.run(TOKEN)