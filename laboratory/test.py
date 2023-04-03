from fuzzywuzzy import fuzz
# 創建翻譯字典，key为中文，value為日文
translation_dict = {
    'hello': '你好',
    'world': '世界',
    "寅武道虎次郎孫權":"寅武道とらじろう孫権",
    "婚禮吹雪姬小喬":"ウェディングふぶき姫小喬",
    "將星G吹雪姬小喬":"将星Gふぶき姫小喬",
    "將星G蛇王凱拉":"将星G蛇王カイラ",
    "將星麒麟曹丕":"将星麒麟曹丕"
}

# 取欲翻譯的字串
input_str = input('輸入中文字符串翻譯：')

# 分割输入字串並翻譯
closest_match = max(translation_dict.keys(), key=lambda x: fuzz.ratio(x, input_str))
# 有幾分接近，fuzz套件算出來的，0~100，越高對於與key值的相似程度越嚴格
match_ratio = fuzz.ratio(closest_match, input_str)

# 輸出
if match_ratio >= 50:
    print(translation_dict[closest_match])
else:
    print(input_str)#不太像字典的key，保持原樣輸出