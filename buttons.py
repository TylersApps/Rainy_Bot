import nextcord
import config
from utils import utils



class GitHubButton(nextcord.ui.View): ## Format from nextcord examples on GitHub
    """Function necessary to add link button to help command embed"""
    def __init__(self):
        super().__init__()
        url = 'https://github.com/tholley7/Rainy_Bot'

        # Add the quoted url to the button, and add the button to the view.
        self.add_item(nextcord.ui.Button(label='GitHub', url=url))


class RoleView(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    VIEW_NAME =  "RoleView"

    @nextcord.ui.button(label='He/Him', 
        style=nextcord.ButtonStyle.primary, 
        custom_id=utils.custom_id(VIEW_NAME, config.HE_HIM_ROLE_ID)
    )
    async def male_button(self, button, interaction):
        await interaction.response.send_message(f'You clicked "{button.label}"')

    @nextcord.ui.button(label='She/Her', 
        style=nextcord.ButtonStyle.primary, 
        custom_id=utils.custom_id(VIEW_NAME, config.SHE_HER_ROLE_ID)
    )
    async def female_button(self, button, interaction):
        await interaction.response.send_message(f'You clicked "{button.label}"')

    @nextcord.ui.button(label='They/Them', 
        style=nextcord.ButtonStyle.primary, 
        custom_id=utils.custom_id(VIEW_NAME, config.THEY_THEM_ROLE_ID)
    )
    async def they_them_button(self, button, interaction):
        await interaction.response.send_message(f'You clicked "{button.label}"')

    @nextcord.ui.button(label='Other', 
        style=nextcord.ButtonStyle.primary, 
        custom_id=utils.custom_id(VIEW_NAME, config.OTHER_PRONOUNS_ROLE_ID)
    )
    async def other_pronouns_button(self, button, interaction):
        await interaction.response.send_message(f'You clicked "{button.label}"')