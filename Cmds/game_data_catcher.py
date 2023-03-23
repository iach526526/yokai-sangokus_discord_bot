import discord,json
from discord.ext import commands
from discord.ui import Button
from core.classes import cog_extension
import urllib.request as req
import bs4,re#有用到正則表達式
with open("setting.json", 'r', encoding='utf-8') as setting_value:  # setting.json含有機器人的金鑰，不公開
    sv_data = json.load(setting_value)
class cather(cog_extension):
  @commands.command()
  async def find(self,ctx, i_want_to_find:str):
    get_url,got_name=Find_dedicated_page(i_want_to_find)
    await ctx.send(f"i got '{got_name}' from: {get_url}")
  @commands.command()
  async def getinfo(self,ctx, i_want_to_find:str):
    tagart_link,yokai_name=Find_dedicated_page(i_want_to_find)
    thumbnail,number_info,race_info,stand_info,sogou_eval,kokutou_eval,event_eval=search_detail(tagart_link,yokai_name)#接收回傳的縮圖、種族、站位資訊
    embed=discord.Embed(title=yokai_name, url=tagart_link, color=0xfbff14)
    embed.set_author(name="Each", url="https://github.com/iach526526", icon_url="https://i.imgur.com/fape9SN.png")
    embed.set_thumbnail(url=thumbnail)
    embed.add_field(name="じてん(辭典號碼)", value=number_info, inline=True)
    embed.add_field(name="【種族】", value=race_info, inline=True)
    embed.add_field(name="【立ち位置】", value=f"\t\t\t{stand_info}", inline=True)
    embed.add_field(name="総合評価", value=sogou_eval, inline=True)
    embed.add_field(name="国盗り評価", value=kokutou_eval,inline=True)
    embed.add_field(name="イベント評価", value=event_eval, inline=True)
    await ctx.send(embed=embed)
#回傳經BS套件整理後的網頁
def link_start(url:str):
  request = req.Request(
  url,
  headers={
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
  })
  with req.urlopen(request) as response:
    data = response.read().decode("utf-8")
  root = bs4.BeautifulSoup(data, "html.parser")
  return root
#回傳經BS套件整理後的網頁
def Find_dedicated_page(i_want_to_find:str):#尋找角色的介紹網址，傳入欲尋找的角色，傳回該角色的專屬網址
  ################連線到腳色一覽表格尋找特定角色的介紹網址#########################################
  root = link_start("https://game8.jp/youkai-sangokushi/421769")
  name_links = root.select(f".tablesorter td .a-link:contains('{i_want_to_find}')")
  if name_links:
      name_link = name_links[0]
      # print(name_link.text)
      # print(name_link['href'])
      tagart_link = name_link['href']
      return tagart_link,name_link.text
  else:#i_want_to_find的內容不存在於421769(天星的網頁)，往將星找下去
      root=link_start("https://game8.jp/youkai-sangokushi/262930")#將星的網頁
      name_links = root.select(f".tablesorter td .a-link:contains('{i_want_to_find}')")
      if name_links:
        name_link = name_links[0]
        # print(name_link.text)
        # print(name_link['href'])
        tagart_link = name_link['href']
        return tagart_link,name_link.text
      else:
        print(f"找不到名為 {i_want_to_find} 的角色")
def search_detail(tagart_link:str,i_want_to_find:str):#跳轉到角色詳細資料的那頁
  ##################連線到下一頁尋找評分、技能等資料#########################################
  root = link_start(tagart_link)
  find_img=root.find("img",alt=i_want_to_find)


  number_tag = root.find(string=re.compile('じてん'))#辭典號碼
  # 取得"じてん"標籤所在的父元素
  parent_tag = number_tag.find_parent("tr")
  # 取得"じてん"標籤所在的父元素中第一個span元素的內容
  number_info = parent_tag.select_one("span:nth-of-type(1)").text.strip()#辭典號碼


  race_tag = root.find(string="【種族】")
  # 取得"【種族】"標籤所在的父元素
  parent_tag = race_tag.find_parent("tr")
  # 取得"【種族】"標籤所在的父元素中第一個div元素的內容
  race_info = parent_tag.select_one("div:nth-of-type(1)").text.strip()#種族資訊

  stand_tag = root.find(string="【立ち位置】")
  parent_tag = stand_tag.find_parent("tr")
  stand_info = parent_tag.select_one("div:nth-of-type(1)").text.strip()#前、後排資訊


  tables = root.find_all('table')
  # 遍歷每個表格，查找包含“総合評価”的單元格
  for table in tables:#大部分記載評分的表格是在網頁中的第二個表格，不過有時會有一些意外
      rows = table.find_all('tr')
      for row in rows:
          cells = row.find_all('th')
          for cell in cells:
              if '総合評価' in cell.get_text():
                  # 找到了含有“総合評価”的表格
                  # print(table)
                  point_table=table
                  break

  # 総合評価
  sogou_eval = point_table.select_one("tr:nth-of-type(1) span").text.strip()

  # 国盗り評価
  kokutou_eval = point_table.select_one("tr:nth-of-type(2) span")
  if (kokutou_eval!=None):
     kokutou_eval=kokutou_eval.text.strip()
  print(kokutou_eval)
  # イベント評価
  event_eval = point_table.select_one("tr:nth-of-type(3) span")
  if (event_eval !=None):
    event_eval=event_eval.text.strip()
  return find_img['data-src'],number_info,race_info,stand_info,sogou_eval,kokutou_eval,event_eval


async def setup(bot):
    await bot.add_cog(cather(bot))