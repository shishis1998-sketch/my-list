# 📚 媒体清单 App 维护手册

> 个人媒体追踪 App「media-tracker」长期维护指南
>
> 🌐 **网址**：https://shishis1998-sketch.github.io/my-list/
> 📂 **仓库**：https://github.com/shishis1998-sketch/my-list

---

## 🗂️ 这个 App 是怎么搭起来的

```
┌─────────────────────────────────────────────────┐
│  手机/电脑浏览器                                  │
│  ┌──────────────────────────────────────────┐  │
│  │  打开网址 → 加载 index.html                │  │
│  │  网页运行 → 数据存浏览器 localStorage      │  │
│  │  改动后 → 1.5 秒自动推送到 GitHub Gist     │  │
│  └──────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
              ↓                    ↑
         (访问)                  (云同步)
              ↓                    ↑
┌──────────────────────┐  ┌──────────────────────┐
│  GitHub Pages        │  │  私密 GitHub Gist    │
│  托管 index.html     │  │  存数据 JSON 文件    │
│  永久免费、无广告    │  │  永久免费、私密      │
└──────────────────────┘  └──────────────────────┘
```

**三件东西彼此独立：**

| 类别 | 存哪 | 备份方式 |
|---|---|---|
| **代码** index.html | GitHub 仓库 | GitHub 自动有版本历史 |
| **数据** JSON | 私密 Gist | 手动「导出 JSON」+ 本地存档 |
| **配置** Token + Gist ID | 浏览器 localStorage | 重新输入即可 |

任何一个出问题，**另外两个不受影响**。

---

## 📅 维护节奏

### 🟢 每月做一次（5 分钟）— 导出 JSON 备份

1. 打开网站
2. 点「导出 JSON」→ 下载
3. 重命名为 `media-tracker-备份-2026-05.json`
4. 存到**至少两个**位置：
   - ☁️ iCloud / Google Drive
   - 📱 手机文件 App
   - 📧 邮件发给自己
   - 💻 电脑硬盘

> 💡 **为什么要这么做**：万一 Gist 出问题（极小概率），或误删大量数据，本地备份能 100% 救回来。

### 🟡 每 3-6 个月（10 分钟）— 检查 Token

1. 在网站随便编辑一条记录
2. 看右上角同步状态：
   - ✅ 绿色 / 已同步 → 一切正常
   - ❌ 红色 / 错误 → 参考「Token 失效怎么办」

### 🔵 每年（5 分钟）— 检查 GitHub 通知邮件

如果 Token 有问题，GitHub 会发邮件。一年没收到任何邮件 = 100% 没事。

---

## 🆘 出问题怎么查

### 问题 1：「打开网址，页面空白 / 报错」

依次尝试：
1. 等 1-2 分钟再试（GitHub 偶尔抽风）
2. 手机长按刷新按钮 → 强制刷新
3. 试试用电脑能不能打开
4. 还不行 → 访问 https://www.githubstatus.com 看服务状态

### 问题 2：「页面打开了，但数据没了」

> ⚠️ **别慌，数据没真的丢。**

排查顺序：
1. **先检查配置**：进设置（左侧菜单），看 Token 和 Gist ID 是否还在
2. **如果 Token 在但数据不显示**：可能是 Gist ID 错了。去 https://gist.github.com 找到 `media-tracker-data.json` Gist，从 URL 复制 ID 重填
3. **如果 Token 不在**：浏览器缓存被清了。重新填 Token 和 Gist ID，数据自动从云端拉回
4. **如果还是没数据**：用最近 JSON 备份恢复（导入 JSON 功能）

### 问题 3：「同步状态显示红色 / 错误」

最常见原因：**Token 失效**（见下方）。

其他可能：
- 网络问题 → 换 WiFi
- GitHub 服务异常 → 等等
- 仓库变私密 → 检查 https://github.com/shishis1998-sketch/my-list 是否还是 Public

### 问题 4：「Token 失效怎么办」

虽然选了「永不过期」，但以下情况 Token 会失效：
- GitHub 检测到 Token 被泄漏
- 你主动撤销了
- 账号安全策略变化（罕见）

**重新生成步骤：**

