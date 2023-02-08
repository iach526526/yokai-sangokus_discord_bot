import discord
from discord.ext import commands
from discord.ui import Button, View
import os,time,json,asyncio
with open("setting.json", 'r', encoding='utf-8') as setting_value:  # setting.json含有機器人的金鑰，不公開
    sv_data = json.load(setting_value)


intents = discord.Intents.all()
bot = commands.Bot(command_prefix='>>>', intents=intents)  # 前贅字符


@bot.event
async def on_ready():
    print("Bot in ready")
    game = discord.Game('努力學習py中')
    # discord.Status.<狀態>，可以是online,offline,idle,dnd,invisible
    await bot.change_presence(status=discord.Status.idle, activity=game)


@bot.command()
async def btm(ctx):
    buttom=Button(label='click',style=discord.ButtonStyle.green,emoji="✌")
    view=View()
    view.add_item(buttom)
    await ctx.send("Hi",view=view)
# # 未完


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
