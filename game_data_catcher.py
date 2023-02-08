# import discord
# from discord.ext import commands
# from discord.ui import Button
# from core.classes import cog_extension
import urllib.request as req
import bs4,time
url="https://game8.jp/youkai-sangokushi/421769"
request=req.Request(url,headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
})

with req.urlopen(request) as response:
    time.sleep(3)
    data=response.read().decode("utf-8")
# class game8(cog_extension):

root=bs4.BeautifulSoup(data,"html.parser")
tar_detail_link=root.find("a",string="鬼王・羅仙呂布")
print(data)