1. 登录 GitHub → 右上角头像 → **Settings**
2. 左侧最底 → **Developer settings**
3. **Personal access tokens** → **Tokens (classic)**
4. **Generate new token (classic)**
5. 设置：
   - Note：随便填，比如 `media-tracker`
   - Expiration：**No expiration**
   - 勾选权限：**只勾 `gist`**（别多勾！）
6. 生成后 **立刻复制**（关掉就再也看不到了）
7. 打开网站 → 设置 → 粘贴新 Token → 保存

### 问题 5：「想在新设备上用」

换手机或电脑：
1. 新设备打开 https://shishis1998-sketch.github.io/my-list/
2. 进入设置
3. 填入**相同的 Token 和 Gist ID**
4. 数据自动从云端拉取

> ✅ 不需要重新搞 Token。同一个 Token 多设备共用。

### 问题 6：「网页突然变丑 / 某些功能不工作」

很可能是浏览器和 CSS 兼容问题：
1. **强制刷新**（iPhone 长按刷新按钮 / 电脑 Ctrl+Shift+R / Mac Cmd+Shift+R）
2. 试试**电脑或别人手机**打开，看是不是只在你设备上有问题
3. 截图描述问题，找 AI 助手帮改 CSS

---

## 🔐 安全注意事项

### Token 不能泄漏

Token = 密码。拿到 Token 的人可以：
- 看你**所有**私密 Gist
- 修改 / 删除 Gist

**预防：**
- ❌ 不在公共电脑登录
- ❌ 不发给陌生人
- ❌ 不贴朋友圈/微博等公开地方
- ✅ 万一泄漏 → 立刻去 GitHub 撤销旧 Token + 生成新的

### 仓库为什么要 Public？

GitHub Pages 免费版**只支持公开仓库**。
但**公开的是代码（index.html），不是数据**。数据在私密 Gist 里，别人看不到。

---

## 💰 费用说明

**全部免费，没有任何隐性收费。**

| 服务 | 费用 | 限制 |
|---|---|---|
| GitHub 账号 | 免费 | 无限私密 Gist |
| GitHub Pages | 免费 | 100GB/月流量（永远用不完）|
| Personal Access Token | 免费 | 无 |

**唯一成本**：每年 30 分钟维护时间。

---

## 🛠️ 想改 App 怎么办

### 小改动（CSS、文字、布局）
1. **先「导出 JSON」备份**
2. GitHub 仓库 → `index.html` → 铅笔图标 ✏️ → 直接改
3. 改完 Commit
4. 等 30 秒-2 分钟，强制刷新

### 大改动（加功能、改逻辑）
找 AI 助手（Claude / ChatGPT）：
- 告诉它想加什么功能
- 把当前 index.html 发给它
- 让它给你完整改后的新文件 + 改动清单

### 改坏了怎么办
1. GitHub 仓库 → 点 **Commits**（Code 标签页顶部）
2. 找到上一个能用的 commit
3. 点 **⋯ → Revert** → 回退

---

## 🎯 长期使用预期

按现在这套搭建方式：

| 时间 | 预期 |
|---|---|
| **5 年内** | ✅ 99% 概率毫无问题 |
| **10 年内** | ⚠️ 可能小修小补（CSS 适配、API 微调）|
| **20 年后** | 🤔 不好说，但**数据 JSON 文件永远能读**（纯文本格式）|

**兜底方案**：哪天 GitHub 真不行了，只要有 JSON 文件，找懂技术的人一小时内能迁移到其他平台。

---

## 📞 常用链接

| 用途 | 链接 |
|---|---|
| 🌐 **网站** | https://shishis1998-sketch.github.io/my-list/ |
| 📂 **代码仓库** | https://github.com/shishis1998-sketch/my-list |
| 💾 **数据 Gist** | https://gist.github.com |
| 🔑 **Token 管理** | https://github.com/settings/tokens |
| 📊 **GitHub 状态** | https://www.githubstatus.com |

---

## ✍️ 备份记录

> 💡 每次手动备份后,在这里记一笔

| 日期 | 备份文件名 | 存放位置 |
|---|---|---|
| 2026-05 | media-tracker-备份-2026-05.json | _填位置_ |
|  |  |  |
|  |  |  |
|  |  |  |

---

*手册最后更新:2026 年 5 月*

*建议设置手机日历每月 1 号提醒「导出 media-tracker 备份」*
