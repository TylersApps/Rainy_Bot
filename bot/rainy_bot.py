import colorama
import os
import discord

# ERROR - AttributeError: module 'discord' has no attribute 'Bot'

client = discord.Client()
bot = discord.Bot()

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@bot.slash_command(guild_ids=[606310746070056991])
async def hello(ctx):
    await ctx.respond("Hello!")



client.run('OTQzMzg5MTU3NTcxNTY3NjM2.YgyVng.Jb3K794ZNddRxCSTtqd4GlSvfJc')