> **简体中文汉化版（非官方 fork）**
>
> 本仓库基于上游 [harshsinghsv/swiftdl](https://github.com/harshsinghsv/swiftdl) **v0.5.1** 源码完成界面中文化，
> 遵循上游 MIT 许可，版权与署名归原作者所有。本 fork 只做文案翻译与本地重编译，未改动任何下载逻辑，未加入任何联网上报。
>
> - **汉化范围**：主界面、新建下载浮层（含镜像地址、视频链接）、YouTube 播放列表选择窗口、多选批量操作与批量删除确认框、设置四个页面、任务卡与右键菜单、托盘菜单、系统通知、运行状态与错误提示、搜索命令面板、开机启动与界面缩放等常规设置项、任务栏按钮上的下载进度、浏览器扩展（popup / 页面视频面板 / 右键菜单 / 名称与描述，含「改为通过端口连接」入口及其提示）、手机远程控制页
> - **刻意保留英文**：分类目录名 `Video / Music / Programs / Compressed / Documents / Images / Other`（同时是下载子文件夹名与程序内部判定依据，翻译会导致分类失效）、软件与浏览器品牌名、`KB/s` 等单位
> - **与官方版并存**：应用标识改为 `com.swiftdl.app.cn`，数据目录与单实例锁独立，可与官方版同时运行
> - **构建**：`cd app && npm ci && npm run build`，再 `cd app/src-tauri && cargo build --release --features custom-protocol`（漏掉该 feature 会白屏并报 `ERR_CONNECTION_REFUSED`）
> - **上游更新后如何同步**：[docs/SYNC-zh-CN.md](docs/SYNC-zh-CN.md)（含 `tools/apply-zh.py` 幂等重放与复验清单；`.github/workflows/upstream-watch.yml` 每天检查上游正式版并自动重放，跳过测试版，上游若自带简中则停手）

<div align="center">

<img src="app/icon.svg" width="88" alt="SwiftDL" />

# SwiftDL

### Every download, at full speed.

The free, open-source download manager for Windows, macOS and Linux.

[![Latest release](https://img.shields.io/github/v/release/harshsinghsv/swiftdl?style=flat-square&color=007aff&label=release)](https://github.com/harshsinghsv/swiftdl/releases/latest)
[![CI](https://img.shields.io/github/actions/workflow/status/harshsinghsv/swiftdl/ci.yml?branch=main&style=flat-square&label=CI)](https://github.com/harshsinghsv/swiftdl/actions/workflows/ci.yml)
[![Platforms](https://img.shields.io/badge/platforms-Windows%20%C2%B7%20macOS%20%C2%B7%20Linux-555?style=flat-square)](#download)
[![Built with Rust and Tauri](https://img.shields.io/badge/built_with-Rust_%2B_Tauri-dea584?style=flat-square&logo=rust&logoColor=white)](#how-it-works)
[![MIT license](https://img.shields.io/badge/license-MIT-f4c430?style=flat-square)](LICENSE)

<br />

<img src="docs/assets/demo.gif" width="900" alt="Clicking Download on the Ubuntu website opens SwiftDL's New download window; after Start, the 5.9 GB file downloads over eight connections at about 29 MB/s" />

<sub>▶&nbsp; <a href="https://github.com/harshsinghsv/swiftdl/releases/download/v0.2.1/swiftdl-launch.mp4"><b>Watch the one-minute launch video</b></a></sub>

<br />
<br />

<a href="https://github.com/harshsinghsv/swiftdl/releases/latest"><img src="https://img.shields.io/badge/Download_SwiftDL-18181b?style=for-the-badge" alt="Download SwiftDL" height="40" /></a>

[Why SwiftDL](#your-browser-is-the-bottleneck) · [Download](#download) · [Features](#features) · [How it works](#how-it-works) · [Browser extension](#browser-extension) · [FAQ](#faq) · [Build from source](#build-from-source)

</div>

---

## Your browser is the bottleneck

Browsers download every file over **a single connection**, and many servers cap how fast each connection can go. Click Download on Ubuntu's 5.9 GB installer and Chrome settles in for nearly an hour:

<p align="center"><img src="docs/assets/problem.png" width="820" alt="Chrome's download bubble: ubuntu-26.04.1-desktop-amd64.iso at under 2 MB/s, 56 minutes left" /></p>

SwiftDL splits the same file across many connections at once, keeps every one of them busy until the last byte, and writes straight into the final file. Same file, same internet:

<p align="center"><img src="docs/assets/race.gif" width="820" alt="Same file, same internet: your browser on one connection takes 56 minutes, SwiftDL on eight connections takes 3 minutes 31 seconds" /></p>

And it saves its progress every second, so a crash, a closed laptop or a dropped Wi-Fi connection never means starting over.

## See it in action

Click a download in your browser and SwiftDL takes it from there, with your cookies, so downloads behind a login still work. On video sites, the **Download video** button on the player lets you pick a quality, from 4K down to audio only:

<p align="center"><img src="docs/assets/youtube.gif" width="820" alt="On a YouTube video, SwiftDL's Download video button opens a window with the quality set to 1080p60; the 412 MB video downloads and merges" /></p>

Everything lands in one place: live speed, every connection, queue, pause and resume.

<p align="center"><img src="docs/assets/app-dark.png" width="1000" alt="SwiftDL main window: downloads grouped by status, with live speed, connections and a detail panel" /></p>

## Download

| Platform | Installer |
| --- | --- |
| **Windows** 10 and 11 | [`SwiftDL_x.y.z_x64-setup.exe`](https://github.com/harshsinghsv/swiftdl/releases/latest), installs per user, no admin rights needed |
| **macOS** (Apple silicon and Intel) | [`SwiftDL_x.y.z_universal.dmg`](https://github.com/harshsinghsv/swiftdl/releases/latest) |
| **Linux** | [`.AppImage`, `.deb` or `.rpm`](https://github.com/harshsinghsv/swiftdl/releases/latest) |

Then add the [browser extension](#browser-extension) so SwiftDL can catch your downloads.

> [!NOTE]
> The official source for SwiftDL is [github.com/harshsinghsv/swiftdl](https://github.com/harshsinghsv/swiftdl). Download installers only from its [Releases page](https://github.com/harshsinghsv/swiftdl/releases).

## Features

<table>
<tr>
<td width="50%" valign="top">

### A window for every download

When your browser hands over a file, a small window asks where to save it. Press **Start** and the same window shows live progress, each connection's position and speed, and finally a **Download complete** summary with **Open** and **Show in folder**.

</td>
<td width="50%" valign="top">
<img src="docs/assets/window-progress.png" alt="Download window with live progress and the per-connection view" />
</td>
</tr>
<tr>
<td width="50%" valign="top">
<img src="docs/assets/window-new.png" alt="New download window with the file's address, size, category and save location" />
</td>
<td width="50%" valign="top">

### Know what you're getting first

SwiftDL checks the file before downloading: its real name, size, type and whether the server can resume it. Pick a category and folder, or **Download later** to queue it.

</td>
</tr>
<tr>
<td width="50%" valign="top">

### Fast by design

- **Many connections per file**, up to 32.
- **Dynamic segmentation:** when a connection finishes its part, it takes half of the biggest part left, so nothing sits idle near the end.
- **No joining step:** the file is reserved up front and every connection writes straight into it.

</td>
<td width="50%" valign="top">
<img src="docs/assets/window-complete.png" alt="Download complete window with Open and Show in folder" />
</td>
</tr>
</table>

**Also included**

- **Resume anything.** Pause, quit, lose your connection or crash: SwiftDL continues where it stopped.
- **Torrents and magnet links.** Pick the files you want; SwiftDL opens magnet links and .torrent files from anywhere.
- **Download video button.** A button appears over video players and lists the video and audio files the page loaded.
- **Queue and speed limit.** Choose how many downloads run at once and cap total bandwidth.
- **Tidy by default.** Files are sorted into Video, Music, Programs, Compressed and Documents folders.
- **Command palette.** Press <kbd>Ctrl</kbd> <kbd>K</kbd> to find a download or run any action.
- **Lives in the tray.** Close the window and downloads keep going.
- **Light and dark.** Follows your system, or pick one in Settings.

<div align="center">
<img src="docs/assets/app-light.png" alt="SwiftDL in light mode" width="1000" />
</div>

## How it works

<img src="docs/assets/how-it-works.svg" alt="Your browser hands the link and cookies to SwiftDL; the app asks where to save it and shows a window; the engine checks the file, reserves it and downloads every part over its own connection, straight into the final file." width="1100" />

1. **Check.** SwiftDL asks the server for the first byte. The answer reveals the file's size and whether it can be downloaded in parts.
2. **Reserve.** The full-size file is created on disk, so every connection can write to its own place.
3. **Split.** The file is divided into parts, one per connection, each fetched with an HTTP range request.
4. **Rebalance.** When a connection finishes early, it takes over half of the largest remaining part.
5. **Save progress.** The list of missing ranges is saved every second, which is what makes resume work after a crash.

### Benchmark

<img src="docs/assets/benchmark.svg" alt="On a server that limits each connection to 2 MB/s: 1 connection 2.0 MiB/s in 32 seconds, 8 connections 15.9 MiB/s in 4 seconds, 16 connections 25.1 MiB/s in 2.6 seconds." width="820" />

Eight connections finishing in exactly an eighth of the time shows the rebalancing at work: no connection is left idle while another finishes alone. You can run this yourself with [`tools/throttle_server.py`](tools/throttle_server.py).

## Browser extension

The SwiftDL extension works in **Chrome, Edge, Brave, Vivaldi and Firefox**:

- Sends browser downloads to SwiftDL, with your cookies and referrer.
- Adds **Download with SwiftDL** to the right-click menu on links and media.
- Shows a **Download video** button over video players.
- Hold <kbd>Alt</kbd> while clicking a link to let the browser handle that download.
- Can be turned off for a single site from its popup.

**Firefox:** install it from [Firefox Add-ons](https://addons.mozilla.org/firefox/addon/swiftdl-integration/), or click **Add to Firefox** in SwiftDL's **Settings → Browser**.

**Chrome, Edge, Brave and Vivaldi:** the extension comes with SwiftDL, so there's nothing extra to download. In SwiftDL, click **Add the extension** (or go to **Settings → Browser**) and follow the four steps:

1. Open `chrome://extensions` (or `edge://extensions`).
2. Turn on **Developer mode**.
3. Click **Load unpacked**.
4. Choose SwiftDL's extension folder. The **Open extension folder** button takes you there. On Windows it's `%LOCALAPPDATA%\SwiftDL\extension`.

Use that folder rather than a copy: it stays in place while SwiftDL is installed and is refreshed when SwiftDL updates. If you don't have the app installed, `swiftdl-extension.zip` on the [latest release](https://github.com/harshsinghsv/swiftdl/releases/latest) has the same files.

Once the extension is on the Chrome Web Store, SwiftDL will offer it automatically: Chrome, Edge and Brave show a one-time **New extension added** prompt and you click **Enable**. No browser lets an app install an extension silently.

## FAQ

<details>
<summary><b>Is it really faster?</b></summary>

When the server limits each connection, which many do, yes, by roughly the number of connections (see the [benchmark](#benchmark)). When a single connection already fills your internet line, more connections can't add speed you don't have, but resume and the queue still help.
</details>

<details>
<summary><b>Can it download videos from YouTube?</b></summary>

Yes, and from Vimeo, X, Reddit and other video sites. Click the **Download video** button on the player (or paste the link into **New download**) and pick a quality, from 4K down to audio only. These sites don't serve a plain file, so SwiftDL uses [yt-dlp](https://github.com/yt-dlp/yt-dlp) for them, plus ffmpeg to join the video and audio. Both are downloaded the first time you need them (on macOS and Linux, install ffmpeg with Homebrew or your package manager), and yt-dlp is kept up to date. Only download what you have the right to. DRM-protected video, like Netflix, will never be supported.
</details>

<details>
<summary><b>What happens if my PC crashes mid-download?</b></summary>

Open SwiftDL and press **Resume**. Progress is saved every second, so at most a second of data is downloaded again, as long as the server supports resuming. SwiftDL tells you up front when it doesn't.
</details>

<details>
<summary><b>Do downloads that need a login work?</b></summary>

Yes, when they come from the browser extension. It passes the site's cookies, referrer and user agent along with the link. They're stored with the download so resume works too, and cleared when it completes.
</details>

<details>
<summary><b>Does SwiftDL collect any data?</b></summary>

No. It has no accounts, analytics or telemetry. It only connects to the servers you download from.
</details>

<details>
<summary><b>How do I uninstall it?</b></summary>

Use **Apps & features** on Windows (or remove the app on macOS and Linux). The uninstaller also removes SwiftDL's browser registrations.
</details>

## Build from source

You need [Rust](https://rustup.rs) and the [Tauri prerequisites](https://v2.tauri.app/start/prerequisites/) for your OS.

```bash
git clone https://github.com/harshsinghsv/swiftdl
cd swiftdl
cargo install tauri-cli --version "^2" --locked
cargo test --workspace
cd app/src-tauri && cargo tauri dev
```

| Path | What it is |
| --- | --- |
| [`crates/engine`](crates/engine) | The download engine: probing, segmentation, rebalancing, resume and speed limiting |
| [`crates/cli`](crates/cli) | `swiftdl`, a command-line downloader built on the engine |
| [`app/src-tauri`](app/src-tauri) | The desktop app: download manager, windows, tray and browser integration |
| [`app/ui`](app/ui) | The interface |
| [`extension`](extension) | The Chromium extension (Manifest V3) |
| [`tools`](tools) | A throttled test server and a native-messaging test client |

Working on the interface only? It is TypeScript, built with Vite: run `npm install` and `npm run dev` in `app/`, then open http://localhost:5179. A simulated backend fills it with downloads, so no Rust build is needed. Run `npm run build` once before building the app with Cargo.

## Contributing

Bug reports, ideas and pull requests are welcome. Start with [CONTRIBUTING.md](CONTRIBUTING.md). To report a security problem privately, see [SECURITY.md](SECURITY.md). Release notes are in the [CHANGELOG](CHANGELOG.md).

## License

SwiftDL is released under the [MIT License](LICENSE).
