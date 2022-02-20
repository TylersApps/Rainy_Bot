import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
from config import reddit, TEST_GUILD_ID
from embed_templates import ERROR_TEMPLATE, EMBED_TEMPLATE
from colors import BRAND_COLOR, RES, CY, YW, RD, GR



class Reddit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @nextcord.slash_command(guild_ids=[TEST_GUILD_ID], description='Get a random post from a subreddit')
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

            await interaction.followup.send(embed=error_embed)
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
            error_embed.description=f"r/{subreddit} doesn't allow grabbing random posts"

            await interaction.followup.send(embed=error_embed)
            print(f"{RD}[SUBREDDIT UNSUPPORTED]: r/{subreddit} doesn't allow grabbing random posts{RES}")
            return

        # # If subreddit doesn't support getting random post
        # if submission == None: 
        #     error_embed = ERROR_TEMPLATE.copy()
        #     error_embed.title = 'Subreddit unsupported'
        #     error_embed.description=f"r/{subreddit} doesn't allow grabbing random posts"

        #     await interaction.followup.send(embed=error_embed)
        #     print(f"{RD}[SUBREDDIT UNSUPPORTED]: r/{subreddit} doesn't allow grabbing random posts{RES}")
        #     return
        # else:
        #     url = submission.url
        #     full_url = f'https://www.reddit.com{submission.permalink}'


        # Initialize title and shorten to max 253 characters
        title = submission.title
        if len(title) > 250:
            title = title[:250] + " ..."
        
        # Initialize post_body and shorten to max 500 characters
        post_body = submission.selftext
        if len(post_body) > 500:
            post_body = post_body[:497]
            post_body += " ..." 


        # Customize embed
        embed = EMBED_TEMPLATE.copy()
        embed.title = title
        embed.url = full_url
        embed.description = post_body
        embed.set_author(name=f'r/{submission.subreddit}', url=f'https://www.reddit.com/r/{submission.subreddit}')
        if url.endswith('.jpg') or url.endswith('.png') or url.endswith('.jpeg'): 
            embed.set_image(url=url)


        # Send embed and confirmation message
        await interaction.followup.send(embed=embed)
        print(f'Sent post from {YW}{submission.subreddit}{RES}: {submission.title}')


    
def setup(bot):
    bot.add_cog(Reddit(bot))