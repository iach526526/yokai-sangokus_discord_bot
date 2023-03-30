import nextcord
from nextcord.ext import commands


class cog_extension(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
