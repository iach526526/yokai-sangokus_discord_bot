import nextcord
from nextcord.ext import commands
from nextcord.ui import Button, View
import os
import time
import json
import asyncio
with open("setting.json", 'r', encoding='utf-8') as setting_value:  # setting.json含有機器人的金鑰，不公開
    sv_data = json.load(setting_value)


intents = nextcord.Intents.all()
bot = commands.Bot(command_prefix='>>', intents=intents)  # 前贅字符


@bot.event
async def on_ready():
    print("Bot in ready")
    game = nextcord.Game('離恨樓裡生離恨💖測試')
    # nextcord.Status.<狀態>，可以是online,offline,idle,dnd,invisible
    await bot.change_presence(status=nextcord.Status.idle, activity=game)


@bot.command()
async def btm(ctx):
    # await ctx.send("loading...")
    # await ctx.guild.id(ctx.guild.id)
    if ctx.guild.id == int("1000338680243834880"):
        buttom = Button(
            label='click', style=nextcord.ButtonStyle.green, emoji="✌")
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
    tasks = []
    for filename in os.listdir("./Cmds/"):
        if filename.endswith('.py'):
            print(f"i read:{filename}^_^")
            task = bot.load_extension(f"Cmds.{filename[:-3]}")
            tasks.append(task)
    await asyncio.gather(*tasks)


async def test():
    await cog()
    await bot.start(sv_data['token'])
if __name__ == "__main__":
    asyncio.run(test())