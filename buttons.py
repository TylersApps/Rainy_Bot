import nextcord
import config
from utils import utils
from nextcord import Interaction



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

    async def alter_role(self, button: nextcord.ui.Button, interaction: Interaction):
        role_id = int(button.custom_id.split(":")[-1])
        role = interaction.guild.get_role(role_id)
        assert isinstance(role, nextcord.Role)

        # If user has the role
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f'Your **{role.name}** role was removed.', ephemeral=True, delete_after=15)
        # If user does not have the role
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f'Gave you the **{role.name}** role!', ephemeral=True, delete_after=15)


    @nextcord.ui.button(label='He/Him', style=nextcord.ButtonStyle.primary, custom_id=utils.custom_id(VIEW_NAME, config.HE_HIM_ROLE_ID))
    async def male_button(self, button, interaction):
        await self.alter_role(button, interaction)

    @nextcord.ui.button(label='She/Her', style=nextcord.ButtonStyle.primary, custom_id=utils.custom_id(VIEW_NAME, config.SHE_HER_ROLE_ID))
    async def female_button(self, button, interaction):
        await self.alter_role(button, interaction)

    @nextcord.ui.button(label='They/Them', style=nextcord.ButtonStyle.primary, custom_id=utils.custom_id(VIEW_NAME, config.THEY_THEM_ROLE_ID))
    async def they_them_button(self, button, interaction):
        await self.alter_role(button, interaction)

    @nextcord.ui.button(label='Other', style=nextcord.ButtonStyle.primary, custom_id=utils.custom_id(VIEW_NAME, config.OTHER_PRONOUNS_ROLE_ID))
    async def other_pronouns_button(self, button, interaction):
        await self.alter_role(button, interaction)