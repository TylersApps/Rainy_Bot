import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
from config import TEST_GUILD_ID
from colors import BRAND_COLOR, RES, RD, YW, CY, GR
from embed_templates import ERROR_TEMPLATE, EMBED_TEMPLATE, UPCOMING_EMBED


class Notion(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @nextcord.slash_command(guild_ids=[TEST_GUILD_ID], description='Command not yet supported')
    async def notion(self, interaction: Interaction):
        """Allow user to edit of notion databases that the user has access to"""
        await interaction.response.send_message(embed=UPCOMING_EMBED)
        print(f'{RD}[NOT SUPPORTED]: Notion command not supported yet.{RES}')



def setup(bot):
    bot.add_cog(Notion(bot))