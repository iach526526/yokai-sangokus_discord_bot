import discord
import json
from discord.ext import commands
from discord.ui import Button
from core.classes import cog_extension
with open("game_data.json", 'r', encoding="utf-8") as game_data:
    gm_data = json.load(game_data)


class coin_finder(cog_extension):
    # # 查找硬幣內容
    @commands.hybrid_group(fallback="get")
    async def yokaicoin(self, ctx):
        await ctx.send(gm_data["coin_help"])

    @yokaicoin.command()
    async def jstar5(self, ctx):
        await ctx.send(gm_data["jstar5"])

    @yokaicoin.command()
    async def jstar4(self, ctx):
        await ctx.send(gm_data["jstar4"])

    @yokaicoin.command()
    async def jstar6(self, ctx):
        await ctx.send(gm_data["jstar6"])


async def setup(bot):
    await bot.add_cog(coin_finder(bot))
