import discord,json
from discord import app_commands
from discord.ext import commands
from discord.ui import Button
from core.classes import cog_extension
with open("setting.json", 'r', encoding='utf-8') as setting_value:  # setting.json含有機器人的金鑰，不公開
    sv_data = json.load(setting_value)


class system(cog_extension):
    @commands.Cog.listener()  # 歡迎離開訊息限用於我的伺服器，否則在有這隻機器人的其他伺服器退出會在我伺服器的歡迎頻跳通知
    async def on_member_join(self, member):
        if member.guild.id == int(sv_data["伺服器id"]):
            channel = self.bot.get_channel(int(sv_data["wellcome_channel"]))
            await channel.send(F"嗨!<@{member.id}>"+sv_data["wellcome_text"])

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if member.guild.id == int(sv_data["伺服器id"]):
            channel = self.bot.get_channel(int(sv_data["wellcome_channel"]))
            await channel.send(F"{member}"+sv_data["left_text"])
        else:
            print("遙遠的彼方有人退出")  # 這是悄悄話，只有你知道歐

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.startswith(':omo:'):
            channel = message.channel
            await channel.send('Send me that 👍 reaction, mate')

            def check(reaction, user):
                return user == message.author and str(reaction.emoji) == '👍'

            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
            except self.asyncio.TimeoutError:
                await channel.send('👎')
            else:
                await channel.send('👍')

    @commands.command()
    async def sync(self,ctx)->None:
        fmt=await ctx.bot.tree.sync()
        await ctx.send(f"同步了{fmt}")
        return
    @app_commands.command(name='prepare' ,description="prepare system")
    async def system(self,interaction:discord.Interaction,s:str):
        await interaction.response.send_message(f"prepare system:{s}",ephemeral=False)
    @commands.command()
    async def id(self, ctx):
        await ctx.send(f"hello<@{ctx.author.id}>")

    @commands.command()#刪訊息
    async def cls(self,ctx, num: int):
        await ctx.channel.purge(limit=num+1)


async def setup(bot):
    await bot.add_cog(system(bot))#,guilds=[discord.Object(bot)]
