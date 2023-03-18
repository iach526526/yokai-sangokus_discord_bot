#這是不含Discord訊息輸出的終端機測試版
import urllib.request as req
import bs4
################連線到腳色一覽表格尋找特定角色的介紹網址#########################################
url = "https://game8.jp/youkai-sangokushi/421769"
request = req.Request(
  url,
  headers={
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
  })



with req.urlopen(request) as response:
  data = response.read().decode("utf-8")
root = bs4.BeautifulSoup(data, "html.parser")
# get_table = root.select(".tablesorter td .a-link")  #傳回角色表格裡包含角色名字的a標籤
i_want_to_find = "冥土野花子蔡琰"
name_links = root.select(f".tablesorter td .a-link:contains('{i_want_to_find}')")
#尋找表格中的值=i_want_to_find
if name_links:
    name_link = name_links[0]
    print(name_link.text)
    print(name_link['href'])
    tagart_link = name_link['href']
    print("\n")
else:
    print(f"找不到名為 {i_want_to_find} 的角色")
###################連線到下一頁尋找評分、技能等資料#########################################
request = req.Request(
  tagart_link,
  headers={
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
  })
with req.urlopen(request) as response:
  data = response.read().decode("utf-8")
root = bs4.BeautifulSoup(data, "html.parser")

get_detail = root.select(".archive-style-wrapper .a-table tr td") 
print(root.find(string=i_want_to_find))
find_img=root.find("img",alt=i_want_to_find)
print(find_img['data-src'])
import re

number_tag = root.find(string=re.compile('じてん'))#辭典號碼
# 取得"じてん"標籤所在的父元素
parent_tag = number_tag.find_parent("tr")
# 取得"じてん"標籤所在的父元素中第一個span元素的內容
number_info = parent_tag.select_one("span:nth-of-type(1)").text.strip()#種族資訊
print(number_info)

race_tag = root.find(string="【種族】")
# 取得"【種族】"標籤所在的父元素
parent_tag = race_tag.find_parent("tr")
# 取得"【種族】"標籤所在的父元素中尋找第一個div元素的內容
race_info = parent_tag.select_one("div:nth-of-type(1)").text.strip()#種族資訊
print(race_info)

stand_tag = root.find(string="【立ち位置】")
parent_tag = stand_tag.find_parent("tr")
stand_info = parent_tag.select_one("div:nth-of-type(1)").text.strip()#前、後排資訊
print(stand_info)

tables = root.find_all('table')
# 遍歷每個表格，查找包含“総合評価”的單元格
for table in tables:#大部分記載評分的表格是在網頁中的第二個表格，不過有時會有一些例外
    rows = table.find_all('tr')
    for row in rows:
        cells = row.find_all('th')
        for cell in cells:
            if '総合評価' in cell.get_text():
                # 找到了含有“総合評価”的表格
                # print(table)
                second_table=table
                break

# 総合評価
sogou_eval = second_table.select_one("tr span").text.strip()

# 国盗り評価
kokutou_eval = second_table.select_one("tr:nth-of-type(2) span").text.strip()

# イベント評価
event_eval = second_table.select_one("tr:nth-of-type(3) span").text.strip()

print(sogou_eval)
print(kokutou_eval)
print(event_eval)



# get_detail = get_detail.select(".archive-style-wrapper .a-table tr td") 
# print(root.find(string="【種族】"))
# race=root.find("tr",string="【種族】")
# print(race)





# print(get_detail)
# a_tags = root.find_all(['td','a'])
# for tag in a_tags:
#   print(tag)
