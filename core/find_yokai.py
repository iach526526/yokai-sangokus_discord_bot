import re  # 有用到正則表達式
from core.make_link import link_start
# 回傳經BS套件整理後的網頁
def Find_dedicated_page(i_want_to_find: str):  # 尋找角色的介紹網址，傳入欲尋找的角色，傳回該角色的專屬網址
    ################連線到腳色一覽表格尋找特定角色的介紹網址#########################################
    root = link_start("https://game8.jp/youkai-sangokushi/421769")
    name_links = root.select(
        f".tablesorter td .a-link:contains('{i_want_to_find}')")
    if name_links:
        name_link = name_links[0]
        # print(name_link.text)
        # print(name_link['href'])
        tagart_link = name_link['href']
        return tagart_link, name_link.text
    else:  # i_want_to_find的內容不存在於421769(天星的網頁)，往將星找下去
        root = link_start("https://game8.jp/youkai-sangokushi/262930")  # 將星的網頁
        name_links = root.select(
            f".tablesorter td .a-link:contains('{i_want_to_find}')")
        if name_links:
            name_link = name_links[0]
            # print(name_link.text)
            # print(name_link['href'])
            tagart_link = name_link['href']
            return tagart_link, name_link.text
        else:
            return None,None
#--------------------舊版網頁--------------------------------------------------
def old(root):
    number_tag = root.find(string=re.compile('じてん'))  # 辭典號碼
    # 取得"じてん"標籤所在的父元素
    parent_tag = number_tag.find_parent("tr")
    # 取得"じてん"標籤所在的父元素中第一個span元素的內容
    number_info = parent_tag.select_one(
        "span:nth-of-type(1)").text.strip()  # 辭典號碼

    race_tag = root.find(string="【種族】")
    # 取得"【種族】"標籤所在的父元素
    parent_tag = race_tag.find_parent("tr")
    # 取得"【種族】"標籤所在的父元素中第一個div元素的內容
    race_info = parent_tag.select_one(
        "div:nth-of-type(1)").text.strip()  # 種族資訊

    stand_tag = root.find(string="【立ち位置】")
    parent_tag = stand_tag.find_parent("tr")
    stand_info = parent_tag.select_one(
        "div:nth-of-type(1)").text.strip()  # 前、後排資訊

    # 查找包含“総合評価”的單元格
    point_table = root.find('th', string=lambda text: text and "総合評価" in text).find_parent(
        'table')  # 定位到寫有角色評分的表格
    # 総合評価
    sogou_eval = point_table.select_one("tr:nth-of-type(1) span").text.strip()
    # 國戰評價和活動評價可能會沒有，若無直接回傳none，有的話要把該標籤的原始碼抓出來取文字，如果是None不能做text.strip()
    # 国盗り評価(可能沒有)
    kokutou_eval = point_table.select_one("tr:nth-of-type(2) span")
    if (kokutou_eval != None):
        kokutou_eval = kokutou_eval.text.strip()
    # イベント(活動)評価(可能沒有)
    event_eval = point_table.select_one("tr:nth-of-type(3) span")
    if (event_eval != None):
        event_eval = event_eval.text.strip()
    return number_info, race_info, stand_info, sogou_eval, kokutou_eval, event_eval
# --------------------新版網頁--------------------------------------------------


def new_page(i_want_to_find, root):
    num = root.find(string=re.compile(r"【じて"))
    # 取得該 `td` 元素中的文字內容
    if num:  # 找出辭典編號
        number_info = num.parent.find(string=re.compile(r'\d+'))  # 找td
        #print(number_info.text)
    script_table = root.find('th', string=lambda text: text and i_want_to_find in text).find_parent(
        'table')  # 定位到寫有角色詳細的表格

    # for i in script_table:
    #    print(i.get_text(strip=True))
    imgs = script_table.find_all('img')
    # 檢查img標籤的alt
    turn = 0  # 計數器
    for text_in_tag in imgs:
        text_in_tag = text_in_tag.get('alt').replace(
            "アイコン", "")  # 把日文的アイコン(image)刪除，它們會在alt加上XXX的images
        # 網頁圖片排版是固定的，種族(0)、rank(1)、角色縮圖(2)、前後衛資訊(3)會按照順序出現，故可以這樣寫
        if turn == 0:
            race_info = text_in_tag
        if turn == 3:
            stand_info = text_in_tag
        # print(str(turn)+text_in_tag)
        turn += 1
    # 進第二張表格
    point_table = root.find('th', string=lambda text: text and "総合評価" in text).find_parent(
        'table')  # 定位到寫有角色評分的表格
    point_rows = point_table.find_all('tr')
    # 取得總評分
    sogou_eval = point_rows[1].find_all('td')[0].text.strip()
    # 取得兩個評分
    event_eval = point_rows[2].find_all('td')[0].text.strip()
    kokutou_eval = point_rows[2].find_all('td')[1].text.strip()

    return number_info, race_info, stand_info, sogou_eval, kokutou_eval, event_eval

def search_detail(tagart_link:str,i_want_to_find:str):#跳轉到角色詳細資料的那頁
    ##################連線到下一頁尋找評分、技能等資料#########################################
    root = link_start(tagart_link)
    flag=False#判斷是否為新排版的旗標，True為是新版。舊版網頁大多用字串搜尋的可以找到資料，新版需要去看img的alt，寫法不同，分別呼叫函式new_page、old
    images = root.find_all("img")#找角色縮圖順便判斷是新的排版方式還是舊的選擇不同爬取方式
    for image in images:
        alt_text = image.get("alt")
        if alt_text=='妖怪':#另一種排版方式的依據，如果有找到那張alt=妖怪的圖片代表為新版
            flag=True
            continue
        if alt_text ==i_want_to_find:
            find_img=image['data-src']#找出角色縮略圖
            break
    if flag:
        number_info,race_info,stand_info,sogou_eval,kokutou_eval,event_eval=new_page(i_want_to_find,root)
    else:
        number_info,race_info,stand_info,sogou_eval,kokutou_eval,event_eval=old(root)
    return find_img,number_info,race_info,stand_info,sogou_eval,kokutou_eval,event_eval