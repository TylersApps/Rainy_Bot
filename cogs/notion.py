import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
from config import TEST_GUILD_IDS
from colors import BRAND_COLOR, RES, RD, YW, CY, GR
from embeds import ERROR_TEMPLATE, EMBED_TEMPLATE, UPCOMING_EMBED
from errors_messages import MISSING_PERMISSIONS


class Notion(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @nextcord.slash_command(guild_ids=TEST_GUILD_IDS, description='Command not yet supported')
    async def notion(self, interaction: Interaction):
        """Allow user to edit of notion databases that the user has access to"""
        try:
            await interaction.response.send_message(embed=UPCOMING_EMBED)
        except Exception:
                print(MISSING_PERMISSIONS)
                
        print(f'{RD}[NOT SUPPORTED]: Notion command not supported yet.{RES}')



def setup(bot):
    bot.add_cog(Notion(bot))