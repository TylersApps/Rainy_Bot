import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
from textwrap import dedent
from config import TEST_GUILD_IDS, BOT_ICON_URL, SUPPORT_ROLE_ID, MOD_ROLE_ID
from embeds import ERROR_TEMPLATE, EMBED_TEMPLATE, BRAND_TEMPLATE, INVALID_PERMISSIONS
from colors import BRAND_COLOR, RES, CY, YW, RD
from emojis import *
from error_messages import MISSING_PERMISSIONS
from buttons import AcceptRulesView, PronounsView, GitHubButtonView, DMRolesView
from random import randint


class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @nextcord.slash_command(guild_ids=TEST_GUILD_IDS, description="Get a list of Rainy Bot's commands!")
    async def help(self, interaction: Interaction):
        """Sends a list of available commands."""
        print(f'{CY}Help{RES} command used!')

        embed = EMBED_TEMPLATE.copy()
        embed.color = BRAND_COLOR
        embed.title = 'Rainy Bot Commands'

        embed.description = dedent('\
                `/help`\nGet a list of available commands.\n\n\
                `/adminhelp`\nGet a list of admin commands (admin only).\n\n\
                `/randompost <subreddit_name>`\nGet random post from subreddit.\n\n\
                `/roll <(x)d(y)>`\nRoll x dice, each with y sides.\n\n\
                `/define <word>`\nDefine a word (English only).\n\n\
                `/urban <phrase>`\nDefine a phrase with Urban Dictionary.')
        
        embed.set_thumbnail(url=BOT_ICON_URL)

        try:
            await interaction.response.send_message(embed=embed, view=GitHubButtonView(), ephemeral=True)
            print(f'Sent {YW}general help{RES} message!')
        except Exception:
            print(f'{RD}[FORBIDDEN]: Bot missing permissions to send messages.{RES}')


    @nextcord.slash_command(guild_ids=TEST_GUILD_IDS, description="Get a list of Rainy Bot's admin commands!")
    async def adminhelp(self, interaction: Interaction):
        """Sends a list of admin commands."""
        print(f'{CY}AdminHelp{RES} command used!')

        if not interaction.user.guild_permissions.administrator:
            try:
                await interaction.response.send_message(embed=INVALID_PERMISSIONS, ephemeral=True)
            except Exception:
                print(f'{RD}[FORBIDDEN]: Bot missing permissions to send messages.{RES}')
            
            print(f'{RD}[INVALID PERMISSIONS]: {interaction.user.name} does not have permission to use AdminHelp command.{RES}')
            return

        embed = EMBED_TEMPLATE.copy()
        embed.color = BRAND_COLOR
        embed.title = 'Rainy Bot Admin Commands'

        embed.description = dedent('\
                `/adminhelp`\nGet a list of admin-specific commands.\n\n\
                `/pronouns`\nSend an embed with buttons to set PronounsView.\n\n\
                `/rules`\nSend the rules embed.\n\n\
                `/dms`\n Send the DM access roles menu.')

        embed.set_thumbnail(url=BOT_ICON_URL)    
        
        try:
            await interaction.response.send_message(embed=embed, view=GitHubButtonView(), ephemeral=True)
            print(f'Sent {YW}Admin Help{RES} message!')
        except Exception:
            print(f'{RD}[FORBIDDEN]: Bot missing permissions to send messages.{RES}')


    @nextcord.slash_command(guild_ids=TEST_GUILD_IDS, description='Roll a specific amount of dice with a specific amount of sides!')
    async def roll(self, interaction: Interaction, dice: str=SlashOption(description="Specified dice")):
        """Rolls die/dice with NdN format"""
        print(f'{CY}Roll{RES} command used!')

        # Make dice lowercase
        dice = dice.lower()
        
        # Split input into rolls and sides
        try:
            rolls, sides = map(int, dice.split('d'))
        except Exception: # Invalid input
            error_embed = ERROR_TEMPLATE.copy()
            error_embed.title = 'Invalid input format'
            error_embed.description = '`dice` input should be formatted like **NdN**'
            try:
                await interaction.response.send_message(embed=error_embed, ephemeral=True)
            except nextcord.Forbidden:
                print(MISSING_PERMISSIONS)
            
            print(f'{RD}[INVALID]: Incorrect roll input format{RES}')
            return

        # Send error if sides or rolls is < 2 or > 100
        if not (2 < rolls < 101 or 2 < sides < 101):
            error_embed = ERROR_TEMPLATE.copy()
            error_embed.title = 'Invalid input'
            error_embed.description = dedent('First N in NdN must be a non-negative, non-zero integer 1-100.\n\
                                              Second N in NdN must be non-negative, non-zero integer 2-100')
            try: 
                await interaction.response.send_message(embed=error_embed, ephemeral=True)
            except Exception:
                print(f'{RD}[FORBIDDEN]: Bot missing permissions to send messages.{RES}')

            print(f'{RD}[INVALID]: One or more N was negative, zero, <2, or >100{RES}')
            return


        embed = EMBED_TEMPLATE.copy()

        total = 0
        for r in range(rolls):
            this_roll = randint(1, sides)
            total += this_roll
            embed.add_field(name=f'Roll {r + 1}', value=f'{this_roll}', inline=True)

        # Formatted string 
        dice_trimmed = f'{rolls}d{sides}'
        embed.title = f'{dice_trimmed} | Total = {total}'

        
        # Send embed and confirmation output
        try:
            await interaction.response.send_message(embed=embed)
            if total == 69:
                await interaction.channel.send("Nice")
        except nextcord.Forbidden:
            print(MISSING_PERMISSIONS)

        print(f'Rolled {YW}{dice_trimmed}{RES} for a total of {YW}{total}{RES}!')


    @nextcord.slash_command(guild_ids=TEST_GUILD_IDS, description='Send an embed with buttons to set pronouns roles!')
    async def pronouns(self, interaction: Interaction):
        """Sends a message with buttons to allow users to get a role with their PronounsView"""
        print(f'{CY}PronounsView{RES} command used!')

        # If the user who used the command doesn't have admin perms
        if not interaction.user.guild_permissions.administrator:
            error_embed = ERROR_TEMPLATE.copy()
            error_embed.title = 'Invalid permissions'
            error_embed.description = "You don't have the right permissions to use that command."
            try:
                await interaction.response.send_message(embed=error_embed, ephemeral=True)
            except nextcord.Forbidden:
                print(MISSING_PERMISSIONS)
            
            print(f'{RD}[INVALID PERMISSIONS]: {interaction.user.name} does not have permission to use PronounsView command.{RES}')
            return

        
        embed = EMBED_TEMPLATE.copy()
        embed.title = 'Pronouns'
        embed.description = 'Use the buttons below to select which pronouns you use.'

        try:
            await interaction.response.send_message('Message sent!', ephemeral=True, delete_after=1)
            await interaction.channel.send(embed=embed, view=PronounsView())
        except nextcord.Forbidden:
            print(MISSING_PERMISSIONS)

        print(f'Sent {YW}Pronouns{RES} menu!')

    
    @nextcord.slash_command(guild_ids=TEST_GUILD_IDS, description='Send rules embed!')
    async def rules(self, interaction: Interaction):
        """Sends a message with the server rules in the form of an embed"""
        print(f'{CY}Rules{RES} command used!')

        # If the user who used the command isn't server owner
        if not await self.bot.is_owner(interaction.user): 
            try:
                await interaction.response.send_message(embed=INVALID_PERMISSIONS, ephemeral=True)
                print(f'{RD}[INVALID PERMISSIONS]: {interaction.user.name} does not have permission to use Rules command.{RES}')
            except nextcord.Forbidden:
                print(MISSING_PERMISSIONS)
                return
        

        # Create embed
        embed = BRAND_TEMPLATE.copy()

        embed.description = dedent(f"\
            **Welcome to Rainy Support!**\n\
            Before you get started we’d like to inform you about our community guidelines. Once you have read the rules, click \"Accept Rules\" to gain access to the server.\n\
            \n\
            **You may:**\n\
            {CHECK} Ping <@&{SUPPORT_ROLE_ID}> for help or <@&{MOD_ROLE_ID}> to report rule violation.\n\
            {CHECK} Mention someone directly to reply to or address them directly.\n\
            {CHECK} Let others test the bot. You are not the only one in here.\n\
            \n\
            **You may not:**\n\
            {REDX} Discuss politics.\n\
            {REDX} Swear or use inflammatory language.\n\
            {REDX} Send NSFW content outside of the designated channel.\n\
            {REDX} Use bot commands outside of the Bot Demo category.\n\
            {REDX} Violate Discord ToS. This is an instant ban.\n\
            {REDX} Send advertisements in channels or DMs.\n\
            {REDX} Disregard DM access roles (see below).\n\
            \n\
            **Please try not to:**\n\
            {SLASH} Interrupt staff.\n\
            {SLASH} Tell mods how to do their job.\n\
            {SLASH} Comment on actions taken by our moderators.\n\
            {SLASH} Ask to become a moderator. (If we are recruiting, you'll know.)\n\
            \n\
            **Note:**\n\
            Moderators are allowed to warn, mute, kick, and ban for any reason.\n\
            Please make sure to read channel descriptions and pinned messages.")
        
        embed.set_footer(text='Rules last updated Feb. 23, 2022')


        # Send message without normal users seeing.
        try:
            await interaction.response.send_message('Message sent!', ephemeral=True, delete_after=1)
            await interaction.channel.send(embed=embed, view=AcceptRulesView())
        except Exception as ex:
            print(f'{MISSING_PERMISSIONS}\n{ex}')

        print(f'Sent {YW}Rules{RES}!')


    @nextcord.slash_command(guild_ids=TEST_GUILD_IDS, description='Send an embed with buttons to set DM access preference role!')
    async def dms(self, interaction: Interaction):
        """Sends a message with buttons to allow users to get a role with their DMs access preferences"""
        print(f'{CY}DMs{RES} command used!')

        # If the user who used the command doesn't have admin perms
        if not interaction.user.guild_permissions.administrator:
            error_embed = ERROR_TEMPLATE.copy()
            error_embed.title = 'Invalid permissions'
            error_embed.description = "You don't have the right permissions to use that command."
            try:
                await interaction.response.send_message(embed=error_embed, ephemeral=True)
            except nextcord.Forbidden:
                print(MISSING_PERMISSIONS)
            
            print(f'{RD}[INVALID PERMISSIONS]: {interaction.user.name} does not have permission to use DMs command.{RES}')
            return

        privacy_article = 'https://support.discord.com/hc/en-us/articles/217916488-Blocking-Privacy-Settings-'
        
        embed = EMBED_TEMPLATE.copy()
        embed.title = 'DM Access Roles'
        embed.description = dedent(f"Use the buttons below to select your preference for DM access.\n\
            \n\
            If you want extra privacy, Discord has it's own method of controlling DM access. \n\
            You can read more about this setting [here]({privacy_article})")
        embed.set_footer(text='Please respect which of these roles a user has. If anyone breaks this rule, report them to an admin.')
        try:
            await interaction.response.send_message('Message sent!', ephemeral=True, delete_after=1)
            await interaction.channel.send(embed=embed, view=DMRolesView())
            print(f'Sent {YW}DMs{RES} menu!')
        except nextcord.Forbidden as ex:
            print(MISSING_PERMISSIONS)
            print(ex)

        
    
    
def setup(bot):
    bot.add_cog(Basic(bot))