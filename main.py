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
    r = js.call("signReq", req)
    signDatas.append(r)
    printf("生成了一条链接...")


def loadConpou(id):
    text = requests.get(f'https://promotion.waimai.meituan.com/lottery/limitcouponcomponent/info?couponReferIds={id}',
                        headers=headers).text
    printf(text)


def run(r, url, req):
    res = requests.post(url=url, headers=r['headers'], json=req['data'], timeout=5)
    if res.status_code == 403:
        printf("忒星提醒您又403了哦！")
        return
    printf(res.text)
    log(res.text)


def start(url, req):
    for item in signDatas:
        td = pool.submit(run, item, url, req)
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
    js_code = open('mt.js', 'r', encoding='utf-8').read()
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
        "dj-token": "",
        "User-Agent": "Mozilla/5.0 (Linux; Android 13; MI 6 Build/TQ2A.230405.003.E1; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/112.0.5615.136 Mobile Safari/537.36 TitansX/12.9.1 KNB/1.2.0 android/13 mt/com.sankuai.meituan/12.9.404 App/10120/12.9.404 MeituanGroup/12.9.404",
        "Content-Type": "application/json",
        "X-Requested-With": "com.sankuai.meituan",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://market.waimai.meituan.com/",
        "Cookie": Cookie
    }
    url = f'https://promotion.waimai.meituan.com/lottery/limitcouponcomponent/fetchcoupon?couponReferId={couponReferId}&actualLng=121.49046325683594&actualLat=31.236862182617188&geoType=2&gdPageId={gdPageId}&pageId={pageId}&version=1&utmSource=appshare&utmCampaign=AgroupBgroupC0D200E0Ghomepage_search&instanceId={instanceId}&componentId={instanceId}'
    data = {"cType": "wm_wxapp", "fpPlatform": 13, "wxOpenId": "oOpUI0VNQW9NfuHdL3Yd8OrJNH4s", "appVersion": "",
            "mtFingerprint": "H5dfp_1.8.2_tttt_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"}
    req = {
        "url": url,
        "method": "POST",
        "headers": headers,
        'data': data
    }
    printf("开始测试程序...")
    loadConpou(couponReferId)
    signDatas.append(js.call("signReq", req))
    start(url, req)
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

    start(url, req)

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
