import nextcord
from colors import ERROR_COLOR, EMBED_COLOR, BRAND_COLOR

ERROR_TEMPLATE = nextcord.Embed(color=ERROR_COLOR)
EMBED_TEMPLATE = nextcord.Embed(color=EMBED_COLOR)
UPCOMING_EMBED = nextcord.Embed(color=BRAND_COLOR, title='Feature coming soon', description="That command isn't supported yet.")