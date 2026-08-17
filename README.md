# 神秘复苏 · 驭鬼者（手机游戏版）

基于《神秘复苏》小说世界观的灵异生存游戏，使用 **Python + Kivy** 开发，可打包为 Android APK。

## 特点

- 📱 **真正的手机APP**：不是网页，是原生Android应用
- 🌐 **在线/离线双模式**：联网时调用大模型API生成剧情，断网自动切换本地数据库
- 👻 **驾驭厉鬼**：28只厉鬼可收集，鬼域压制+规律破解+关押驾驭战斗系统
- ✦ **成神路线**：黄岗村隐藏鬼差路线，吞噬成长，黄金门登神结局
- 💾 **本地存档**：自动保存进度

## 项目结构

```
mystery-revival-app/
├── main.py           # 主程序（Kivy UI + 游戏逻辑）
├── game_data.py      # 游戏数据（厉鬼/物品/地点/离线事件）
├── game_state.py     # 状态管理 + 存档
├── api_client.py     # API客户端（在线调用大模型）
├── buildozer.spec    # Android打包配置
├── requirements.txt  # Python依赖
└── README.md         # 本文件
```

---

## 一、电脑上测试运行

### 1. 安装依赖
```bash
pip install kivy
```

### 2. 运行
```bash
python main.py
```

### 3. 配置API地址
在游戏内「设置」中修改后端API地址，或设置环境变量：
```bash
# Linux/Mac
export MR_API_URL=https://你的后端地址/api
# Windows
set MR_API_URL=https://你的后端地址/api
```

---

## 二、打包成 Android APK

### 方法一：Buildozer（推荐，Linux环境）

#### 1. 安装Buildozer和依赖
```bash
pip install buildozer
# Ubuntu/Debian需要安装的系统依赖
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
```

#### 2. 准备图标和启动图
- 准备 `icon.png`（1024x1024）和 `presplash.png`（启动图）放到项目目录
- 没有也可以，用默认的

#### 3. 打包
```bash
cd mystery-revival-app
buildozer android debug
```
第一次打包会自动下载Android SDK/NDK，需要30分钟-1小时。

打包完成后，APK在 `bin/` 目录下：
```
bin/mysteryrevival-1.0.0-arm64-v8a-debug.apk
```

#### 4. 安装到手机
```bash
# 手机开启USB调试后
adb install bin/mysteryrevival-1.0.0-arm64-v8a-debug.apk
```
或者把APK文件传到手机直接安装。

### 方法二：在线打包（不用配环境）

使用 [Google Colab](https://colab.research.google.com/) 或 GitHub Actions 在线构建，搜索"buildozer colab"有现成模板。

---

## 三、后端部署（关键：不用同一网络也能连API）

手机APP要在任何网络下都能调用你的大模型API，需要把后端部署到**公网**。有三种方案：

### 方案A：内网穿透（最简单，不用买服务器）

在你电脑上运行后端，用内网穿透工具暴露到公网。

#### 使用 cpolar（国内推荐，免费）
1. 下载 https://www.cpolar.com/
2. 注册登录，启动后端：
   ```bash
   cd mystery-revival-api
   node server.js
   ```
3. 新开终端，穿透3000端口：
   ```bash
   cpolar http 3000
   ```
4. 会得到一个公网地址，如 `https://abc123.cpolar.cn`
5. 手机APP设置里填：`https://abc123.cpolar.cn/api`

#### 使用 ngrok（国际推荐）
```bash
ngrok http 3000
```
得到 `https://xxx.ngrok-free.app`

> 免费版地址会变，每次重启需要重新设置。付费版有固定地址。

### 方案B：云服务器（最稳定）

1. 买一台云服务器（阿里云/腾讯云，最便宜的约30元/月）
2. 把 `mystery-revival-api` 上传到服务器
3. 安装Node.js，运行：
   ```bash
   npm install
   node server.js
   ```
4. 用 PM2 后台运行：
   ```bash
   npm install -g pm2
   pm2 start server.js --name mystery-api
   pm2 startup
   ```
5. 服务器安全组放行3000端口
6. 绑定域名（可选），API地址为 `http://你的服务器IP:3000/api`

### 方案C：免费托管（零成本）

使用 [Render](https://render.com) 或 [Railway](https://railway.app) 免费托管Node.js后端：
1. 把后端项目上传到GitHub
2. 在Render新建Web Service，连接GitHub仓库
3. 设置环境变量（API_KEY、MODEL等）
4. 部署完成后得到 `https://xxx.onrender.com` 公网地址

---

## 四、游戏玩法

### 核心数值
- **生命**：受到灵异攻击扣，归零死亡
- **理智**：接触灵异掉，归零崩溃
- **复苏**：使用厉鬼力量涨，满100%被吞噬
- **洞察**：用于破解厉鬼杀人规律

### 战斗流程
1. 开启鬼域压制对方鬼域层级
2. 消耗洞察破解杀人规律
3. 用棺材钉或能力完全限制
4. 尝试关押驾驭（成功获得新鬼，失败被反噬）

### 成神路线（隐藏）
1. 洞察≥50 + 驾驭≥2鬼 → 去黄岗村探索触发鬼差
2. 用人皮纸交易或拼死一战 → 驾驭鬼差
3. 战斗中选择「吞噬」败鬼，累积压制数
4. 压制数≥10解锁「重启」能力
5. 压制数≥20 + 驾驭≥8鬼 + 鬼域≥8层 + 神位碎片 → 黄金门登神

---

## 五、常见问题

**Q: 打包报错怎么办？**
A: 第一次打包最容易出问题的是SDK/NDK下载，建议用代理或手动下载放到 `~/.buildozer/android/platform/` 目录。

**Q: 手机安装提示风险？**
A: 因为是debug签名的APK，选择"继续安装"即可。发布版需要正式签名。

**Q: 离线模式能玩完整内容吗？**
A: 可以。离线模式有11个地点、每个地点3-4个专属事件、28只厉鬼、完整战斗和成神系统。在线模式只是剧情更丰富多变。

**Q: 怎么改默认API地址？**
A: 设置环境变量 `MR_API_URL`，或在游戏内设置页修改，修改后自动保存。
