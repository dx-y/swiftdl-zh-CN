# -*- coding: utf-8 -*-
# 简体中文汉化映射执行器（幂等，可重复运行）
# 用法: python tools/apply-zh.py [app/ui 目录]
#   - 不带参数时默认处理本仓库的 app/ui
#   - 只替换 MAP 中登记过的英文原串，命不中的保持原样，不影响编译
#   - 上游改版后，把新增英文补进下面的 MAP 再重跑即可
#   - 随后必须 npm run build 与 cargo build --release --features custom-protocol
"""SwiftDL UI 中文化：文本节点 / 属性 / JS 字面量 白名单精确替换。"""
import re, sys, os, json

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "app", "ui")

MAP = {
# ---------- 0.5.0 / 0.5.1 new UI ----------
"Start with the computer": "开机启动",
"Open quietly in the tray at sign-in, so the browser extension always has SwiftDL to send downloads to": "登录时在托盘中静默启动，让浏览器扩展始终有 SwiftDL 可以接收下载任务",
# 扩展（extension/，需以该目录为 ROOT 运行）
"Can't reach SwiftDL": "无法连接 SwiftDL",
"Connect through a port instead": "改为通过端口连接",
"In SwiftDL, open Settings, switch on Remote control and copy the secret. SwiftDL must be running.": "在 SwiftDL 的“设置 > 本地 API”中开启“兼容 aria2 的 API”，并复制其中的密钥。SwiftDL 需保持运行。",
"Port (6800)": "端口（6800）",
"Save and test": "保存并测试",
"Download SwiftDL": "下载 SwiftDL",
# ---------- 0.4.2 / 0.4.3 new UI ----------
# 只放完整独立字符串；带 ${...} 的模板串在源码里手工处理。
"Playlist": "播放列表",
"Close (Esc)": "关闭（Esc）",
"Video, up to 1080p": "视频，最高 1080p",
"Video, best available": "视频，最佳画质",
"Audio only": "仅音频",
"Select none": "全不选",
"Select all": "全选",
"Reading the playlist…": "正在读取播放列表…",
"Couldn't read that playlist: ": "无法读取该播放列表：",
"Open the app once. If it's already open, restart the browser.": "请先打开一次 SwiftDL。若已在运行，请重启浏览器。",
"Mirrors": "镜像地址",
"Video links": "视频链接",
# ---------- index.html ----------
"A folder picker opens": "会打开文件夹选择器",
"About": "关于",
"Add the browser extension": "添加浏览器扩展",
"After a torrent finishes": "种子下载完成后",
"All downloads": "全部下载",
"Allow other devices on my network": "允许局域网内其他设备访问",
"Also delete the file from disk": "同时从磁盘删除文件",
"Any": "任意",
"Ask where to save each file before downloading": "每次下载前询问保存位置",
"Automation": "自动化",
"Browser": "浏览器",
"Browser extension": "浏览器扩展",
"Browser still asks where to save? Turn off": "浏览器仍提示保存位置？请关闭",
"Cancel": "取消",
"Change…": "更改…",
"Choose SwiftDL's extension folder": "选择 SwiftDL 的扩展文件夹",
"Clear": "清空",
"Click Load unpacked": "点击“加载已解压的扩展程序”",
"Close": "关闭",
"Closing the window keeps downloads and browser integration going": "关闭窗口后下载与浏览器接管仍会继续",
"Confirm browser downloads": "接管浏览器下载前先确认",
"Connections per download": "每个下载的连接数",
"Copy path": "复制路径",
"Custom": "自定义",
"Dark": "深色",
"Debrid API token": "Debrid API 令牌",
"Debrid service": "Debrid 服务",
"Debug log": "调试日志",
"Done": "完成",
"Download": "下载",
"Download folder": "下载目录",
"Download later": "稍后下载",
"Downloads wait until this time, once": "下载任务将等到该时间，仅一次",
"Drop to download": "松开即下载",
"Fast, resumable downloads with many connections at once.": "多连接并行、支持断点续传的快速下载。",
"File name": "文件名",
"Find files on a page": "在页面中查找文件",
"Firefox Add-ons": "Firefox 扩展商店",
"Firefox:": "Firefox：",
"Free and open source.": "免费开源。",
"From the service's account page: real-debrid.com/apitoken, alldebrid.com/apikeys or premiumize.me/account.": "见服务商账户页：real-debrid.com/apitoken、alldebrid.com/apikeys 或 premiumize.me/account。",
"General": "常规",
"Get the browser extension": "获取浏览器扩展",
"Happens once, then goes back to doing nothing": "仅执行一次，之后恢复为不操作",
"Idle": "空闲",
"Interface size": "界面缩放",
"Keep running in the tray": "关闭窗口后仍在托盘运行",
"Keep sharing": "继续做种",
"Lets tools like AriaNg and scripts control SwiftDL. Local only, and every call needs the secret. Restart SwiftDL to apply.": "允许 AriaNg 等工具和脚本控制 SwiftDL。仅限本机，每次调用都需要密钥。重启 SwiftDL 后生效。",
"Light": "浅色",
"Like http://127.0.0.1:8080 or socks5://127.0.0.1:1080. Empty follows your system. Restart SwiftDL to apply.": "例如 http://127.0.0.1:8080 或 socks5://127.0.0.1:1080。留空则跟随系统。重启 SwiftDL 后生效。",
"Links from file-hosting sites the service supports download through your account there.": "该服务支持的网盘链接将通过你的账号下载。",
"List the files a web page links to": "列出网页中链接的文件",
"Local API": "本地 API",
"Made when you turn it on": "开启时自动生成",
"Makes everything in the main window larger or smaller": "调整主窗口内容整体大小",
"Maximize": "最大化",
"Minimize": "最小化",
"More connections are faster on servers that limit each one": "对限制单连接速度的服务器，连接越多越快",
"Network": "网络",
"Network address": "网络出口地址",
"New download": "新建下载",
"No downloads yet": "暂无下载",
"Not used": "未使用",
"Nothing": "无",
"Notifications": "通知",
"Notify me when a download finishes": "下载完成后通知我",
"Offer the extension automatically": "自动推荐安装扩展",
"Open extension folder": "打开扩展文件夹",
"Open http://127.0.0.1:6800 for the web remote": "用 http://127.0.0.1:6800 打开网页远程控制",
"Open log": "打开日志",
"Open the extensions page": "打开扩展管理页",
"Others wait in the queue": "其余任务排队等待",
"Paste a link, drop one onto this window, or start a download in your browser.": "粘贴链接、拖到本窗口，或在浏览器中发起下载。",
"Paste a link…": "粘贴链接…",
"Paste a page address…": "粘贴页面地址…",
"Paste from clipboard": "从剪贴板粘贴",
"Pause all": "全部暂停",
"Port": "端口",
"Progress, connections and a \"Download complete\" summary": "实时进度、各连接状态与“下载完成”汇总",
"Proxy": "代理",
"Quit SwiftDL": "退出 SwiftDL",
"Remove": "移除",
"Remove download?": "移除下载？",
"Resume all": "全部继续",
"Save": "保存",
"Save videos, music, programs and archives into their own folders": "按视频、音乐、程序、压缩包等类型分别保存到子文件夹",
"Search": "搜索",
"Search downloads or type a command…": "搜索下载或输入命令…",
"Secret": "密钥",
"Seeing two download windows?": "出现两个下载窗口？",
"Select all": "全选",
"Send downloads out only from this address, such as your VPN's. If it goes away, downloads stop instead of using another route. Restart SwiftDL to apply.": "只从该地址（例如 VPN 网卡）发出下载。该地址消失时下载会停止，而不会改走其他线路。重启 SwiftDL 后生效。",
"Settings": "设置",
"Shared across all downloads": "所有下载共享",
"Sharing it back helps others download it. The download is ready either way.": "回传做种可帮助他人下载。无论是否做种，文件都已下载完成。",
"Show New download before a download from the browser starts": "浏览器发起下载时先显示“新建下载”窗口",
"Show a window for each download": "每个下载显示独立窗口",
"Shut down": "关机",
"Simultaneous downloads": "同时下载数",
"Sleep": "睡眠",
"Sort by file type": "按文件类型分类",
"Speed": "速度",
"Speed limit": "速度限制",
"Start the queue at": "队列开始时间",
"Stop sharing": "停止做种",
"Supported browsers ask once, the next time they start": "支持的浏览器会在下次启动时询问一次",
"SwiftDL will fetch the file's details first": "SwiftDL 会先获取文件信息",
"System": "跟随系统",
"System follows your computer's light or dark setting": "跟随系统的浅色/深色设置",
"The extension sends browser downloads to SwiftDL, with your cookies so downloads behind a login work, and adds a download button to videos.": "扩展会把浏览器下载交给 SwiftDL，并携带 Cookie 以支持登录后的下载，还会在视频上添加下载按钮。",
"The path is already copied, so paste it into the picker": "路径已复制，直接粘贴到选择框即可",
"The switch is in the top-right corner of that page": "开关在该页面右上角",
"Theme": "主题",
"Turn off “Ask where to save each file before downloading” in your browser's download settings. The browser asks before SwiftDL can take over.": "在浏览器下载设置中关闭“下载前询问每个文件的保存位置”。否则浏览器会先询问，SwiftDL 无法接管。",
"Turn on Developer mode": "打开“开发者模式”",
"Type": "类型",
"Unpack archives": "自动解压压缩包",
"Until ratio 1": "做种到比率 1",
"Until ratio 2": "做种到比率 2",
"Use this folder rather than a downloaded copy: it stays in place while SwiftDL is installed and is refreshed when SwiftDL updates.": "请使用此文件夹而非另存的副本：只要 SwiftDL 已安装，它就会一直存在，并在 SwiftDL 更新时刷新。",
"Used as token:SECRET in each call": "每次调用以 token:SECRET 形式使用",
"Waiting for the extension to connect…": "正在等待扩展连接…",
"Watch the clipboard": "监听剪贴板",
"What SwiftDL did and any errors. Attach it when you report a bug.": "记录 SwiftDL 的操作与错误。反馈问题时请附上。",
"When a .zip, .tar.gz or .7z finishes, unpack it into a folder beside it": ".zip、.tar.gz 或 .7z 下载完成后解压到同目录文件夹",
"When all downloads finish": "全部下载完成后",
"When you switch to SwiftDL after copying a download link, offer to download it": "复制下载链接后切换到 SwiftDL 时，提示是否下载",
"aria2-compatible API": "兼容 aria2 的 API",
"get it from": "获取地址：",
"in its download settings, so only SwiftDL asks.": "在其下载设置中，让只有 SwiftDL 询问。",
"in the address bar": "在地址栏中",
# ---------- download.html ----------
# ---------- src/main.ts ----------
"Actions": "操作",
"Cancel download": "取消下载",
"Cancel download…": "取消下载…",
"Cancel this download?": "取消此下载？",
"Click Add next to a browser below": "点击下方浏览器旁的“添加”",
"Completed": "已完成",
"Connections": "连接数",
"Copy link": "复制链接",
"Copy the new link first, then choose this again": "请先复制新链接，再重新选择此项",
"Custom…": "自定义…",
"Delete": "删除",
"Dismiss": "忽略",
"Download cancelled": "下载已取消",
"Download in browser": "用浏览器下载",
"Download next": "下一个下载",
"Downloaded": "已下载",
"Downloading": "下载中",
"Downloading the update…": "正在下载更新…",
"Downloads": "下载",
"Downloads in this view will show up here.": "该视图中的下载会显示在这里。",
"Failed": "失败",
"File": "文件",
"Finished": "已完成",
"Finishing…": "正在收尾…",
"Get it": "获取",
"In progress": "进行中",
"Install and restart": "安装并重启",
"Installed": "已安装",
"Installed · asks to enable the extension on next start": "已安装 · 下次启动时会提示启用扩展",
"It's not waiting in the queue": "它不在等待队列中",
"Link copied": "链接已复制",
"Link replaced, resuming": "链接已替换，继续下载",
"More": "更多",
"Navigation": "导航",
"No limit": "不限速",
"No link on the clipboard": "剪贴板中没有链接",
"No links found in what you pasted": "粘贴内容中未找到链接",
"No links found on this page": "此页面未找到链接",
"No results": "无匹配结果",
"No, the server doesn't support it": "否，服务器不支持",
"Not installed": "未安装",
"Nothing here": "这里还没有内容",
"Open": "打开",
"Open settings": "打开设置",
"Open the link in your browser, which downloads it with your own session": "在浏览器中打开该链接，用你自己的登录会话下载",
"Opened Firefox Add-ons. Click “Add to Firefox” there.": "已打开 Firefox 扩展商店，请在那里点击“添加到 Firefox”。",
"Opened the extension page. Click “Add to browser” there.": "已打开扩展页面，请在那里点击“添加到浏览器”。",
"Path copied": "路径已复制",
"Pause": "暂停",
"Pause all downloads": "暂停全部下载",
"Paused": "已暂停",
"Queued": "排队中",
"Reading the page…": "正在读取页面…",
"Remove from list?": "从列表中移除？",
"Remove speed limit": "取消限速",
"Removed from list": "已从列表移除",
"Remove…": "移除…",
"Replace link from clipboard": "用剪贴板链接替换",
"Resume": "继续",
"Resume all downloads": "继续全部下载",
"Retry": "重试",
"Select none": "全不选",
"Set up browser extension": "设置浏览器扩展",
"Settings saved": "设置已保存",
"Show in folder": "在文件夹中显示",
"Size": "大小",
"Speed limit removed": "已取消限速",
"Start at 02:00": "02:00 开始",
"SwiftDL checks the file's name and size before downloading.": "SwiftDL 会在下载前检查文件名和大小。",
"Time left": "剩余时间",
"Unknown size": "大小未知",
"Waiting for the extension to connect… ": "正在等待扩展连接…",
"Will download next": "将作为下一个下载",
"Yes": "是",
"You have ": "当前版本 ",
"your browser": "你的浏览器",
# ---------- src/download.ts ----------
"A SHA-256 is 64 letters and digits": "SHA-256 为 64 位字母与数字",
"Address": "地址",
"Can't resume · 1 connection": "不支持续传 · 单连接",
"Cancel download?": "取消下载？",
"Connecting…": "正在连接…",
"Download complete": "下载完成",
"Download failed": "下载失败",
"Finding peers who share it. This can take a few seconds.": "正在寻找共享该资源的节点，可能需要几秒。",
"Getting file details…": "正在获取文件信息…",
"Getting video details…": "正在获取视频信息…",
"Hide details": "隐藏详情",
"Location": "保存位置",
"Reading the file list…": "正在读取文件列表…",
"Show details": "显示详情",
"Starting…": "正在开始…",
"Waiting in queue": "排队等待中",
}

