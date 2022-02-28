import aiohttp
import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
from udpy import UrbanClient

from config import TEST_GUILD_IDS
from colors import BRAND_COLOR, RES, RD, YW, CY, GR
from embeds import ERROR_TEMPLATE, EMBED_TEMPLATE, INVALID_INPUT_EMBED, WORD_NOT_FOUND_EMBED
from error_messages import MISSING_PERMISSIONS, WORD_NOT_FOUND_MSG


class Search(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(guild_ids=TEST_GUILD_IDS, description='Get the definition of a word')
    async def define(self, interaction: Interaction, word: str = SlashOption(description="Word to define")):
        """Sends the definition of the specified word"""
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
            
            print(WORD_NOT_FOUND_MSG)
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
    async def urban(self, interaction: Interaction, phrase: str = SlashOption(description="Word to define")):
        """Sends the definition of a word from Urban Dictionary"""
        print(print(f'{CY}Urban{RES} command used!'))
        
        # Get list of definitions from Urban Dictionary API
        urban = UrbanClient()
        phrase = phrase.lower()
        defs_list = urban.get_definition(phrase)


        try:
            first_def = defs_list[0]
        except Exception: # Send error embed if the phrase isn't found
            try:
                await interaction.response.send_message(embed=WORD_NOT_FOUND_EMBED)
                print(WORD_NOT_FOUND_MSG)
                return
            except nextcord.Forbidden:
                print(MISSING_PERMISSIONS)
            
        

        # Create embed
        embed = EMBED_TEMPLATE.copy()
        embed.title = f'{phrase[0].upper()}{phrase[1:]}'
        embed.url = f'https://www.urbandictionary.com/define.php?term={phrase}'
        embed.add_field(name='Definition', value=f'{first_def.definition}', inline=False)
        embed.add_field(name='Example', value=f'{first_def.example}', inline=False)
        embed.set_thumbnail(
            url='https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/apple/285/banana_1f34c.png'
        )

        # Send embed to channel
        try:
            await interaction.response.send_message(embed=embed)
        except nextcord.Forbidden:
            print(MISSING_PERMISSIONS)


        print(f'Sent definition of {YW}{phrase}{RES}!')



def setup(bot):
    bot.add_cog(Search(bot))