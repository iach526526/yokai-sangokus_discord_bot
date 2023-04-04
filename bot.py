import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Button, View
import os
import json
import asyncio
with open("setting.json", 'r', encoding='utf-8') as setting_value:  # setting.json含有機器人的金鑰等我的伺服器專屬的資料，不公開
    sv_data = json.load(setting_value)



intents = discord.Intents.all()
bot = commands.Bot(command_prefix='>>', intents=intents,# 前贅字符
                   description="This is a bot that can do many things!",#help指令出現的描述
                   applicatcion_id='1071341160947265536')#ID


@bot.event
async def on_ready():
    print("Bot in ready")
    game = discord.Game('離恨樓裡生離恨💖測試')
    # discord.Status.<狀態>，可以是online,offline,idle,dnd,invisible
    for guild in bot.guilds:
        print(guild.name)
    await bot.change_presence(status=discord.Status.idle, activity=game)


@bot.command(name="btm", description="btm_test")
async def btm(ctx):
    # await ctx.send("loading...")
    # await ctx.guild.id(ctx.guild.id)
    if ctx.guild.id == int("1000338680243834880"):
        buttom = Button(
            label='click', style=discord.ButtonStyle.green, emoji="✌")
        view = View()
        view.add_item(buttom)
        await ctx.send("Hi", view=view)
    else:
        await ctx.send("guild is incorrect")
    await ctx.send("done")
# # 未完



@bot.command()
async def sh_id(ctx):
    await ctx.send("loading")

    # print("now_guild")
    await ctx.send(ctx.guild.id)
    await ctx.send("done")

# @bot.command()
# async def hardlevels(ctx):
#     output_arr = []
#     for i in range(2):
#         output_arr.append(gm_data["hard_levels"][i]["name"] +
#                           gm_data["hard_levels"][i]["type"]+gm_data["hard_levels"][i]["work"])
#     await ctx.send(output_arr)
# # 未完


async def cog():
    for filename in os.listdir("./Cmds/"):
        if filename.endswith('.py'):
            print(f"i read:{filename}^_^")
            await bot.load_extension(f"Cmds.{filename[:-3]}")
async def test():
    async with bot:
        await cog()
        await bot.start(sv_data['token'])
if __name__ == "__main__":
    asyncio.run(test())