# 逻辑键 / 分类值：绝不替换
GUARD = {"Other", "Video", "Music", "Programs", "Compressed", "Documents", "Images",
         "File", "All", "Enter", "Escape", "Del", "Delete", "Space", "Ctrl", "ArrowUp", "ArrowDown",
         "Backspace", "Cookie", "Referer", "User-Agent", "SwiftDL", "checked"}

files = ["index.html", "download.html", "src/main.ts", "src/download.ts"]
report = {}
for rel in files:
    p = os.path.join(ROOT, rel.replace("/", os.sep))
    t = open(p, encoding="utf-8").read()
    orig = t
    hits = []

    # 1) 文本节点 >text<
    def rep_text(m):
        inner = m.group(1)
        core = inner.strip()
        if core in MAP and core not in GUARD:
            hits.append(core)
            lead = inner[:len(inner) - len(inner.lstrip())]
            trail = inner[len(inner.rstrip()):]
            return ">" + lead + MAP[core] + trail + "<"
        return m.group(0)
    t = re.sub(r">([^<>]+)<", rep_text, t)

    # 2) 属性值
    def rep_attr(m):
        name, val = m.group(1), m.group(2)
        if val in MAP and val not in GUARD:
            hits.append(val)
            return '%s="%s"' % (name, MAP[val])
        return m.group(0)
    t = re.sub(r'(placeholder|title|aria-label|alt)="([^"]*)"', rep_attr, t)

    # 3) JS 字符串字面量（单/双引号，不含换行）
    def make_rep(q):
        def f(m):
            v = m.group(1)
            if v in MAP and v not in GUARD:
                hits.append(v)
                return q + MAP[v] + q
            return m.group(0)
        return f
    t = re.sub(r'"([^"\\\n]{2,200})"', make_rep('"'), t)
    t = re.sub(r"'([^'\\\n]{2,200})'", make_rep("'"), t)

    if t != orig:
        open(p, "w", encoding="utf-8", newline="\n").write(t)
    report[rel] = {"replaced": len(hits), "unique": len(set(hits))}

