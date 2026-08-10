# HajimiTodotxt

![HajimiTodotxt Banner](banner.png)

[English](README.md) | [繁體中文](README_zht.md) | [简体中文](README_zhs.md)

---

### 概述

HajimiTodotxt 是一款輕量級、本機優先的待辦事項管理工具，以單頁式 Web 應用程式實現。它基於 todo.txt 格式並加以擴展，提供簡潔的介面來管理您的任務、專案和截止日期。  

關於項目名稱：這個項目是最初作爲測試Gemini 3.1 Pro性能做出來的個人興趣項目，因此得此名。不過目前的橫幅圖像並不是是使用NanoBanana生成的。

本項目儘可能使用免費AI算力生成。

**主要功能：**
- 階層式專案系統（`+專案.子專案`）
- 情境標籤（`@情境`）用於任務分類
- 截止日期與隱藏日期
- 重複任務
- 今日任務視覺指示
- 23 種內建主題
- 多語言支援（繁體中文 / 英文）
- 原子化檔案寫入確保資料安全
- 響應式手機介面

### 安裝

#### 系統要求
- Python 3.10 或更高版本
- 無需安裝外部依賴

#### 安裝步驟

```bash
# 1. 克隆儲存庫
git clone https://github.com/traditionalgithub/HajimiTodotxt.git
cd HajimiTodotxt

# 2. 啟動伺服器
python server.py
```

伺服器將顯示帶有認證令牌的 URL：
```
★ HajimiTodotxt 後端服務已啟動！
★ 安全認證連結（請複製並在瀏覽器中開啟）：
   http://127.0.0.1:6888/?token=abc123def456...
```

### 使用方法

1. **存取應用程式**：從終端複製 URL 並在瀏覽器中開啟
2. **新增任務**：點擊標題列中的 ➕ 按鈕
3. **完成任務**：點擊任務旁的核取方塊
4. **過濾任務**：使用搜尋欄或點擊專案/情境標籤
5. **排序任務**：點擊 🔃 按鈕設定排序方式

### 任務格式

任務遵循 todo.txt 格式並加以擴展：

```
[x YYYY-MM-DD] (優先級) YYYY-MM-DD 任務標題 +專案 @情境 due:YYYY-MM-DD t:YYYY-MM-DD rec:rec:+1d desc:"描述"
```

**任務範例：**
```
(A) 2026-04-06 撰寫報告 +工作.專案 due:2026-04-10 desc:"期末報告"
(B) 2026-04-06 數學練習 +學校.數學 due:2026-04-15 @圖書館
x 2026-04-05 (C) 2026-04-01 已完成任務 +個人
```

### 配置設定

編輯 `todo.rc` 自訂設定：

```ini
theme=nord-light                    # 主題選擇（23種選項）
confirm_delete=true                 # 刪除任務前確認
default_priority=(C)                # 新任務預設優先級
expand_projects=false               # 預設展開專案
click_action=filter                 # 點擊動作："filter" 或 "clipboard"
```

**可用主題：** neutral、dark、solarized-light、nord-light、sakura、mint、lavender、peach、cream、sky、matcha、linen、honey、seafoam、cloud、coral、solarized-dark、nord-dark、dim、forest、twilight、cocoa

### 快捷鍵

| 按鍵 | 動作 |
|------|------|
| `+` | 新增任務 |
| `/` | 聚焦搜尋欄 |
| `Esc` | 關閉對話框 |

### API 端點

| 端點 | 方法 | 描述 |
|------|------|------|
| `/` | GET | 提供 index.html |
| `/api/read?file={todo\|done\|config}` | GET | 讀取檔案內容 |
| `/api/write` | POST | 寫入檔案內容 |

---

### 開發

```bash
# 啟動開發伺服器
python server.py

# 在瀏覽器中存取
# 從終端複製顯示的 URL
```

### 專案結構

```
HajimiTodotxt/
├── index.html           # 前端 SPA（HTML/CSS/JS 全部內聯）
├── server.py            # Python HTTP 伺服器
├── todo.txt             # 未完成任務
├── done.txt             # 已完成任務
├── todo.rc              # 使用者配置
└── lang/
    ├── zh-TW.json       # 繁體中文
    └── en.json          # 英文
```

### 資料同步

使用以下工具跨裝置同步資料：
- [Syncthing](https://syncthing.net/)
- [Rclone](https://rclone.org/)

同步以下檔案：
- `todo.txt`
- `done.txt`
- `todo.rc`

---

**授權條款：** [Blue Oak Model 授權 1.0.0](https://blueoakcouncil.org/license/1.0.0)
**最後更新：** 2026-08-10