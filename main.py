import datetime
import json
import os
import sys
import time

import execjs
import requests
from concurrent.futures import ThreadPoolExecutor


def printf(text, userId=''):
    ti = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    print(f'[{ti}][{userId}]: {text}')
    sys.stdout.flush()


def generateSignDatas(js, req):
    r = js.call("callMtgsig", req)
    signDatas.append(r)
    printf("生成了一条链接...")


def loadConpou(id):
    text = requests.get(f'https://promotion.waimai.meituan.com/lottery/limitcouponcomponent/info?couponReferIds={id}',
                        headers=headers).text
    printf(text)


def run(item):
    res = requests.post(url=item['url'], headers=item['headers'], json=item['data'], timeout=5)
    if res.status_code == 403:
        printf("忒星提醒您又403了哦！")
        return
    printf(res.text)
    log(res.text)


def start():
    for item in signDatas:
        td = pool.submit(run, item)
        threads.append(td)

def getNowTime():
    return int(round(time.time() * 1000))


def getFileContent(path):
    if os.path.exists(path) and os.path.isfile(path):
        with open(path, 'r') as f:
            content = f.read()
        return content
    else:
        raise Exception(f'无法找到文件：{path}')


def timestamp(shijian):
    s_t = time.strptime(shijian, "%Y-%m-%d %H:%M:%S")
    mkt = int(time.mktime(s_t))
    return mkt * 1000


def log(content):
    logPath = './log.txt'
    with open(logPath, 'a', encoding='utf-8') as lg:
        ti = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        lg.write(f'[{ti}]: {content}\t\n')
        lg.flush()
        lg.close()


if __name__ == '__main__':
    config = {}
    threads = []
    signDatas = []
    try:
        with open('./config.json', 'r') as c:
            rdConfigStr = c.read()
        config = json.loads(rdConfigStr)
    except Exception as e:
        printf(f'加载配置文件异常：{str(e)}')
        os.system('pause')
    Cookie = getFileContent('./ck.txt')
    js_code = open('mtgsig.js', 'r', encoding='utf-8').read()
    js = execjs.compile(js_code)
    pool = ThreadPoolExecutor(max_workers=100)
    couponReferId = config['couponReferId']
    gdPageId = config['gdPageId']
    pageId = config['pageId']
    instanceId = config['instanceId']
    maxCount = config['maxCount']
    startTimeStr = config['startTime']
    preGenerationTime = config['preGenerationTime']
    leadTime = config['leadTime']
    startTime = timestamp(startTimeStr) - leadTime

    headers = {
        "dj-token": "BUtNUwMAAABuBktNUwMaOQIAAAABO5rMWgAAACxuVckJSPql7oHvFAVd3HxCxlPut6BupLOB7KbBBmQVp4yuGJKFMxfXKIO6wCIsIjxIcQnGfaUnxZM5gtozHm5y509Oa+1qbJnAkP2KQFE9HO3fqUN9CFNvwtMAAABOr+bOPv9lUGZCdvoPdd941hT4SFb/WJNmWXHkZMN/wn1vbBD21/Vz/rsz3oVhVqdw8ctKDejgNo+TMIaNeolkXsFWTGZ9TV2P3hLL6hK+",
        "User-Agent": "Mozilla/5.0 (Linux; Android 11; Redmi Note 8 Pro Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.141 Mobile Safari/537.36 TitansX/12.10.3 KNB/1.2.0 android/11 mt/com.sankuai.meituan/12.10.406 App/10120/12.10.406 MeituanGroup/12.10.406",
        "Content-Type": "application/json",
        "X-Requested-With": "com.sankuai.meituan",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://market.waimai.meituan.com/",
        "Cookie": Cookie
    }
    url = f'https://promotion.waimai.meituan.com/lottery/limitcouponcomponent/fetchcoupon?couponReferId={couponReferId}&actualLng=121.49046325683594&actualLat=31.236862182617188&geoType=2&gdPageId={gdPageId}&pageId={pageId}&version=1&utmSource=appshare&utmCampaign=AgroupBgroupC0D200E0Ghomepage_search&instanceId={instanceId}&componentId={instanceId}'

    req = {
        "url": url,
        "headers": headers
    }
    printf("开始测试程序...")
    loadConpou(couponReferId)
    signDatas.append(js.call("callMtgsig", req))
    start()
    signDatas = []

    while True:
        printf(f'等待开始时间：{startTimeStr}')
        if getNowTime() >= startTime:
            printf("时间到，开始抢券...")
            break
        elif getNowTime() >= (startTime - preGenerationTime) and len(signDatas) < maxCount:
            printf("开始提前生成链接...")
            for i in range(maxCount):
                generateSignDatas(js, req)
        time.sleep(0.1)

    start()

    while True:
        maxTd = len(threads)
        disableTd = 0
        runTd = 0
        for td in threads:
            if td.running() is False:
                disableTd = disableTd + 1
            else:
                runTd = runTd + 1
        if maxTd == disableTd:
            exit()
            os.system('pause')
        time.sleep(2)
        printf(f'运行中线程数：{runTd} 待运行线程数：{disableTd} 总线程数：{maxTd}')
