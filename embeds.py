import nextcord
from colors import ERROR_COLOR, EMBED_COLOR, BRAND_COLOR



# Specific
INVALID_PERMISSIONS = nextcord.Embed(
    color=ERROR_COLOR,
    title='Invalid Permissions',
    description="You don't have the right permissions to use that command."
)
INVALID_INPUT_EMBED = nextcord.Embed(
    color=ERROR_COLOR,
    title='Invalid input',
    description='Please try again.'
)
WORD_NOT_FOUND_EMBED = nextcord.Embed(
    color=ERROR_COLOR,
    title='Word not found',
    description="Couldn't find that word."
)


# Generic
ERROR_TEMPLATE = nextcord.Embed(color=ERROR_COLOR)
EMBED_TEMPLATE = nextcord.Embed(color=EMBED_COLOR)
BRAND_TEMPLATE = nextcord.Embed(color=BRAND_COLOR)
UPCOMING_EMBED = nextcord.Embed(color=BRAND_COLOR, title='Feature coming soon', description="That command isn't supported yet.")