print(json.dumps(report, ensure_ascii=False, indent=1))


# ============ Rust 端（托盘菜单 / 通知 / 状态提示） ============
# 逻辑比较键（label/枚举/按键名）：生成 MAP 时也不要收录
LOGIC_KEYS = {"Delete", "Backspace", "Audio only", "New download", "Other"}

RUST_MAP = {
"could not change start with the computer: {e}": "无法设置开机启动：{e}",
"could not read start with the computer: {e}": "无法读取开机启动状态：{e}",
"Open SwiftDL":"打开 SwiftDL","Quit SwiftDL":"退出 SwiftDL","Ignore speed limit":"忽略限速",
"Download complete":"下载完成","Unpacked":"已解压","Couldn't unpack":"解压失败",
"Downloads finished":"下载全部结束","Going to sleep in a few seconds.":"几秒后将进入睡眠。",
"Shutting down in 60 seconds. To cancel, run: shutdown /a":"60 秒后关机。要取消请运行：shutdown /a",
"Checking the file":"正在检查文件","Getting yt-dlp":"正在获取 yt-dlp","Getting ffmpeg":"正在获取 ffmpeg",
"Unpacking ffmpeg":"正在解压 ffmpeg",
"Unpacking yt-dlp":"正在解压 yt-dlp","couldn't download yt-dlp":"无法下载 yt-dlp","couldn't unpack yt-dlp":"无法解压 yt-dlp","Getting video details":"正在获取视频信息",
"Joining video and audio":"正在合并视频与音频","Merging video and audio":"正在合并视频与音频",
"Joining video and audio needs ffmpeg.":"合并视频与音频需要 ffmpeg。","Finishing":"正在收尾","Starting":"正在开始",
"Best quality":"最佳画质","Audio only":"仅音频","Finding peers":"正在寻找节点","Looking for peers":"正在寻找节点",
"Downloading from 1 peer":"正在从 1 个节点下载","Checking existing pieces":"正在校验已有分块",
"File name is empty":"文件名为空","That isn't a web link":"这不是网页链接",
"That's a large file, not a web page":"这是一个大文件，不是网页","Download not found":"未找到该下载",
"Only regular file downloads can change address":"只有普通文件下载可以更换地址","Pause the download first":"请先暂停下载",
"The file finished, but couldn't be read to check it.":"文件已下载完成，但读取校验失败。",
"This link opens a web page":"该链接打开的是网页",
}
EXT_MAP = {
"Open SwiftDL":"打开 SwiftDL","On this page":"本页视频","Catch downloads":"接管下载",
"Skip files under":"跳过小于","Off":"关闭","Connected":"已连接","Not connected":"未连接","Checking":"检查中",
"Can't reach SwiftDL":"无法连接 SwiftDL",
"Open the app once. If it's already open, restart the browser.":"请先打开一次 SwiftDL。若已在运行，请重启浏览器。",
"Download SwiftDL":"下载 SwiftDL",
"This browser can't find SwiftDL's helper. Install SwiftDL with its installer (not just the .exe file), open it once, then reload this extension.":"浏览器找不到 SwiftDL 的辅助程序。请用安装包（不是单独的 .exe 文件）安装 SwiftDL，打开一次后重新加载本扩展。","On ":"在 ","Hold ":"按住 ",
"while clicking to download in the browser":"再点击，即可改用浏览器下载",
}

