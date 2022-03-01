import nextcord
import os
from nextcord.ext import commands

# From my 
from colors import RES, GR
from config import TOKEN
from buttons import AcceptRulesView, PronounsView



# Initialize bot
bot = commands.Bot(command_prefix="~", intents=nextcord.Intents.all() )


# Runs when bot is started up
@bot.event
async def on_ready():
    print(f'\n{GR}[Logged in as {bot.user}]{RES}')
    bot.add_view(PronounsView())
    bot.add_view(AcceptRulesView())


# Add guild
@bot.event
async def on_guild_join(guild):
    guild.create_role()


# Load cogs on strartup
for fn in os.listdir(os.path.join(os.getcwd(), 'cogs')):
    if fn.endswith('.py') and not fn.startswith('__init__'):
        bot.load_extension(f'cogs.{fn[:-3]}')


# Loads a cog
@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')
    await ctx.send('Loaded cog!')

# Unloads a cog
@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    await ctx.send('Unloaded cog!')

# Reloads a cog
@bot.command()
async def reload(ctx, extension):
    bot.reload_extension(f'cogs.{extension}')
    await ctx.send('Reloaded cog!')



bot.run(TOKEN)