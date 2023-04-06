import discord,json
from discord.ext import commands
from discord import app_commands
from core.classes import cog_extension
#引入自己寫在core的函式，使這頁更簡潔
from core.translate import trans
from core.find_yokai import Find_dedicated_page,search_detail
with open("setting.json", 'r', encoding='utf-8') as setting_value:  # setting.json含有機器人的金鑰，不公開
    sv_data = json.load(setting_value)
class cather(cog_extension):
    @app_commands.command(name='尋找角色' ,description="單純尋找角色頁網址，不查詳細資訊")
    async def find(self,interaction:discord.Interaction, i_want_to_find:str,公開訊息:bool=True):
        i_want_to_find=trans(i_want_to_find)#丟去trans函式(在core/translate.py)翻譯
        get_url,got_name=Find_dedicated_page(i_want_to_find)
        await interaction.response.send_message(f"i got '{got_name}' from: {get_url}",ephemeral=公開訊息)
    @app_commands.command(name='getinfo' ,description="尋找角色資訊(包含評分、種族等詳細資訊)")
    async def getinfo(self,interaction:discord.Interaction, i_want_to_find:str,invisible:bool=True):
        orginial_emb=discord.Embed(title="loading",description="努力加載中")
        await interaction.response.send_message(embed=orginial_emb,ephemeral=invisible)
        msg=await interaction.original_response()
        i_want_to_find=trans(i_want_to_find)#丟去trans函式(在core/translate.py)翻譯
        tagart_link,yokai_name=Find_dedicated_page(i_want_to_find)
        result=exist_error(tagart_link,yokai_name,i_want_to_find)
        print(f"result:{result}")
        if not (result):
            #正常輸出
            thumbnail,number_info,race_info,stand_info,sogou_eval,kokutou_eval,event_eval=search_detail(tagart_link,yokai_name)#接收回傳的縮圖、種族、站位資訊
            info_embed=make_embed(yokai_name,tagart_link,thumbnail,number_info,race_info,stand_info,sogou_eval,kokutou_eval,event_eval)#把蒐集到的資訊到的資訊做成DC嵌入訊息
            print(msg)
            await msg.edit(embed=info_embed)
            #print(thumbnail,number_info,race_info,stand_info,sogou_eval,kokutou_eval,event_eval)#測試用程式
        else:
        #回傳erro訊息
            await msg.edit(embed=result)
#函式區
def exist_error(link,yokai_name,you_want_to_find):#確認Find_dedicated_page函式有回傳東西，不為None
   if ((not link) or (not yokai_name)):
      embed = discord.Embed(title=f"找不到'{you_want_to_find}'")
      embed.add_field(name="欸若(error)啦", value="請檢查角色名稱再試一次", inline=True)
      return embed
   else:
      return None


def make_embed(yokai_name,tagart_link,thumbnail,number_info,race_info,stand_info,sogou_eval,kokutou_eval,event_eval):
    embed=discord.Embed(title=yokai_name, url=tagart_link, color=0xfbff14)
    embed.set_author(name="Each", url="https://github.com/iach526526", icon_url="https://i.imgur.com/fape9SN.png")
    embed.set_thumbnail(url=thumbnail)
    embed.add_field(name="じてん(辭典號碼)", value=number_info, inline=True)
    embed.add_field(name="【種族】", value=race_info, inline=True)
    embed.add_field(name="【立ち位置】", value=f"\t\t\t{stand_info}", inline=True)
    embed.add_field(name="総合評価", value=sogou_eval, inline=True)
    embed.add_field(name="国盗り評価", value=kokutou_eval,inline=True)
    embed.add_field(name="イベント評価", value=event_eval, inline=True)
    # print(thumbnail,number_info,race_info,stand_info,sogou_eval,kokutou_eval,event_eval)#測試用程式
    # print(embed)
    return embed
async def setup(bot):
    await bot.add_cog(cather(bot))
