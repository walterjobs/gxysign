import os
import json
import requests
from datetime import datetime
# from serverchan_sdk import sc_send

# ====== 从环境变量读取（GitHub Secrets）======
auth = os.environ["MOGUDING_AUTH"]
send_key = os.environ["BARK_KEY"]
planid = os.environ["PLANID"]

list_url = "https://api.moguding.net:9000/attendence/clock/v2/listByApp"
sign_url = "https://api.moguding.net:9000/msg/notice/v1/batchSignMessage"


headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
                  "(KHTML, like Gecko) Version/18.5 Safari/605.1.15 Edg/141.0.0.0 ",
    "Accept": "application/json",
    "authorization": auth,
}

# ====== 1. 获取未签到列表 ======
param1 = {
    "planId": planid,
    "state": 0,
    "type": 1,
}

unsign = requests.post(list_url, headers=headers, json=param1).text
list_json = json.loads(unsign)

user_id_list = [
    item.get("userId")
    for item in list_json.get("data", [])
    if item.get("userId") is not None
]
stu_name_list = [
    item.get("stuName")
    for item in list_json.get("data", [])
    if item.get("stuName")
]

desp = "\n".join(stu_name_list) + "\n未签到" if stu_name_list else "全部已签到 ✅"
print (desp)
bark_url = f"https://api.day.app/{send_key}/{desp}"

# ====== 2. 签到（无论何时都执行） ======
if stu_name_list
    for user_id in user_id_list:
        param2 = {"type": 1, "tolds": user_id}
        toldsign = requests.post(sign_url, headers=headers, json=param2)
        print(toldsign.text)
    else
    print(全部已签到,无需推送)

# ====== 3. 推送：只在 22:00 - 22:15（北京时间）之间执行 ======
# GitHub Actions 用 UTC，+8 小时得到北京时间
now = datetime.utcnow()
bj_now = now.hour + 8  # 简单处理，日期跨天可忽略

# 更稳妥的写法：
from datetime import timedelta, timezone
bj_time = datetime.now(timezone.utc) + timedelta(hours=8)
start = bj_time.replace(hour=20, minute=30, second=0, microsecond=0)
end   = bj_time.replace(hour=23, minute=30, second=0, microsecond=0)

if start <= bj_time <= end:
    response = requests.post(bark_url, timeout=10)
    print("已推送：\n", desp)
else:
    print(f"当前北京时间 {bj_time.strftime('%H:%M:%S')} 不在 22:00-22:15 范围内，跳过推送。")
