import nextcord
import os
from nextcord.ext import commands

# From my 
from colors import RES, GR, YW, WHITE
from config import BOT_TOKEN, TEST_TOKEN
from buttons import AcceptRulesView, DMRolesView, PronounsView



# Initializes bot
bot = commands.Bot(command_prefix='~', intents=nextcord.Intents.all())


# Runs when bot is started up
@bot.event
async def on_ready():
    print(f'\n{GR}[Logged in as {bot.user}]{RES}')
    bot.add_view(PronounsView())
    bot.add_view(AcceptRulesView())
    bot.add_view(DMRolesView())


# Runs when the bot joins a new guild
@bot.event
async def on_guild_join(guild):
    print(f'{GR}Joined Guild:{RES} {guild.name}!')
    # Create DM access roles if the guild doesn't have them already.
    if not nextcord.utils.get(guild.roles, name='DMs Open'):
        await guild.create_role(name='DMs Open', colour=nextcord.Colour.green())
        print(f'Created {YW}DMs Open{RES} role!')

    if not nextcord.utils.get(guild.roles, name='DMs Closed'):
        await guild.create_role(name='DMs Closed', colour=nextcord.Colour.red())
        print(f'Created {YW}DMs Closed{RES} role!')
    
    if not nextcord.utils.get(guild.roles, name='Ask to DM'):
        await guild.create_role(name='Ask to DM', colour=nextcord.Colour.blue())
        print(f'Created {YW}Ask to DM{RES} role!')

    # Create pronouns roles if the guild doesn't have them already.
    if not nextcord.utils.get(guild.roles, name='He/Him'):
        await guild.create_role(name='He/Him')
        print(f'Created {YW}He/Him{RES} role!')

    if not nextcord.utils.get(guild.roles, name='She/Her'):
        await guild.create_role(name='She/Her')
        print(f'Created {YW}She/Her{RES} role!')

    if not nextcord.utils.get(guild.roles, name='They/Them'):
        await guild.create_role(name='They/Them')
        print(f'Created {YW}They/Them{RES} role!')

    if not nextcord.utils.get(guild.roles, name='Other Pronouns'):
        await guild.create_role(name='Other Pronouns')
        print(f'Created {YW}Other Pronouns{RES} role!')

    # Create Verified role if the guild doesn't have it already.
    if not nextcord.utils.get(guild.roles, name='Accepted Rules'):
        await guild.create_role(name='Accepted Rules', color=WHITE)


# Loads cogs on strartup
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



bot.run(BOT_TOKEN)