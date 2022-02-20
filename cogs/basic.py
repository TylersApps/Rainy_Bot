import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
from config import TEST_GUILD_ID, BOT_ICON_URL
from embed_templates import ERROR_TEMPLATE, EMBED_TEMPLATE
from colors import BRAND_COLOR, RES, CY, YW, RD
from utils import utils
from buttons import RoleView, GitHubButton
from random import randint


class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @nextcord.slash_command(guild_ids=[TEST_GUILD_ID], description="Get a list of Rainy Bot's commands")
    async def help(self, interaction: Interaction):
        """Sends a list of available commands."""
        print(f'{CY}Help{RES} command used!')

        embed = EMBED_TEMPLATE.copy()
        embed.color = BRAND_COLOR
        embed.title = 'Rainy Bot Commands'

        embed.description = '\
                `/help`\nGet a list of available commands\n\n\
                `/adminhelp`\nIf you are an admin, get a list of admin commands.\n\n\
                `/randompost <subreddit_name>`\nGet random post from subreddit\n\n\
                `/roll <(x)d(y)>`\nRoll x dice, each with y sides\n\n\
                `/define <word>`\nDefine a word (English only)'
        
        embed.set_thumbnail(url=BOT_ICON_URL)


        await interaction.response.send_message(embed=embed, view=GitHubButton())



    @nextcord.slash_command(guild_ids=[TEST_GUILD_ID], description="Get a list of Rainy Bot's admin commands")
    async def adminhelp(self, interaction: Interaction):
        """Sends a list of admin commands."""
        print(f'{CY}AdminHelp{RES} command used!')

        if not interaction.user.guild_permissions.administrator:
            error_embed = ERROR_TEMPLATE.copy()
            error_embed.title = 'Invalid permissions'
            error_embed.description = "You don't have the right permissions to use that command."
            await interaction.response.send_message(embed=error_embed)
            print(f'{RD}[INVALID PERMISSIONS]: User does not have permission to use Pronouns command.{RES}')
            return

        embed = EMBED_TEMPLATE.copy()
        embed.color = BRAND_COLOR
        embed.title = 'Rainy Bot Admin Commands'

        embed.description = '\
                `/adminhelp`\nGet a list of admin-specific commands\n\n\
                `/pronouns`\nSend an embed with buttons for users to self-assign a pronouns role'

        embed.set_thumbnail(url=BOT_ICON_URL)    
        

        await interaction.response.send_message(embed=embed, view=GitHubButton())

    
    @nextcord.slash_command(guild_ids=[TEST_GUILD_ID], description='Roll a specific amount of dice with a specific amount of sides.')
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
            await interaction.response.send_message(embed=error_embed)
            print(f'{RD}[INVALID]: Incorrect roll input format{RES}')
            return

        # Send error if sides or rolls is < 1 
        if sides < 1 or rolls < 1:
            error_embed = ERROR_TEMPLATE.copy()
            error_embed.title = 'Invalid values'
            error_embed.description = 'Each N in NdN must be a non-negative, non-zero integer'
            await interaction.response.send_message(embed=error_embed)
            print(f'{RD}[INVALID]: Sides or  was less than 1{RES}')
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
        await interaction.response.send_message(embed=embed)
        print(f'Rolled {YW}{dice_trimmed}{RES} for a total of {YW}{total}{RES}!')


    @nextcord.slash_command(guild_ids=[TEST_GUILD_ID], description='Command not yet supported')
    async def pronouns(self, interaction: Interaction):
        """Sends a message with buttons to allow users to get a role with their pronouns"""
        if not interaction.user.guild_permissions.administrator:
            error_embed = ERROR_TEMPLATE.copy()
            error_embed.title = 'Invalid permissions'
            error_embed.description = "You don't have the right permissions to use that command."
            await interaction.response.send_message(embed=error_embed)
            print(f'{RD}[INVALID PERMISSIONS]: User does not have permission to use Pronouns command.{RES}')
            return

        print(f'{CY}PronounMenu{RES} command used!')

        embed = EMBED_TEMPLATE.copy()
        embed.title = 'What are your pronouns?'
        embed.description = 'Use the buttons below to select what pronouns you use.'

        await interaction.response.send_message(embed=embed, view=RoleView())
        print(f'Sent {YW}Pronoun Menu{RES}!')

    
    
def setup(bot):
    bot.add_cog(Basic(bot))