import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
from numpy import delete
from config import TEST_GUILD_IDS, BOT_ICON_URL, SUPPORT_ROLE_ID, MOD_ROLE_ID
from embeds import ERROR_TEMPLATE, EMBED_TEMPLATE, BRAND_TEMPLATE, INVALID_PERMISSIONS
from colors import BRAND_COLOR, RES, CY, YW, RD
from emojis import *
from errors_messages import MISSING_PERMISSIONS
from buttons import AcceptRules, Pronouns, GitHubButton
from random import randint


class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @nextcord.slash_command(guild_ids=TEST_GUILD_IDS, description="Get a list of Rainy Bot's commands")
    async def help(self, interaction: Interaction):
        """Sends a list of available commands."""
        print(f'{CY}Help{RES} command used!')

        embed = EMBED_TEMPLATE.copy()
        embed.color = BRAND_COLOR
        embed.title = 'Rainy Bot Commands'

        embed.description = '\
                `/help`\nGet a list of available commands\n\n\
                `/adminhelp`\nGet a list of admin commands (admin only).\n\n\
                `/randompost <subreddit_name>`\nGet random post from subreddit\n\n\
                `/roll <(x)d(y)>`\nRoll x dice, each with y sides\n\n\
                `/define <word>`\nDefine a word (English only)'
        
        embed.set_thumbnail(url=BOT_ICON_URL)

        try:
            await interaction.response.send_message(embed=embed, view=GitHubButton(), ephemeral=True)
        except Exception:
                print(f'{RD}[FORBIDDEN]: Bot missing permissions to send messages.{RES}')



    @nextcord.slash_command(guild_ids=TEST_GUILD_IDS, description="Get a list of Rainy Bot's admin commands")
    async def adminhelp(self, interaction: Interaction):
        """Sends a list of admin commands."""
        print(f'{CY}AdminHelp{RES} command used!')

        if not interaction.user.guild_permissions.administrator:
            try:
                await interaction.response.send_message(embed=INVALID_PERMISSIONS, ephemeral=True)
            except Exception:
                print(f'{RD}[FORBIDDEN]: Bot missing permissions to send messages.{RES}')
            
            print(f'{RD}[INVALID PERMISSIONS]: User does not have permission to use Pronouns command.{RES}')
            return

        embed = EMBED_TEMPLATE.copy()
        embed.color = BRAND_COLOR
        embed.title = 'Rainy Bot Admin Commands'

        embed.description = '\
                `/adminhelp`\nGet a list of admin-specific commands\n\n\
                `/pronouns`\nSend an embed with buttons to set pronouns'

        embed.set_thumbnail(url=BOT_ICON_URL)    
        
        try:
            await interaction.response.send_message(embed=embed, view=GitHubButton(), ephemeral=True)
        except Exception:
                print(f'{RD}[FORBIDDEN]: Bot missing permissions to send messages.{RES}')



    @nextcord.slash_command(guild_ids=TEST_GUILD_IDS, description='Roll a specific amount of dice with a specific amount of sides.')
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
                await interaction.response.send_message(embed=error_embed)
            except Exception:
                print(MISSING_PERMISSIONS)
            
            print(f'{RD}[INVALID]: Incorrect roll input format{RES}')
            return

        # Send error if sides or rolls is < 2 or > 100
        if sides < 2 or rolls < 2 or sides > 100 or dice > 100:
            error_embed = ERROR_TEMPLATE.copy()
            error_embed.title = 'Invalid input'
            error_embed.description = 'Each N in NdN must be a non-negative, non-zero integer 2-100.'
            try: 
                await interaction.response.send_message(embed=error_embed)
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
        except Exception:
                print(MISSING_PERMISSIONS)

        print(f'Rolled {YW}{dice_trimmed}{RES} for a total of {YW}{total}{RES}!')



    @nextcord.slash_command(guild_ids=TEST_GUILD_IDS, description='Send an embed with buttons to set pronouns')
    async def pronouns(self, interaction: Interaction):
        """Sends a message with buttons to allow users to get a role with their pronouns"""
        print(f'{CY}Pronouns{RES} command used!')

        # If the user who used the command doesn't have admin perms
        if not interaction.user.guild_permissions.administrator:
            error_embed = ERROR_TEMPLATE.copy()
            error_embed.title = 'Invalid permissions'
            error_embed.description = "You don't have the right permissions to use that command."
            try:
                await interaction.response.send_message(embed=error_embed)
            except Exception:
                print(MISSING_PERMISSIONS)
            
            print(f'{RD}[INVALID PERMISSIONS]: User does not have permission to use Pronouns command.{RES}')
            return

        
        embed = EMBED_TEMPLATE.copy()
        embed.title = 'What are your pronouns?'
        embed.description = 'Use the buttons below to select what pronouns you use.'

        try:
            await interaction.response.send_message(embed=embed, view=Pronouns())
            print(f'Sent {YW}Pronoun Menu{RES}!')
        except Exception:
                print(MISSING_PERMISSIONS)

    

    @nextcord.slash_command(guild_ids=TEST_GUILD_IDS, description='Send rules embed')
    async def rules(self, interaction: Interaction):
        """Sends a message with the server rules in the form of an embed"""
        print(f'{CY}Rules{RES} command used!')

        # If the user who used the command isn't server owner
        if not await self.bot.is_owner(interaction.user): 
            try:
                await interaction.response.send_message(embed=INVALID_PERMISSIONS, ephemeral=True)
            except Exception:
                print(MISSING_PERMISSIONS)
            
            print(f'{RD}[INVALID PERMISSIONS]: User does not have permission to use Rules command.{RES}')
            return
        

        embed = BRAND_TEMPLATE.copy()
        embed.description = f"\
            **Welcome to Rainy Support!**\n\
            Before you get started we’d like to inform you about our community guidelines.\n\
            \n\
            **You can:**\n\
            {CHECK} Ping <@&{SUPPORT_ROLE_ID}> for help or <@&{MOD_ROLE_ID}> to report rule violation.\n\
            {CHECK} Mention someone directly to reply to or address them directly.\n\
            {CHECK} Let others test the bot. You are not the only one in here.\n\
            \n\
            **You can't:**\n\
            {REDX} Swear or use inflammatory language.\n\
            {REDX} Send NSFW content outside of the designated channel.\n\
            {REDX} Use bot commands outside of the Bot Demo category.\n\
            {REDX} Violate Discord ToS. This is an instant ban.\n\
            {REDX} Send advertisements in channels or DMs.\n\
            \n\
            **Please try not to:**\n\
            {SLASH} Interrupt staff.\n\
            {SLASH} Tell mods how to do their job.\n\
            {SLASH} Comment on actions taken by our moderators.\n\
            {SLASH} Ask to become a moderator. (If we are recruiting, you'll know.)\n\
            \n\
            **Note:**\n\
            Moderators are allowed to warn, mute, kick, and ban for any reason.\n\
            Please make sure to read pinned messages and channel descriptions for rules."
        

        # Send message without normal users seeing.
        try:
            await interaction.response.send_message('Sending message...', ephemeral=True, delete_after=30)
            await interaction.channel.send(embed=embed, view=AcceptRules())
        except Exception:
                print(MISSING_PERMISSIONS)


    
    
def setup(bot):
    bot.add_cog(Basic(bot))