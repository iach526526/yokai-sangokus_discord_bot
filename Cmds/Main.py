import discord
from discord.ext import commands
from discord.ui import Button
from core.classes import cog_extension
class Main(cog_extension):
    @commands.command()
    async def hello(self,ctx):
        await ctx.send(f"hello<@{ctx.author.id}>")


    @commands.command()
    async def cls(self,ctx, num: int):
        await ctx.channel.purge(limit=num+1)
        
async def setup(bot):
    await bot.add_cog(Main(bot))