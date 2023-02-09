import discord,json
from discord.ext import commands
from discord.ui import Button
from core.classes import cog_extension
with open("setting.json", 'r', encoding='utf-8') as setting_value:  # setting.json含有機器人的金鑰，不公開
    sv_data = json.load(setting_value)
class system(cog_extension):
    @commands.Cog.listener()
    async def on_member_join(self,member):
        channel=self.bot.get_channel(int(sv_data["wellcome_channel"]))
        await channel.send(F"嗨!<@{member.id}>"+sv_data["wellcome_text"])
    #     print("in")
    @commands.Cog.listener()
    async def on_member_remove(self,member):
        channel=self.bot.get_channel(int(sv_data["wellcome_channel"]))
        await channel.send(F"{member}"+sv_data["left_text"])
    @commands.command()
    async def hello(self,ctx):
        await ctx.send(f"hello<@{ctx.author.id}>")


    @commands.command()
    async def cls(self,ctx, num: int):
        await ctx.channel.purge(limit=num+1)
        
async def setup(bot):
    await bot.add_cog(system(bot))