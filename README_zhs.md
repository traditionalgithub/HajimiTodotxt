# HajimiTodotxt

![HajimiTodotxt Banner](banner.png)

[English](README.md) | [繁體中文](README_zht.md) | [简体中文](README_zhs.md)

---

### 概述

HajimiTodotxt 是一款轻量级、本机优先的待办事项管理工具，以单页式 Web 应用程序实现。它基于 todo.txt 格式并加以扩展，提供简洁的界面来管理您的任务、项目和截止日期。  

关于项目名称：这个项目是最初作为测试Gemini 3.1 Pro性能做出来的个人兴趣项目，因此得此名。不过目前的横幅图像并不是是使用Nano Banana生成的。  

本项目尽可能使用免费AI算力生成。

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