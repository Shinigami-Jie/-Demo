import json
import time
import requests
import pytesseract
from PIL import Image

# 请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Referer": "https://viewer-trial.bookwalker.jp/03/19/viewer.html?cid=fae458f9-fba8-499f-b7a7-9298264943a2&cty=0&adpcnt=7qM_Nkp",
    "Connection": "close",
    "cookie":"_gid=GA1.2.379775111.1711607418; _gcl_au=1.1.1836246587.1711607419; _yjsu_yjad=1711607420.6b87e1a1-1cba-4013-9efc-86d3e56f079b; _clck=1xpxx00%7C2%7Cfkg%7C0%7C1548; _tt_enable_cookie=1; _ttp=aJRMdury4D8--ODYjLlIur6o6wU; cookie_optin=1; cookie_optin_registered=1711607420; bweternity=2f3rsvunh9ogw4g0cco0sccg4wksswwoc040kk0csog8wsog; myService=1; __lt__cid=cb190862-d676-4004-90ff-ce7dbfa2b349; _fbp=fb.1.1711607512660.237456285; __lt__cid=cb190862-d676-4004-90ff-ce7dbfa2b349; pc_detail_summary=1; _ga=GA1.2.567019305.1711607278; _clsk=1aipmuh%7C1711613302673%7C48%7C0%7Cj.clarity.ms%2Fcollect; _ga_EPKMR4CGNW=GS1.1.1711612878.2.1.1711613304.57.0.0; _ga_QM1GNDW25K=GS1.1.1711612878.2.1.1711613304.0.0.0; fromfae458f9-fba8-499f-b7a7-9298264943a2=1; pfCd=03; AWSALB=SSr+wZX/UeOw3FfJnGIvy7uysZ+UxCrCd4L4zVbwndx0uXISwNhxBt87/eBu0nZ8RU+8CCmC7ZXp3Ir1VplNIyVe/U/AQDUPuSpBTC9Z6W7t52nG5nEUC3T3bLwD; AWSALBCORS=SSr+wZX/UeOw3FfJnGIvy7uysZ+UxCrCd4L4zVbwndx0uXISwNhxBt87/eBu0nZ8RU+8CCmC7ZXp3Ir1VplNIyVe/U/AQDUPuSpBTC9Z6W7t52nG5nEUC3T3bLwD",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7",
}
baseUrl = "https://viewer-trial.bookwalker.jp/trial-page/c?cid=211e7eb5-fcda-4fc0-b129-e8e8fb011493&BID=171160741494191175089NFBR";
primayRequest = requests.get(baseUrl,headers=headers);
# 将读取到的字符串转换成dict
param = json.loads(primayRequest.text)['auth_info'];
# 拿到请求图片时需要的参数
pfCd = str(param['pfCd']);
policy = str(param['Policy']);
signature = str(param['Signature']);
key_Pair_Id = str(param['Key-Pair-Id']);
time.sleep(1)
failList = [];
imageList = [];
# 下载图片
def downloadImages(imageFile,imageSource):
    if imageSource.status_code == 200:
        with open(imageFile, "ab") as out:
            out.write(imageSource.content);
            return 200;
    elif imageSource.status_code == 403:
           failList.append(str(imageSource.url));
           return 403;
    else:
           print("下载失败");
           return 500;

# 读取图片转文字
def readImage(imageList):
    try:
        for imageUrl in imageList:
            image = Image.open(imageUrl, "r");
            text = pytesseract.image_to_string(image, lang="jpn")
            contexts = str(text).split();
            with open(imageUrl.replace("jpeg", "txt"), 'w', encoding="UTF-8") as output:
                index = 1;
                for context in contexts:
                    if index % 5 == 0:
                        output.write("\n")
                    index += 1;
                    output.write(context);
                print("写入完成!");

    except Exception as e:
        e.args;
        print("下载出错啦!");

# 根据页数决定发多少次请求
for page in range(41,52):
    imageSource = requests.get(f"https://viewer-epubs-trial.bookwalker.jp/2_normal/211e7eb5-fcda-4fc0-b129-e8e8fb011493/1/SVGA/normal_default/item/xhtml/p-002.xhtml/{page}.jpeg?pfCd={pfCd}&Policy={policy}&Signature={signature}&Key-Pair-Id={key_Pair_Id}")
    print(imageSource.status_code);
    imageFile = f"C:\\Users\\Decade\\Desktop\\僕らは『読み』を間違える1\\{page}.jpeg";
    downloadImages(imageFile,imageSource);
    imageList.append(imageFile);

# 将未下载的链接写入文件中
for url in failList:
    with open("C:\\Users\\Decade\Desktop\\僕らは『読み』を間違える1\\未下载的链接.txt","a+") as e:
        e.write(url);
        e.write("\n")
readImage(imageList);