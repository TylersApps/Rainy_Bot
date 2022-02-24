import aiohttp
import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
from config import TEST_GUILD_IDS
from colors import BRAND_COLOR, RES, RD, YW, CY, GR
from embeds import ERROR_TEMPLATE, EMBED_TEMPLATE, UPCOMING_EMBED
from error_messages import MISSING_PERMISSIONS


class Search(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(guild_ids=TEST_GUILD_IDS, description='Get the definition of a word')
    async def define(self, interaction: Interaction, word: str = SlashOption(description="Word to define")):
        """Send the definition of the specified word"""
        print(f'{CY}Define{RES} command used!')

        api_url = f"http://api.dictionaryapi.dev/api/v2/entries/en/{word}"

        # Get the json data for the specified word
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url, ssl=False) as resp:
                    data = await resp.json()
        except Exception as ex: 
            error_embed = ERROR_TEMPLATE.copy()
            error_embed.title = "Something went wrong"
            error_embed.description = f'API Error. Please contact developer.'

            try:
                await interaction.response.send_message(embed=error_embed)
            except nextcord.Forbidden:
                print(MISSING_PERMISSIONS)

            print(f'{RD}[ERROR]: {ex}{RES}')
            return
        
        try:
            content = data[0]['meanings']
        except KeyError: # Send error embed if the word isn't found
            error_embed = ERROR_TEMPLATE.copy()
            error_embed.title = "Word not found"
            error_embed.description = f'Can\'t find "{word}" in dictionary'

            try:
                await interaction.response.send_message(embed=error_embed)
            except nextcord.Forbidden:
                print(MISSING_PERMISSIONS)
            
            print(f'{RD}[INVALID]: Can\'t find "{word}" in dictionary.{RES}')
            return

        
        # Customize embed with title and thumbnail   
        embed = EMBED_TEMPLATE.copy()
        embed.title=f'"{word.lower().capitalize()}"'
        embed.set_thumbnail(
            url='https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/apple/285/open-book_1f4d6.png'
        )

        # Iterate through and create fields
        for item in content:
            part_of_speech = item['partOfSpeech']
            combined_definitions = ''

            for subitem in item['definitions'][:3]:
                definition = subitem['definition']
                definition_index = item['definitions'][:3].index(subitem) + 1
                combined_definitions += f"{definition_index}. {definition}\n"
            
            embed.add_field(name=part_of_speech.upper(), value=combined_definitions, inline=False)


        # Send embed
        try:
            await interaction.response.send_message(embed=embed)
        except nextcord.Forbidden:
                print(MISSING_PERMISSIONS)
        
        # Send confirmation message
        print(f'Sent definition of {YW}{word}{RES}!')


    
    @nextcord.slash_command(guild_ids=TEST_GUILD_IDS, description='Command not yet supported')
    async def urban(self, interaction: Interaction):
        """Define a word or term with Urban Dictionary"""
        try:
            await interaction.response.send_message(embed=UPCOMING_EMBED)
        except nextcord.Forbidden:
                print(MISSING_PERMISSIONS)

        print(f'{RD}[NOT SUPPORTED]: Urban command not supported yet.{RES}')



def setup(bot):
    bot.add_cog(Search(bot))