def sub_file(p, mp, allow_text):
    t = open(p, encoding="utf-8").read(); o = t; n = 0
    for k, v in mp.items():
        pat = '"' + k + '"'
        if pat in t:
            n += t.count(pat); t = t.replace(pat, '"' + v + '"')
    if allow_text:
        for k, v in mp.items():
            if ">" + k + "<" in t:
                n += t.count(">" + k + "<"); t = t.replace(">" + k + "<", ">" + v + "<")
            if '="' + k + '"' in t:
                n += t.count('="' + k + '"'); t = t.replace('="' + k + '"', '="' + v + '"')
    if t != o:
        open(p, "w", encoding="utf-8", newline="\n").write(t)
    return n

ui = os.path.abspath(ROOT)
app = os.path.dirname(ui)                      # .../app
rs_dir = os.path.join(app, "src-tauri", "src")
repo = os.path.dirname(app)                    # 仓库根

total = 0
if os.path.isdir(rs_dir):
    for f in os.listdir(rs_dir):
        if f.endswith(".rs"):
            total += sub_file(os.path.join(rs_dir, f), RUST_MAP, False)
    print("Rust 端替换:", total)

for d in [os.path.join(repo, "extension"), os.path.join(app, "src-tauri", "gen", "extension-firefox")]:
    if not os.path.isdir(d):
        continue
    for f in os.listdir(d):
        if f.endswith((".html", ".js")):
            sub_file(os.path.join(d, f), EXT_MAP, True)
print("扩展弹窗文案已处理")

print("""
下一步重新编译（前后端一起）：
  cd %s
  npm install && npm run build
  cd src-tauri && cargo build --release
产物：<仓库>/target/release/swiftdl-app.exe，复制出来并附带 extension/ 与 extension-firefox/ 即可。
""" % app)
