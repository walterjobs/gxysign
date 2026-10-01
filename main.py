import os
import json
import requests
from datetime import datetime, timedelta, timezone

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

resp = requests.post(list_url, headers=headers, json=param1)
unsign = resp.text
print("原始响应:", unsign)  # 便于排查

try:
    list_json = json.loads(unsign)
except json.JSONDecodeError:
    list_json = {}

# ====== 判断 cookie 是否过期 ======
# 常见判定条件：
#   1. HTTP 状态码为 401 / 403
#   2. 返回的 code 不是 200（或不是成功码）
#   3. data 为 None（而非空列表）
#   4. msg 中包含"过期""无效""未登录""token"等关键字
data = list_json.get("data")
code = list_json.get("code")
msg = str(list_json.get("msg", ""))

cookie_expired = (
    resp.status_code in (401, 403)
    or (code is not None and code != 200)
    or data is None
    or any(k in msg for k in ("过期", "失效", "无效", "未登录", "token", "登录"))
)

if cookie_expired:
    desp = "工学云cookie 过期"
    print(desp)
    # 立即推送 cookie 过期通知
    bark_url = f"https://api.day.app/{send_key}/{desp}"
    try:
        requests.post(bark_url, timeout=10)
        print("已推送：", desp)
    except Exception as e:
        print("推送失败：", e)
    # 直接结束，避免后续无意义调用
    raise SystemExit(0)

# ====== cookie 正常，继续处理未签到列表 ======
stu_name_list = [
    item.get("stuName")
    for item in data
    if item.get("stuName")
]
user_id_list = [
    item.get("userId")
    for item in data
    if item.get("userId") is not None
]

desp = "\n".join(stu_name_list) + "\n未签到" if stu_name_list else "全部已签到 ✅"
print(desp)
bark_url = f"https://api.day.app/{send_key}/{desp}"

# ====== 2. 签到 ======
if stu_name_list:
    for user_id in user_id_list:
        param2 = {"type": 1, "tolds": user_id}
        toldsign = requests.post(sign_url, headers=headers, json=param2)
        print(toldsign.text)
else:
    print("无需提醒打卡")

# ====== 3. 推送：只在 20:30 - 23:30（北京时间）之间执行 ======
bj_time = datetime.now(timezone.utc) + timedelta(hours=8)
start = bj_time.replace(hour=20, minute=30, second=0, microsecond=0)
end   = bj_time.replace(hour=23, minute=30, second=0, microsecond=0)

if start <= bj_time <= end:
    response = requests.post(bark_url, timeout=10)
    print("已推送：\n", desp)
else:
    print(f"当前北京时间 {bj_time.strftime('%H:%M:%S')} 不在 20:30-23:30 范围内，跳过推送。")
