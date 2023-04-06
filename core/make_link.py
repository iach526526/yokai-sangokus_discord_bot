#連到網頁並回傳經beautifulsoup處理過的HTML樹
import urllib.request as req
import bs4
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
