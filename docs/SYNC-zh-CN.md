# 上游更新后如何同步汉化（zh-CN 分支维护指南）

本仓库是 [harshsinghsv/swiftdl](https://github.com/harshsinghsv/swiftdl) 的简体中文汉化 fork。

分支模型：

| 分支 | 用途 |
| --- | --- |
| `main` | 与上游 `harshsinghsv/swiftdl:main` 保持一致，**不放汉化改动**，仅用于比对与合并 |
| `zh-CN` | 全部汉化改动所在分支，构建产物即中文版 |

---

## 一、一次性配置

```bash
git remote add upstream https://github.com/harshsinghsv/swiftdl.git
git remote set-url --push upstream DISABLE   # 防止误推上游
git fetch upstream --tags
```

## 二、每次上游发版后的同步步骤

```bash
# 1. 拉取上游最新代码与 tag
git fetch upstream --tags

# 2. 切到汉化分支
git checkout zh-CN

# 3. 合并上游（冲突几乎都集中在 UI 文案、tauri.conf.json、Rust 提示串）
git merge upstream/main
```

**冲突处理原则：逻辑取上游，文案取中文。** 上游重构过的函数结构必须原样采用，只在用户可见字符串处保留中文。

```bash
# 4. 重放已知文案映射（幂等，只翻译命中的英文原串）
python tools/apply-zh.py app/ui

# 5. 找出上游新增、尚未翻译的英文
python tools/extract-en.py app/ui > /tmp/en.json    # 可选：导出候选清单
#    对照清单人工补译，补进 tools/apply-zh.py 的 MAP 后重跑第 4 步

# 6. 重新构建（两条命令都要跑）
cd app && npm ci && npm run build
cd src-tauri && cargo build --release --features custom-protocol
```

> `--features custom-protocol` **不能省**。缺这个 feature 时 Tauri 按 dev 模式启动，
> 窗口会去请求 `http://localhost:5179`，表现为白屏 + `ERR_CONNECTION_REFUSED`，
> 前端资源也不会嵌进 exe。

```bash
# 7. 打 tag 并发布
gh release create vX.Y.Z-zh.1 \
  --title "SwiftDL vX.Y.Z 简体中文版" \
  --notes "基于上游 vX.Y.Z 的源码级汉化，功能与上游一致，仅界面中文化。"
```

## 三、每次都要过的复验清单

| 场景 | 检查点 |
| --- | --- |
| 主界面 | 网络/速度/空闲状态、侧栏分类、任务卡、空状态 |
| 新建下载浮层 | 标题、粘贴提示、按钮（从剪贴板粘贴 / 在页面中查找文件 / 稍后下载 / 下载） |
| 设置四页 | 常规、速度、浏览器、关于 |
| 任务卡右键 | 打开 / 在文件夹中显示 / 暂停 / 继续 / 重试 / 用浏览器下载 / 复制链接 / 取消下载 |
| 托盘菜单 | 打开 SwiftDL / 忽略限速 / 退出 SwiftDL |
| 系统通知 | 下载完成 / 已解压 / 解压失败 / 下载全部结束 |
| 异常路径 | 链接不支持、404、yt-dlp 或 ffmpeg 缺失、Debrid 令牌无效、非 torrent 文件 |
| 浏览器扩展 | popup、页面视频面板（本页的视频与音频 / 流媒体 / 此视频 / 在 SwiftDL 中选择画质 / 暂未找到可下载的文件 / 仅音频）、右键菜单、扩展名称与描述 |
| 远程页 | 标题「SwiftDL 远程控制」 |

## 四、三条容易踩的坑

1. **分类目录名绝对不要翻译。** `Video / Music / Programs / Compressed / Documents / Images / Other`
   同时是下载目录下的子文件夹名和程序内部的分类判定依据，翻译会让路径改名、分类失效。
2. **扩展里用于字符串比较的值必须与显示文案同步改。** 例如音轨项的标签参与
   `q.label === "Audio only"` 这类比较，显示改成「仅音频」后比较值也要一起改，否则逻辑失效。
3. **应用标识保持 `com.swiftdl.app.cn`。** 这样中文版与原版的数据目录、单实例锁互不干扰，
   两个版本可以同时运行；若改回上游的 `com.swiftdl.app`，会与官方版抢同一把锁。

## 五、上游大改版时

若上游重写了 UI 结构（换框架、换组件库、文案迁到 i18n 文件），纯文本替换会大面积失配。
此时不要逐条硬改，按这个顺序做：

1. `git diff upstream/main zh-CN --stat` 看改动范围；
2. 若上游已引入 i18n 语言文件，直接新增 `zh-CN` 语言包，比改源码更省事，也更利于跟随上游；
3. 若仍是硬编码文案，重新导出英文候选清单，重建 `tools/apply-zh.py` 的 MAP；
4. 构建 + 过第三节复验清单。
