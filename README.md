# Rainy Bot
Rainy Bot is a multi-use Discord bot that I use in my servers. It has several functions (outlined below) and I would love to try new functions. Pop an idea in the [issues](https://github.com/tholley7/Rainy_Bot/issues) tab if you have an idea for a new feature and I will do my best to implement it!


## Commands

### Current
- `/help` displays a list of all available commands (different list for admins and non-admins).
- `/randompost <subreddit_name>` gets a random post from the specified subreddit.
- `/roll <(x)d(y)>` rolls x dice with y sides (e.g. "/roll 4d6" rolls four 6-sded dice).
- `/define <word>` defines the word passed in using the [Free Dictionary API](https://dictionaryapi.dev/).
- `/pronouns` sends an embed with buttons to set pronouns [Admin Only]
- `/rules` sends rules message to channel [Owner Only]
- `/urban <word>` defines the word with Urban Dictionary

### Planned
- `/dms` sends an embed with buttons to set DM permissions to DMs Open, DMs Closed, or Ask to DM [Owner Only]
- `/unsplash <search_term>` returns a random post from unsplash OR a random post from search


## Built With
- [Nextcord](https://nextcord.readthedocs.io/) - Discord API wrapper
- [Async PRAW](https://asyncpraw.readthedocs.io/en/stable/code_overview/models/subreddit.html) - Asynchronous Reddit API wrapper
- [Colorama](https://pypi.org/project/colorama/) - Colorful console outputs
- [AIOHTTP](https://docs.aiohttp.org/en/stable/) - Asynchronous HTTP Client/Server
- [udpy](https://pypi.org/project/udpy/) - Urban Dictionary API Wrapper


## Contributors
- Tyler Holley


## License
This project is licensed under the **MIT License** - see the [LICENSE.md](LICENSE.md) file for details.


## Acknowledgements
Inspired by Milesnocte's [WoodyBot](https://github.com/Milesnocte/WoodyBot)