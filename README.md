# MeiTuanAutoCoupon
# 美团网页抢券通用脚本 自带1.0mtgsig（原创脚本，仅供学习交流使用，关注忒星不迷路）

# 说明
1.脚本适用范围（几乎所有美团外卖网页券活动，如母亲节鲜花100无门槛、品质百货30无门槛、直播间120蛋糕券等...）

2.后续美团相关活动

# 运行环境要求
1.NodeJs （https://nodejs.org/en）

2.Python （https://www.python.org/）

# Python模块安装（cmd 执行）
```text
pip install requests

pip install pyexecjs
```

# 配置说明
```text
{
  //优惠券id 从美团活动页面获得
  "couponReferId": "D65881E6226B417E9E909111DA2DD791",
  //活动页面id 从美团活动页面获得
  "gdPageId": "495093",
  //活动页面id 从美团活动页面获得
  "pageId": "497076",
  //优惠券模块id 从美团活动页面获得
  "instanceId": "16843237183550.7887493532593517",
  //抢券次数 根据自己电脑 网络等因素手动调整
  "maxCount": 30,
  //抢券开始时间
  "startTime": "2023-05-20 14:00:00",
  //提前多长时间开始生成抢券链接 单位毫秒 40000 = 提前40秒生成
  "preGenerationTime": 40000,
  //提前多长时间抢券 单位毫秒 当前配置理论开始时间为2023-05-20 13:59:59.800
  实际会晚于这个时间一点点 根据自己电脑 网络等因素手动调整
  "leadTime": 200
}
```

# 账号配置 （ck.txt 只支持单账号 多开请创建多个文件夹）
```text
token=AgGyIxOjMm5s6WdPofAbSVMzE0z-156c31kkSj-uMvon2C4jkbMPb4gAAAABaFQAAka4zYxgp9tf3_Hgw5O5p3;
```

# 启动 (在cmd中执行命令)
```text
python main.py
```

# 交流群：（已满200人 群主wx：g4994g 加我拉你进群）
![image](https://user-images.githubusercontent.com/49848349/206616062-426f6747-58da-43da-82a3-e676fbf6f436.png)