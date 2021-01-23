import json
import requests
import urllib.parse as urlparse

requests.packages.urllib3.disable_warnings()


url = "https://hk4e-api.mihoyo.com/event/gacha_info/api/getGachaLog?authkey_ver=1&sign_type=2&auth_appid=webview_gacha&init_type=301&gacha_id=2ffa459718702872a52867fa0521e32b6843b0&lang=zh-cn&device_type=pc&ext=%7b%22loc%22%3a%7b%22x%22%3a-659.7898559570313%2c%22y%22%3a224.739013671875%2c%22z%22%3a204.33694458007813%7d%2c%22platform%22%3a%22WinST%22%7d&game_version=CNRELWin1.2.0_R1771533_S1847412_D1816310&region=cn_gf01&authkey=h22N3%2bI3x8B54PJf96l%2bYYjgEL%2bUV0WD4P4Uy6gq17tMCusJKqIZID4ZWfBn8YDXlQnuJgPrGfP0vT0orauB%2bbLVZkHcfLbxY2kiMOT0wdTwDHpZ1WS8KYqN5ehX6k4sGjFmerYj98i40EOWDKT7A6YQ5cKTyfp3bhV0%2b1v0ZK%2btRy18glxS4%2fYEIFYOdnkWoo3Uo1Hm8cneGqGhxebT1JCFM3EZQUFfZc%2b5hig0uXMl%2b%2f3WEqyg2MgSPg2O4nnGNOJd2bwdP7kF6DbYdnr%2bZa4qjGsGfqNT%2br3YYmj%2f0qCKa1WmjbGSNvNWtf344oEfiFq0qhURjCXBrJk9o3oZKZ679wHCQpm58%2fOegXwRZ4aR8mC7NQ9nQgk5xtfn%2focaJNt1JzZamkiqVhsvzTPNfEYPjDHxeJGWoPq1D%2fyHxGPq3C4A4M%2b9aOGrlFGMSiP0fGm3CSuTibVmY2%2bBsQTz8BWwpygl9ZPs4COX%2fZSJNCMN6j5FYh4m9v2C8pq8VMxCNQ%2bKKDqC8H9DtYnY2iJDjk%2fc8hd4nn4LgdWZCzaOFKX9PlU5UlG0XZWA2qWrKuzx22pz6mZnMU1U%2fLr1%2fntp%2f8HJFm02ECvu0rre9wt2b6oRnY4mMj8oQoUgk1hsov6uXDKvHv7eij3FOEHPi4JRTJQId2BuKk9yGBrd2Z62XFTsjOGNGOnD0hdO%2fq3nvFI%2f0%2bNAg76DZ2B%2bBAyRs2RKLoAI7NYClxxp8M5%2f1ULcOaW%2bUy8mg4r323%2fi%2fJCcb2yt48orzcFIPQM4lDTgkWI5aGQZMil638EBuPbKEdfthOEpgxrn1lIYw2OUQsDbPlYGWlSgqRVv0JIYIwqJi9AvjxapLiSnyYLM2fW6G9QK8k218bxvSwvvOfUzxcz0YKZPHOa5kc3DKpvWhWfrokuZv9BMHJB%2b%2bi1sinfx4kvVdGeeX5dULFTI%2bZduKYS3qzfYvWWn5YNh9%2bkwXQNhbi955eRmH41rQeGCWr52sa8T1%2fNBTRuJCheQLrbm7DSyjdNG&game_biz=hk4e_cn&gacha_type=301&page=3&size=6"


def getApi(gacha_type, size, page):
    parsed = urlparse.urlparse(url)
    querys = urlparse.parse_qsl(parsed.query)
    param_dict = dict(querys)
    param_dict["size"] = size
    param_dict["gacha_type"] = gacha_type
    param_dict["page"] = page
    param = urlparse.urlencode(param_dict)
    path = url.split("?")[0]
    api = path + "?" + param
    return api


def getQueryVariable(variable):
    query = url.split("?")[1]
    vars = query.split("&")
    for v in vars:
        if v.split("=")[0] == variable:
            return v.split("=")[1]
    return ""


def getInfo(item_id):
    for info in gacha_info:
        if info["item_id"] == item_id:
            return info["name"] + "," + info["item_type"] + "," + info["rank_type"]
    return "物品ID未找到"


def checkApi(url):
    if not url:
        print("未填入url")
        exit()
    if "getGachaLog" not in url:
        print("错误的url，检查是否包含getGachaLog")
        exit()
    try:
        r = requests.get(url, verify=False)
        s = r.content.decode("utf-8")
        j = json.loads(s)
    except Exception as e:
        print("API请求解析出错：" + str(e))
        exit()

    if not j["data"]:
        if j["message"] == "authkey valid error":
            print("authkey错误，请重新抓包获取url")
        else:
            print("数据为空，错误代码：" + j["message"])
        exit()


checkApi(url)

r = requests.get(url.replace("getGachaLog", "getConfigList"), verify=False)
s = r.content.decode("utf-8")
configList = json.loads(s)
gacha_types = []
for banner in configList["data"]["gacha_type_list"]:
    gacha_types.append(banner["key"])
# print(gacha_types)

region = getQueryVariable("region")
lang = getQueryVariable("lang")
gachaInfoUrl = "https://webstatic.mihoyo.com/hk4e/gacha_info/{}/items/{}.json".format(region, lang)
r = requests.get(gachaInfoUrl, verify=False)
s = r.content.decode("utf-8")
gacha_info = json.loads(s)
# print(gacha_info)

size = "20"
# api限制一页最大20
for gacha_type in gacha_types:
    filename = "gacha" + gacha_type + ".csv"
    f = open(filename, "w", encoding="UTF-8")
    for page in range(1, 9999):
        api = getApi(gacha_type, size, page)
        r = requests.get(api, verify=False)
        s = r.content.decode("utf-8")
        j = json.loads(s)

        gacha = j["data"]["list"]
        if not len(gacha):
            break
        for i in gacha:
            time = i["time"]
            item_id = i["item_id"]
            info = time + "," + item_id + "," + getInfo(item_id)
            print(info)
            f.write(info + "\n")
    f.close()
    # 添加BOM防止乱码
    with open(filename, encoding="utf-8") as f:
        content = f.read()
        if content != "":
            content = "\ufeff" + content
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
