import discord
from discord.ext import commands
import time
import json
with open("setting.json", 'r', encoding='utf-8') as setting_value:#setting.json含有機器人的金鑰，不公開
    sv_data = json.load(setting_value)
with open("game_data.json",'r',encoding="utf-8") as game_data:
    gm_data=json.load(game_data)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='-', intents=intents)  # 前贅字符

@bot.event
async def on_ready():
    print("Bot in ready")


@bot.command()
async def hello(ctx):
    await ctx.send(f"hello<@{ctx.author.id}>")


@bot.command()
async def cls(ctx, num: int):
    await ctx.channel.purge(limit=num+1)


@bot.command()
async def nowact(ctx):
    embed = discord.Embed(title="第三次極限特攻：塗黑卡門賈詡",
                          description="前半BOSS 蛇型後衛 無減傷 弱點土。排名獎勵前半是書，後半將DX道具，大家要保持好名次拿到道具哦!能多一將", color=0xffae00)
    embed.set_author(name="妖狐獸")
    embed.add_field(
        name="特性", value="不會〔摸魚〕〔混亂〕〔超摸魚〕〔超混亂〕〔睡眠〕妖氣量關聯技能效果減半（降妖氣、加妖氣等等）", inline=True)
    embed.add_field(name="特攻角色", value="諾亞A、活動軍魔（新郎新娘）增傷、受到的傷減少", inline=False)
    embed.add_field(name="6.5 S蛇形 塗黑卡門賈詡",
                    value=" 妖術:吸收 冰抗性 火弱點（有可能會是後半戰BOSS的抗性)", inline=True)
    embed.add_field(name="技能", value=" 全體吸血+降命中+持續傷害+敵全體妖氣-10%", inline=True)
    embed.add_field(
        name="潛在能力", value="對暖暖加傷25%、80%持續傷害消除、有利種族附身+3秒、衝撞減傷30%", inline=True)
    embed.add_field(name="6.5 將蛇形 塗黑卡門賈詡", value="妖術:吸收 冰抗性 火弱點", inline=True)
    embed.add_field(
        name="技能", value="全體吸血+降命中+持續傷害+敵全體妖氣-（10～25？）%", inline=True)
    embed.add_field(
        name="潛在能力", value="潛在能力：對暖暖加傷50%、50%火減傷、80%持續傷害消除、有利種族附身+5秒、衝撞減傷40% ", inline=True)
    await ctx.channel.purge(limit=1)
    await ctx.send(embed=embed)

#未完
@bot.command()
async def hardlevels(ctx):
    output_arr = []
    for i in range(2):
        output_arr.append(gm_data["hard_levels"][i]["name"] +
                          gm_data["hard_levels"][i]["type"]+gm_data["hard_levels"][i]["work"])
    await ctx.send(output_arr)
#未完
#查找硬幣內容
@bot.hybrid_group(fallback="get")
async def yokaicoin(ctx):
    await ctx.send(gm_data["coin_help"])

@yokaicoin.command()
async def jstar5(ctx):
    await ctx.send(gm_data["jstar5"])

@yokaicoin.command()
async def jstar4(ctx):
    await ctx.send(gm_data["jstar4"])

# @bot.command()
# async def invisible(ctx):#invisible
#     # await ctx.send(ctx.guild.members)
#     for member in ctx.guild.members:
#         if str(member.status)=='invisible':
#             await ctx.send(member.name)

bot.run(sv_data['token'])
