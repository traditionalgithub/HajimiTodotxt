# HajimiTodotxt

![HajimiTodotxt Banner](banner.png)

[English](README.md) | [繁體中文](README_zht.md) | [简体中文](README_zhs.md)

---

### 概述

HajimiTodotxt 是一款轻量级、本机优先的待办事项管理工具，以单页式 Web 应用程序实现。它基于 [todo.txt 格式](https://github.com/todotxt/todo.txt)并加以扩展，提供简洁的界面来管理您的任务、项目和截止日期。  

关于项目名称：这个项目是最初作为测试Gemini 3.1 Pro性能做出来的个人兴趣项目，因此得此名。不过目前的横幅图像并不是使用Nano Banana生成的。  

本项目尽可能使用免费AI算力生成。

### **首先，todo.txt 是什么？**

[todo.txt](https://github.com/todotxt/todo.txt) 是 Gina Trapani 发起的一套待办事项**纯文本格式规范**，也是本项目的灵感来源。它的第一条、也是最核心的规则很简单：

> **todo.txt 文件中的一行，就是一笔任务。**

它不用数据库、不依赖特定软件、不需要导入导出，任务就存放在一个名为 `todo.txt` 的纯文本文件里，任何文本编辑器都能直接阅读与修改。因为纯文本不受操作系统或软件绑定，所以它具备**可搜索、可携带、轻量、易于处理**的特性，即使某个云端服务挂了，任务清单依然完整无损。

todo.txt 通过特殊标记，让任务可以沿着三个轴向被切割、检视：

- **优先级（Priority）**：`(A)` ~ `(Z)`，`(A)` 最重要，让你一眼看出接下来该做什么
- **项目（Project）**：`+项目`，例如 `+打扫车库`，用于列出某个项目下的所有任务
- **情境（Context）**：`@情境`，例如 `@家`、`@办公室`、`@手机`，源自 David Allen 的《搞定》（Getting Things Done），依照地点与场合分类任务

**格式规则：**

| 元素 | 格式 | 说明 |
|------|------|------|
| 优先级 | `(A)` ~ `(Z)` | 若有优先级，**必须**出现在最前面 |
| 创建日期 | `YYYY-MM-DD` | 可选，接在优先级之后 |
| 完成标记 | `x` | 已完成任务以**小写** `x` 开头，后面接完成日期 |
| 项目标签 | `+项目` | 可有多个，出现于优先级/日期之后 |
| 情境标签 | `@情境` | 可有多个 |
| 附加字段 | `key:value` | 扩展用，例如 `due:2026-04-10` 表示截止日期 |

**完整示例：**

```
x 2011-03-02 2011-03-01 Review Tim's pull request +TodoTxtTouch @github
```

这表示一笔于 2011-03-01 创建、2011-03-02 完成的任务，属于 `+TodoTxtTouch` 项目与 `@github` 情境。

由于 todo.txt 就是纯文本，它特别适合：

- **可携带**：任何系统、任何编辑器都能读写，也可用 Git 做版本控制
- **可同步**：配合 Syncthing、Rclone 等工具即可跨设备同步
- **长久保存**：纯文本格式不会过时，没有供应商锁定（vendor lock-in）的风险
- **生态系**：有数十种兼容的 CLI、桌面、移动应用程序可供选用

HajimiTodotxt 保留了这套「纯文本、一行一任务」的优雅精神，并在其上加入层级式项目、重复任务等扩展——也就是下一节要谈的内容。

### **和原 todo.txt 格式相比有什么区别？**

HajimiTodotxt 兼容 todo.txt 核心规范（`(A)` 优先级、创建日期、`x` 完成标记、`+项目`、`@情境`），但在此基础上进行了大量扩展。主要差异如下：

**注：部分功能可能不在其他的 todotxt 类软件中实现**

**1. 扩展字段（原格式没有的 metadata）**

| 字段 | 说明 |
|------|------|
| `t:YYYY-MM-DD` | 隐藏日期（threshold）：此日期前的任务默认隐藏，以虚线边框和较低透明度呈现 |
| `rec:...` | 重复规则：完成任务后自动生成下一次任务 |
| `desc:"..."` | 多行详细描述：`"..."` 中可填入多行描述用以记录任务提示，可以简单地把任务提示（例如相关信息的网址）或实现步骤记录于此。
以 `\n` 换行，若输入中带有 `\n` 者将自动叠加 `\` 进行字符逃逸 |
| `id:...` | ID 字段（旧版本功能，仅在 `show_id=true` 时输出，预计未来弃用） |

注：desc 字段**可能不在其他 `todo.txt` 类软件中**
**2. 层级式项目**
- 原 todo.txt 只有扁平的 `+项目`，HajimiTodotxt 支持 `+项目.子项目.孙项目` 任意层级，借鉴 [TaskWarrior](https://taskwarrior.org/) 的多层级 `+project.subproject` 思路
- 项目过滤支持通配符：`+项目.*`（单一层级）、`+**.子项目`（任意层数）
- 提供项目树状视图、项目概览，点击项目区段即可筛选

**3. 重复任务**
- 原 todo.txt 规范完全没有重复任务，而常见的扩展规则以 `rec:` 标签实现这个功能，HajimiTodotxt 也不例外：
  - `+1d` / `+1m` / `+1y`：以今天为基准重复
  - `1d`（无前缀）：以原截止日为基准重复
  - 纯数字 `rec:5` 自动视为 `rec:+5d`
  - `++1d` / `++1m` / `++1y`：**（可能不在其他的 todotxt 软件中实现）**跳到下一个大于今天的日期（以原截止日步进），用意是实现 [orgmode](https://orgmode.org/) 的 `++` 语法
- 完成含 `rec:` 的任务时自动生成下一次任务；若同时有 `t:`，会保持与 `due:` 的相对距离
- 描述中的 `---REPEAT-ABOVE---` / `---REPEAT-COPY---` 可控制哪些内容复制给下一个带 `rec:` 标签的往复任务

**4. 今日任务标记**
类似于 [MS Todo](https://en.wikipedia.org/wiki/Microsoft_To_Do) 和 [Super Productivity](https://github.com/super-productivity/super-productivity) 的"今日任务"功能
- 特殊的 `@☀️.YYYYMMDD` 情境标签，用于标记今日任务，显示时会自动隐藏
- 当日以 ☀️、过期以 😱、未来以 🌙 显示视觉指示

**5. 搜索/过滤语法**
- 日期比较：`<today`、`<=tomorrow`、`>2026-08-10`，可以快速过滤指定日期前后的任务
- 优先级表达式：`pri=A`、`pri<C`、`pri=A-C`（范围）、`pri=A,B`（列表）、`pri=!`（无优先级）
- 项目通配符过滤、情境标签点击过滤

**6. 其他差异**
- 任务以「行号」定位（数组索引），不依赖 ID
- `todo.rc` 配置支持 JSON 复杂结构（`sort_keys`、`saved_filters`、`opacity` 等）
- 服务器层面：随机 Token 认证、原子化写入（临时文件 + rename）、CORS 仅允许本机、CSRF 防护

**主要功能：**
- 层级式项目系统（`+项目.子项目`）
- 情境标签（`@情境`）用于任务分类
- 截止日期与隐藏日期
- 重复任务
- 今日任务视觉指示
- 23 种内置主题
- 多语言支持（繁体中文 / 英文）
- 原子化文件写入确保数据安全
- 响应式手机界面

### 安装

#### 系统要求
- Python 3.10 或更高版本
- 无需安装外部依赖

#### 安装步骤

```bash
# 1. 克隆仓库
git clone https://github.com/traditionalgithub/HajimiTodotxt.git
cd HajimiTodotxt

# 2. 启动服务器
python server.py
```

服务器将显示带有认证令牌的 URL：
```
★ HajimiTodotxt 后端服务已启动！
★ 安全认证链接（请复制并在浏览器中打开）：
   http://127.0.0.1:6888/?token=abc123def456...
```

### 使用方法

1. **访问应用程序**：从终端复制 URL 并在浏览器中打开
2. **添加任务**：点击标题栏中的 ➕ 按钮
3. **完成任务**：点击任务旁的复选框
4. **过滤任务**：使用搜索栏或点击项目/情境标签
5. **排序任务**：点击 🔃 按钮设置排序方式

### 任务格式

任务遵循 todo.txt 格式并加以扩展：

```
[x YYYY-MM-DD] (优先级) YYYY-MM-DD 任务标题 +项目 @情境 due:YYYY-MM-DD t:YYYY-MM-DD rec:rec:+1d desc:"描述"
```

**任务示例：**
```
(A) 2026-04-06 撰写报告 +工作.项目 due:2026-04-10 desc:"期末报告"
(B) 2026-04-06 数学练习 +学校.数学 due:2026-04-15 @图书馆
x 2026-04-05 (C) 2026-04-01 已完成任务 +个人
```

### 配置设定

编辑 `todo.rc` 自定义设置：

```ini
theme=nord-light                    # 主题选择（23种选项）
confirm_delete=true                 # 删除任务前确认
default_priority=(C)                # 新任务默认优先级
expand_projects=false               # 默认展开项目
click_action=filter                 # 点击动作："filter" 或 "clipboard"
```

**可用主题：** neutral、dark、solarized-light、nord-light、sakura、mint、lavender、peach、cream、sky、matcha、linen、honey、seafoam、cloud、coral、solarized-dark、nord-dark、dim、forest、twilight、cocoa

### 快捷键

| 按键 | 动作 |
|------|------|
| `+` | 添加任务 |
| `/` | 聚焦搜索栏 |
| `Esc` | 关闭对话框 |

### API 端点

| 端点 | 方法 | 描述 |
|------|------|------|
| `/` | GET | 提供 index.html |
| `/api/read?file={todo\|done\|config}` | GET | 读取文件内容 |
| `/api/write` | POST | 写入文件内容 |

---

### 开发

```bash
# 启动开发服务器
python server.py

# 在浏览器中访问
# 从终端复制显示的 URL
```

### 项目结构

```
HajimiTodotxt/
├── index.html           # 前端 SPA（HTML/CSS/JS 全部内联）
├── server.py            # Python HTTP 服务器
├── todo.txt             # 未完成任务
├── done.txt             # 已完成任务
├── todo.rc              # 用户配置
└── lang/
    ├── zh-TW.json       # 繁体中文
    └── en.json          # 英文
```

### 数据同步

使用以下工具跨设备同步数据：
- [Syncthing](https://syncthing.net/)
- [Rclone](https://rclone.org/)

同步以下文件：
- `todo.txt`
- `done.txt`
- `todo.rc`

---

**授权条款：** [Blue Oak Model 授权 1.0.0](https://blueoakcouncil.org/license/1.0.0)
**最后更新：** 2026-08-10