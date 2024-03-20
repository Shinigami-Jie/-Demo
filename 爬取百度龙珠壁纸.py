import os
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver


def getPhoto(url, dirName, fileName="wallpapers",count=5):
    # 请求头
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.95 Safari/537.36",
        "Referer": "https://www.baidu.com/",
        "Connection": "close",
        "Cookie": "BDqhfp=%E5%81%87%E9%9D%A2%E9%AA%91%E5%A3%AB%E5%A3%81%E7%BA%B8%26%26-10-1undefined%26%260%26%261; PSTM=1641373116; BIDUPSID=6A027138EA12E88CD4148423E2469E12; H_WISE_SIDS=110085_269904_271170_274777_275171_276572_277161_270102_277354_277641_277636_275732_259642_278053_278512_278791_278388_279075_279613_277758_279749_279998_276711_280266_278414_280614_280651_280721_280809_280557_280636_267170_281043_280852_280169_277970_281233_281367_279203_281392_280437_280371_8000065_8000111_8000123_8000141_8000146_8000163_8000173_8000178_8000179_8000182_8000195_8000203; BDUSS=Vyc01GWX5xOTltMFR4alA1SVhLWWFFNzBMOH5OeWo3cn5URUJMRDNiU1BTLWRsRVFBQUFBJCQAAAAAAAAAAAEAAAAQmk-xVWx0cmFtYW5LeW9kYWkAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAI--v2WPvr9lb1; BDUSS_BFESS=Vyc01GWX5xOTltMFR4alA1SVhLWWFFNzBMOH5OeWo3cn5URUJMRDNiU1BTLWRsRVFBQUFBJCQAAAAAAAAAAAEAAAAQmk-xVWx0cmFtYW5LeW9kYWkAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAI--v2WPvr9lb1; BAIDUID=D8E53E467CD50B300741AB9EFC4E22F2:FG=1; ZFY=CFHwmfdO4N4U7a0BP1dfZsGcMtK:A8YWBeC:AJ3PY8kYo:C; BAIDUID_BFESS=D8E53E467CD50B300741AB9EFC4E22F2:FG=1; H_WISE_SIDS_BFESS=110085_269904_271170_274777_275171_276572_277161_270102_277354_277641_277636_275732_259642_278053_278512_278791_278388_279075_279613_277758_279749_279998_276711_280266_278414_280614_280651_280721_280809_280557_280636_267170_281043_280852_280169_277970_281233_281367_279203_281392_280437_280371_8000065_8000111_8000123_8000141_8000146_8000163_8000173_8000178_8000179_8000182_8000195_8000203; H_PS_PSSID=40207_40216_40223_40254_40295_40290_40287_40286_40317_40079_40364_40368_40376_40360_40335_40416; BA_HECTOR=2gak85a08k8h800g2g24a1814bl0jj1iv0iam1s; BDRCVFR[krBU_nwdDgR]=mk3SLVN4HKm; PSINO=7; delPer=0; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; BDRCVFR[dG2JNJb_ajR]=mk3SLVN4HKm; cleanHistoryStatus=0; BDRCVFR[Txj84yDU4nc]=mk3SLVN4HKm; indexPageSugList=%5B%22%E5%81%87%E9%9D%A2%E9%AA%91%E5%A3%AB%E5%A3%81%E7%BA%B8%22%2C%22%E9%BE%99%E7%8F%A0%E8%B6%85%E5%A3%81%E7%BA%B8%22%2C%22%E8%9C%A1%E7%AC%94%E5%B0%8F%E6%96%B0%E5%81%87%E9%9D%A2%E9%AA%91%E5%A3%AB%E8%81%94%E5%8A%A8%E5%A4%B4%E5%83%8F%22%2C%22%E8%9C%A1%E7%AC%94%E5%B0%8F%E6%96%B0%E4%B8%80%E5%8F%B7%E5%A4%B4%E5%83%8F%22%2C%22%E6%A1%83%E4%B9%8B%E5%8A%A9%22%2C%22%E6%9D%B0%E5%85%8B%E9%80%8A%22%2C%22%E6%B0%B4%E6%9C%A8%E4%B8%80%E9%83%8E%22%2C%22%E7%B1%B3%E6%B4%A5%E7%8E%84%E5%B8%88%22%2C%22%E4%BD%9B%E8%8E%B1%E8%BF%AA%C2%B7%E6%91%A9%E5%85%8B%E7%91%9E%22%5D; ab_sr=1.0.1_ZmM1ZGM5Mjk1MDI2MGU2N2UxZjlkMmJjMjZhYjQzZTcxZjFlYWVmNzcwNjdlMTg2ZDgzMDIwNTUyNzg3NmMxZjFlNmM4OGNiZWJmZmM5NzUyMTk5ZjcxZGY4YzIzNGI5MWQwNTdlZmExNzgzNTI3ZTYzYjUwNzlkMzE4OGExNmI3ZDYzNjQxODMyMzZkNmYyYzY2OTRkOTIwZDBjY2RlOQ==; BDRCVFR[-pGxjrCMryR]=mk3SLVN4HKm",
        "Accept-Language": "zh-CN,zh;q=0.9",
    }

    # 创建浏览器驱动
    driver = webdriver.Chrome()

    # 访问目标网址
    driver.get(url)

    # 等待页面加载完成
    driver.implicitly_wait(10)

    # 滚动页面并加载更多图片
    for i in range(count):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(10)

    # 获取页面内容
    html_content = driver.page_source

    # 解析HTML内容
    soup = BeautifulSoup(html_content, "html.parser")

    image_links = []
    for img in soup.find_all("img", class_="main_img img-hover"):
        img_url = str(img["src"])

        if img_url.__contains__("baidu.com/it"):
            image_links.append(img_url.split("?")[0])
        else:
            image_links.append(img_url)
    print(image_links)
    # 创建保存目录
    if not os.path.exists(dirName):
        os.mkdir(dirName)

    # 下载图片
    i = 0;
    for image_link in image_links:
        # 获取图片文件名
        i += 1;
        num = i;
        if image_link.__contains__("data:image/jpeg"):
            continue
        # 下载图片并保存
        requests.packages.urllib3.disable_warnings()
        response = requests.get(image_link, verify=False, headers=headers)
        with open(os.path.join(dirName, f"{fileName}{str(num)}.jpg"), "wb") as f:
            f.write(response.content)

    print("下载完成")
    # 关闭 Selenium 浏览器驱动
    driver.quit()

# 要爬取的网页 URL
keyword = str("龙珠壁纸");
url = f"https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1710313944820_R&pv=&ic=&nc=1&z=&hd=&latest=&copyright=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&dyTabStr=&ie=utf-8&sid=&word={keyword}"
dirName = "dragon_ball_wallpapers";
getPhoto(url,dirName)
