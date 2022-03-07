import nextcord
from nextcord import Interaction
from emojis import CHECK
from error_messages import MISSING_PERMISSIONS
from colors import RES, YW



class GitHubButtonView(nextcord.ui.View):
    """Function necessary to add link button to help command embed"""
    def __init__(self):
        super().__init__(timeout=None)
        url = 'https://github.com/tholley7/Rainy_Bot'

        # Add the quoted url to the button, and add the button to the view.
        self.add_item(nextcord.ui.Button(label='GitHub', url=url))


class AcceptRulesView(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)


    async def alter_role(self, button: nextcord.ui.Button, interaction: Interaction):
        role = nextcord.utils.get(interaction.guild.roles, name=button.custom_id)
        assert isinstance(role, nextcord.Role)

        # If user doesn't have the role
        if not role in interaction.user.roles:
            await interaction.user.add_roles(role)
            try:
                await interaction.response.send_message(f'Thank you for accepting the rules! You should be able to access the server now.', ephemeral=True, delete_after=10)
                print(f'{YW}{interaction.user}{RES} accepted the rules!')
            except nextcord.Forbidden:
                print(MISSING_PERMISSIONS)
        # If user has the role
        else:
            try:
                await interaction.response.send_message(f'You have already accepted the rules!', ephemeral=True, delete_after=10)
            except nextcord.Forbidden:
                print(MISSING_PERMISSIONS)


    @nextcord.ui.button(label='Accept Rules', style=nextcord.ButtonStyle.green, custom_id='Accepted Rules')
    async def accept_button(self, button, interaction):
        await self.alter_role(button, interaction)
    

class DMRolesView(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)


    async def alter_role(self, button: nextcord.ui.Button, interaction: Interaction):
        role = nextcord.utils.get(interaction.guild.roles, name=button.custom_id)
        assert isinstance(role, nextcord.Role)

        # If user has the role
        if role in interaction.user.roles:
            try:
                await interaction.user.remove_roles(role)
                await interaction.response.send_message(f'Your **{role.name}** role was removed.', ephemeral=True, delete_after=15)
                print(f'Removed {YW}{role.name}{RES} role from {YW}{interaction.user}{RES}!')
            except Exception:
                print(MISSING_PERMISSIONS)
        # If user does not have the role
        else:
            try:
                await interaction.user.add_roles(role)
                await interaction.response.send_message(f'Gave you the **{role.name}** role!', ephemeral=True, delete_after=15)
                print(f'Gave {YW}{role.name}{RES} role to {YW}{interaction.user}{RES}!')
            except Exception:
                print(MISSING_PERMISSIONS)


    @nextcord.ui.button(label='DMs Open', style=nextcord.ButtonStyle.green, custom_id='DMs Open')
    async def dms_open_button(self, button, interaction):
        await self.alter_role(button, interaction)

    @nextcord.ui.button(label='DMs Closed', style=nextcord.ButtonStyle.red, custom_id='DMs Closed')
    async def dms_closed_button(self, button, interaction):
        await self.alter_role(button, interaction)

    @nextcord.ui.button(label='Ask to DM', style=nextcord.ButtonStyle.primary, custom_id='Ask to DM')
    async def dms_ask_button(self, button, interaction):
        await self.alter_role(button, interaction)


class PronounsView(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    async def alter_role(self, button: nextcord.ui.Button, interaction: Interaction):
        role = nextcord.utils.get(interaction.guild.roles, name=button.custom_id)
        print(role)
        print(role.name)
        assert isinstance(role, nextcord.Role)

        # If user has the role
        if role in interaction.user.roles:
            try:
                await interaction.user.remove_roles(role)
                await interaction.response.send_message(f'Your **{role.name}** role was removed.', ephemeral=True, delete_after=15)
                print(f'Removed {YW}{role.name}{RES} role from {YW}{interaction.user}{RES}!')
            except Exception:
                print(MISSING_PERMISSIONS)
        # If user does not have the role
        else:
            await interaction.user.add_roles(role)
            try:
                await interaction.response.send_message(f'Gave you the **{role.name}** role!', ephemeral=True, delete_after=15)
                print(f'Gave {YW}{role.name}{RES} role to {YW}{interaction.user}{RES}!')
            except Exception:
                print(MISSING_PERMISSIONS)


    @nextcord.ui.button(label='He/Him', style=nextcord.ButtonStyle.primary, custom_id='He/Him')
    async def male_button(self, button, interaction):
        await self.alter_role(button, interaction)

    @nextcord.ui.button(label='She/Her', style=nextcord.ButtonStyle.primary, custom_id='She/Her')
    async def female_button(self, button, interaction):
        await self.alter_role(button, interaction)

    @nextcord.ui.button(label='They/Them', style=nextcord.ButtonStyle.primary, custom_id='They/Them')
    async def they_them_button(self, button, interaction):
        await self.alter_role(button, interaction)

    @nextcord.ui.button(label='Other Pronouns', style=nextcord.ButtonStyle.primary, custom_id='Other Pronouns')
    async def other_pronouns_button(self, button, interaction):
        await self.alter_role(button, interaction)