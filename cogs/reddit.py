import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
from textwrap import dedent
from config import reddit, TEST_GUILD_IDS
from embeds import ERROR_TEMPLATE, EMBED_TEMPLATE
from colors import RES, CY, YW, RD, GR
from error_messages import MISSING_PERMISSIONS, NSFW_MISMATCH



class Reddit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @nextcord.slash_command(guild_ids=TEST_GUILD_IDS, description='Get a random post from a subreddit!')
    async def randompost(self, interaction: Interaction, subreddit_name: str = SlashOption(description="Subreddit Choice")):
        """Send a random post from specified subreddit as an embed"""
        await interaction.response.defer()

        print(f'{CY}RandomPost{RES} command used!')

        if subreddit_name.startswith(('/r/', 'r/')):
            subreddit_name = subreddit_name.split('r/')[-1]
        

        # If specified subreddit doesn't exist, send error embed.
        try:
            subreddit = await reddit.subreddit(subreddit_name, fetch=True)
        except Exception: # Invalid subreddit input
            error_embed = ERROR_TEMPLATE.copy()
            error_embed.title = 'Invalid subreddit'
            error_embed.description=f"r/{subreddit_name} doesn't exist or is banned from Reddit."

            try:
                await interaction.followup.send(embed=error_embed, ephemeral=True)
            except nextcord.Forbidden:
                print(MISSING_PERMISSIONS)

            print(f"{RD}[INVALID]: r/{subreddit_name} doesn't exist or is banned{RES} from Reddit.")
            return

        try:
            submission = await subreddit.random()
            # print(f'{GR}GRABBED SUBMISSION:{RES} {submission}')
            url = submission.url
            full_url = f'https://www.reddit.com{submission.permalink}'
        except AttributeError: # Couldn't grab submission
            error_embed = ERROR_TEMPLATE.copy()
            error_embed.title = 'Subreddit unsupported'
            error_embed.description=f"r/{subreddit} doesn't allow grabbing random posts or doesn't have any posts."

            try:
                await interaction.followup.send(embed=error_embed, ephemeral=True)
            except nextcord.Forbidden:
                print(MISSING_PERMISSIONS)
            
            print(f"{RD}[UNSUPPORTED]: r/{subreddit} doesn't allow grabbing random posts or doesn't have any posts.{RES}")
            return

        # If submission is NSFW and channel is not, send error embed.
        if (not interaction.channel.is_nsfw()) and (submission.over_18):
            error_embed = ERROR_TEMPLATE.copy()
            error_embed.title = "Can't send that here."
            error_embed.description = dedent("\
                **That post is marked as NSFW.**\n\
                If that is a NSFW subreddit, use a channel marked as NSFW.\n\
                If that subreddit isn't NSFW, try that command again.")
            
            try:
                await interaction.followup.send(embed=error_embed, ephemeral=True)
            except nextcord.Forbidden:
                print(MISSING_PERMISSIONS)

            print(NSFW_MISMATCH)
            return


        # Initialize title and shorten to max 253 characters
        title = submission.title
        if len(title) > 250:
            title = title[:250] + ' ...'
        
        # Initialize post_body and shorten to max 500 characters
        post_body = submission.selftext
        if len(post_body) > 500:
            post_body = post_body[:497]
            post_body += ' ...' 


        # Customize embed
        embed = EMBED_TEMPLATE.copy()
        embed.title = title
        embed.url = full_url
        embed.description = post_body
        embed.set_author(name=f'r/{submission.subreddit}', url=f'https://www.reddit.com/r/{submission.subreddit}')
        if url.endswith('.jpg') or url.endswith('.png') or url.endswith('.jpeg'): 
            embed.set_image(url=url)


        # Send embed and confirmation message
        try:
            await interaction.followup.send(embed=embed)
        except nextcord.Forbidden:
                print(MISSING_PERMISSIONS)

        print(f'Sent post from {YW}{submission.subreddit}{RES}: {submission.title}')


    
def setup(bot):
    bot.add_cog(Reddit(bot))