
作为实习指导老师，每天上工学云查看学生签到情况，是一件重复性很高、很枯燥的工作。
本项目自动调用工学云接口：
*  获取学生签到情况
*  批量通知未签到学生
*  通过 [Bark](https://github.com/Finb/Bark) 推送到 iPhone。
配合 **GitHub Actions** 定时执行，无需服务器，白嫖到底。

## 🚀 快速开始

### 1. Fork / Clone 本仓库

### 2. 配置 GitHub Secrets

进入仓库 **Settings → Secrets and variables → Actions → New repository secret**，依次添加：

| Secret 名称 | 必填 | 说明 |
|---|---|---|
| `MOGUDING_AUTH` | ✅ | 请求头里的 `authorization` 值 |
| `PLANID` | ✅ | 请求头里的实习计划 PLANID |
| `BARK_KEY` | ✅ | Bark App 里的推送 Key |

#### 如何获取 `MOGUDING_AUTH`、`PLANID`

1. 手机或电脑登录工学云，抓包进入 `https://api.moguding.net:9000/attendence/clock/v2/listByApp` 
2. 复制请求头里的 `authorization` 字段值（一长串 token）
3. 复制请求头里的 `planId` 字段值


#### 如何获取 `BARK_KEY`（当然也可以利用server酱进行微信推送，见项目OLD分支）

1. App Store 安装 [Bark](https://apps.apple.com/app/bark-customed-notifications/id1403753865)
2. 打开 App，首页那串 `https://api.day.app/xxxxxxxx` 里的 `xxxxxxxx` 就是 Key

