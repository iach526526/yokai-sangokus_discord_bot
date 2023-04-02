import urllib.request as req
import bs4
import re
#列出該rank所有角色名稱
def link_start(url:str):#函式會回傳經BS套件整理後的網頁
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
#列出該頁所有角色
url="https://game8.jp/youkai-sangokushi/262930"#將星的網頁
root=link_start(url)
name_links = root.select(".tablesorter td .a-link")
flag=1
for i in name_links:
  if flag%2==0:
    flag+=1
    continue
  print(i.text)
  flag+=1