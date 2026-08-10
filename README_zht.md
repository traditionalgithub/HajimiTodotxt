# HajimiTodotxt

![HajimiTodotxt Banner](banner.png)

[English](README.md) | [繁體中文](README_zht.md) | [简体中文](README_zhs.md)

---

### 概述

HajimiTodotxt 是一款輕量級、本機優先的待辦事項管理工具，以單頁式 Web 應用程式實現。它基於 [todo.txt 格式](https://github.com/todotxt/todo.txt)，並在儘可能確保和原格式相容的前提下進行大幅度魔改，提供簡潔的介面來管理您的任務、專案和截止日期。  

關於項目名稱：這個項目是最初作爲測試Gemini 3.1 Pro性能做出來的個人興趣項目，因此得此名。不過目前的橫幅圖像並不是使用NanoBanana生成的。

**本項目儘可能使用免費AI算力生成。**

### **和原 todo.txt 格式相比有什麼區別？**

HajimiTodotxt 相容 todo.txt 核心規範（`(A)` 優先級、建立日期、`x` 完成標記、`+專案`、`@情境`），但在此基礎上進行了大量擴展。主要差異如下：

**注：部分功能可能不在其他的 todotxt 類軟件中實現**

**1. 擴展欄位（原格式沒有的 metadata）**

| 欄位 | 說明 |
|------|------|
| `t:YYYY-MM-DD` | 隱藏日期（threshold）：此日期前的任務預設隱藏，以虛線邊框和較低透明度呈現 |
| `rec:...` | 重複規則：完成任務後自動產生下一次任務 |
| `desc:"..."` | 多行詳細描述：`"..."`中可填入多行描述用以記錄任務提示，以`\n`換行，若輸入中帶有`\n`者將自動疊加`\`進行字符逃脫 |
| `id:...` | ID 欄位（舊版本功能，僅在 `show_id=true` 時輸出，預計未來棄用） |

注：desc欄位**可能不在其他`todo.txt`類軟件中**，其用意是以`todo.txt`優雅易讀設計換取易用性，可以簡單地把任務提示（例如相關資訊的網址）或實現步驟記錄於此。

**2. 階層式專案**
- 原 todo.txt 只有扁平的 `+專案`，HajimiTodotxt 支援 `+專案.子專案.孫專案` 任意層級，借鑑[TaskWarrior](https://taskwarrior.org/)的多層級 `+project.subproject`的思路
- 專案過濾支援萬用字元：`+專案.*`（單一層級）、`+**.子專案`（任意層數）
- 提供專案樹狀檢視、專案概覽，點擊專案區段即可篩選

**3. 重複任務**
- 原 todo.txt 規範完全沒有重複任務，而常見的擴展規則以`rec:`標籤實現這個功能，HajimiTodotxt也不例外：
  - `+1d` / `+1m` / `+1y`：以今天為基準重複
  - `1d`（無前綴）：以原截止日為基準重複
  - 純數字 `rec:5` 自動視為 `rec:+5d`
  - `++1d` / `++1m` / `++1y`：**（可能不在其他的 todotxt 軟件中實現）**跳到下一個大於今天的日期（以原截止日步進），用意是實現[Org mode](https://orgmode.org/)的`++`語法
- 完成含 `rec:` 的任務時自動產生下一次任務；若同時有 `t:`，會保持與 `due:` 的相對距離
- 描述中的 `---REPEAT-ABOVE---` / `---REPEAT-COPY---` 可控制哪些內容複製給下一個帶`rec:`標籤的往復任務

**4. 今日任務標記**
類似於[MS Todo](https://en.wikipedia.org/wiki/Microsoft_To_Do) 和 [Super Productivity](https://github.com/super-productivity/super-productivity)的“今日任務”功能
- 特殊的 `@☀️.YYYYMMDD` 情境標籤，用於標記今日任務，顯示時會自動隱藏
- 當日以 ☀️、過期以 😱、未來以 🌙 顯示視覺指示

**5. 搜尋／過濾語法**
- 日期比較：`<today`、`<=tomorrow`、`>2026-08-10`，可以快速過濾指定日期前後的任務
- 優先級運算式：`pri=A`、`pri<C`、`pri=A-C`（範圍）、`pri=A,B`（清單）、`pri=!`（無優先級）
- 專案萬用字元過濾、情境標籤點擊過濾

**6. 其他差異**
- 任務以「行號」定位（陣列索引），不依賴 ID
- `todo.rc` 配置支援 JSON 複雜結構（`sort_keys`、`saved_filters`、`opacity` 等）
- 伺服器層面：隨機 Token 認證、原子化寫入（暫存檔 + rename）、CORS 僅允許本機、CSRF 防護

### **主要功能：**
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