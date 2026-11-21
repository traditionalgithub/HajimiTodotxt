# REPLICA.md — HajimiTodotxt 完整復刻文檔

> **生成此文檔的提示詞：**
> 請先參考 AGENT.md、SPEC.md、brief.md 文檔。之後根據此待辦和個人記事本項目的包括外觀和介面設計、工具運作邏輯、技術棧構成等等，生成一個 REPLICA.md 文檔，使得這個項目可以給新的智能體完整復刻。

---

## 目錄

1. [專案概述](#1-專案概述)
2. [檔案結構與用途](#2-檔案結構與用途)
3. [技術棧](#3-技術棧)
4. [後端伺服器 server.py](#4-後端伺服器-serverpy)
5. [前端 index.html](#5-前端-indexhtml)
6. [數據格式規範](#6-數據格式規範)
7. [API 端點](#7-api-端點)
8. [認證與安全機制](#8-認證與安全機制)
9. [使用者介面設計](#9-使用者介面設計)
10. [前端功能模組](#10-前端功能模組)
11. [任務操作流程](#11-任務操作流程)
12. [今日任務功能](#12-今日任務功能)
13. [國際化 i18n](#13-國際化-i18n)
14. [開發規則與慣例](#14-開發規則與慣例)

---

## 1. 專案概述

### 1.1 專案名稱
**HajimiTodotxt** (哈基米待辦 / Hajimi Todo)，內部版本號 v7.2.2.1.5.0

### 1.2 專案類型
輕量級 Web 應用 (SPA — Single Page Application) / 個人待辦工具

基於 todo.txt 格式但有相當程度擴展，支援階層式專案、上下文標籤、截止日期、重複任務、今日任務過濾等功能。

### 1.3 核心設計原則
- **簡約優先** — UI 簡潔，降低認知負擔
- **資料安全** — 原子化寫入防止資料損毀
- **本機優先** — 無雲端服務，資料本地純文字儲存
- **Unix 哲學** — 開放檔案格式，可與外部工具互操作（如 Syncthing / Rclone 同步）

### 1.4 啟動方式
```bash
python server.py
# 終端機會顯示帶 token 的 URL，複製到瀏覽器打開
# 例如: http://127.0.0.1:6888/?token=abc123...
```

---

## 2. 檔案結構與用途

```
.
├── SPEC.md              # 項目規格文件（需隨項目變化更新）
├── RULES.md             # AI Agent 工作規範
├── REPLICA.md           # 本文件 — 完整復刻文檔
├── AGENT.md             # 智能體行為指引
├── brief.md             # 開發備忘錄（含詳細行為規範）
├── index.html           # 前端主檔案（HTML/CSS/JS 全部內聯）
├── server.py            # 後端伺服器（Python http.server）
├── todo.txt             # 未完成任務儲存
├── done.txt             # 已完成任務儲存
├── todo.rc              # 用戶配置檔案
├── lang/
│   ├── zh-TW.json       # 繁體中文語言資源
│   └── en.json          # 英文語言資源
├── worklog/             # 工作總結報告目錄（人類查閱用，AI 預設忽略）
├── obsolete/            # 過時檔案目錄（AI 必須忽略）
└── server.v7p2.py / server.v7p4.py  # 舊版伺服器備份
```

**重要規則：**
- `obsolete/` 目錄中的內容反映歷史狀態，**AI 智能體必須忽略此目錄中的所有內容**
- `worklog/` 目錄主要作存檔用途，**除非用戶指定，AI 智能體應忽略此目錄**
- 每次施工後應在 `worklog/` 留下一份 `yyyymmdd.n.md` 工作總結報告
- 施工後需檢查 `SPEC.md` 並在必要時更新

---

## 3. 技術棧

### 3.1 前端
- **HTML5** — 單一 HTML 檔案，全部內聯
- **CSS3** — 內聯樣式，CSS 變數驅動多主題系統
- **JavaScript (ES6+)** — 純原生 JS，**無框架依賴**
- **i18n** — 基於 JSON 語言資源檔的動態語言切換

### 3.2 後端
- **Python 3.10+** — 僅使用標準庫 `http.server`
- **HTTP 協議** — RESTful API 風格
- **認證** — Cookie-based Session + URL Token

### 3.3 資料儲存
- 純文字檔案 (UTF-8 編碼)
- 格式相容 todo.txt 規範（含擴展）

---

## 4. 後端伺服器 server.py

### 4.1 總覽
單一 Python 檔案，基於 `http.server.SimpleHTTPRequestHandler`，監聽 `127.0.0.1:6888`。
支援 socket 地址重用 (`allow_reuse_address = True`)。

### 4.2 核心行爲

#### 4.2.1 靜態檔案服務
繼承 `SimpleHTTPRequestHandler.do_GET()` 提供靜態檔案（如 `lang/*.json`），但需通過認證檢查。

#### 4.2.2 根路徑 `/`
- 返回 `index.html`
- 若為首次登入請求（URL 含有效 token），種植 `auth` Cookie
- Cookie 屬性: `httponly=True`, `samesite=Strict`
- Cache-Control: `no-store, no-cache, must-revalidate`

#### 4.2.3 GET `/api/read?file={todo|done|config}`
- 讀取指定檔案內容
- 若 `file=config`，解析 `key=value` 格式為 JSON 物件（value 嘗試 `json.loads` 解析）
- 回應：`{"content": "..."}` 或 `{key: value, ...}`
- Header 必須包含 `Cache-Control: no-store`

#### 4.2.4 GET `/api/fileinfo?file={todo|done|config}`
- 讀取檔案修改時間 (`os.path.getmtime`)
- 回應：`{"mtime": 1234567890.123}`

#### 4.2.5 POST `/api/write`
- Body: `{"file": "todo", "content": "..."}`
- 若 `file=config`，content 為物件，轉換為 `key=value` 格式寫入
- **原子化寫入策略**：先寫入 `.tmp` 臨時檔案，再用 `os.replace()` 替換原檔案
- 成功回應：`{"status": "ok"}` + HTTP 200
- 失敗回應：HTTP 500 + 錯誤訊息

#### 4.2.6 POST 安全性
- 必須檢查 Origin/Referer 是否為 `http://127.0.0.1:{PORT}`
- 必須檢查 Cookie 中的 auth token

### 4.3 日誌
`do_POST` 成功寫入時在終端印出 `.`（不換行），失敗時印出 `[ERROR]` 訊息。
`log_message` 被覆蓋為 `pass`（不輸出預設日誌）。

---

## 5. 前端 index.html

### 5.1 總覽
單一 HTML 檔案，2220 行（當前版本），包含全部 CSS 樣式與 JavaScript 邏輯。
使用 IIFE 模式封裝在 `App` 命名空間下。

### 5.2 啟動流程
```
1. window.onload → App.init()
2. 偵測語言（localStorage → navigator.language → 預設 zh-TW）
3. 載入語言資源 /lang/{lang}.json
4. 初始化 DOM 快取
5. 初始化優先級下拉選單 (A-Z)
6. 初始化排序選單 UI
7. 初始化事件委派
8. 載入配置 (loadConfig) → 應用主題/透明度/寬度
9. 載入資料 (loadData) → 從 /api/read 獲取 todo.txt & done.txt
10. 更新 UI 文字 (updateUI)
11. 渲染任務列表 (render)
```

### 5.3 重要架構

#### App 命名空間公開方法：

| 方法 | 用途 |
|------|------|
| `init()` | 初始化 |
| `render()` | 渲染任務列表 |
| `openProjectView()` | 開啟專案概覽視窗 |
| `closeProjectView()` | 關閉專案概覽視窗 |
| `jumpToTask(index, isDone)` | 從專案概覽跳轉到主視圖任務並高亮 |
| `toggleProjectViewChildren(id)` | 展開/收起專案子節點 |
| `toggleProjectViewDescriptions(e, id)` | 展開/收起專案下所有任務描述 |
| `toggleAllProjectViewNodes()` | 一鍵全部展開/收起 |
| `sync()` | 同步資料到伺服器 |
| `loadData()` | 載入 todo/done |
| `loadConfig()` | 載入配置 |
| `saveConfig()` | 儲存配置 |
| `openEditModal(index, isDone)` | 開啟編輯視窗 |
| `closeEditModal()` | 關閉編輯視窗 |
| `saveTask()` | 儲存任務（關閉視窗） |
| `saveTaskAndKeepOpen()` | 儲存任務（保持開啟） |
| `saveTaskAndComplete()` | 儲存任務內容並立即完成（重複任務往復用） |
| `deleteTask(index, isDone)` | 刪除任務 |
| `deleteTaskFromEdit()` | 從編輯視窗刪除 |
| `completeTask(index)` | 完成任務 |
| `uncompleteTask(index)` | 取消完成 |
| `toggleTodayFilter()` | 切換今日過濾 |
| `toggleTaskToday(index)` | 切換今日標記 |
| `toggleTaskTodayInModal()` | 編輯器中切換今日 |
| `toggleShowHidden()` | 切換隱藏任務顯示 |
| `toggleDoneSection()` | 展開/收起已完成 |
| `clearFilter()` | 清空過濾欄 |
| `applyTheme(theme)` | 套用主題 |
| `applyMainWidth(width)` | 套用主寬度 |
| `applyOpacity(value)` | 套用隱藏任務透明度 |
| `applyDoneOpacity(value)` | 套用已完成透明度 |
| `switchTab(tab)` | 切換編輯分頁 |
| `toggleSortMenu(event)` | 排序選單 |
| `toggleSavedFilters(event)` | 常用過濾器選單 |
| `openContextMenu(event, targetId)` | 上下文標籤選單 |
| `openProjectMenu(event, targetId)` | 專案標籤選單（階層式樹狀） |
| `appendTagToInput(targetId, tag)` | 插入標籤到輸入框 |
| `insertDateToDesc()` | 插入當前時間到描述 |
| `insertRepeatSeparator()` | 插入重複分隔線 |
| `insertRepeatSeparatorBoth()` | 插入複製分隔線 |
| `renumberNumberedItems()` | 重新編號 |
| `resizeTitleInput(action)` | 調整標題輸入框大小 |
| `resizeDescInput(action)` | 調整描述輸入框大小 |
| `updateSort(i, k, v)` | 更新排序規則 |
| `updateDoneSort(i, k, v)` | 更新已完成排序 |
| `updateUI()` | 更新所有 UI 文字（i18n） |
| `toggleDesc(index)` | 展開/收起描述 |
| `saveCurrentFilter()` | 儲存當前過濾條件 |
| `applyFilter(q)` | 套用過濾條件 |
| `removeFilter(e, idx)` | 刪除過濾條件 |
| `toggleProjectChildren()` | 展開/收起專案子節點 |
| `toggleAllProjectChildren()` | 全部展開/收起 |

### 5.4 資料同步 sync()

```
1. tasks.map(stringifyTask).join('\n') → todo.txt 文本
2. doneTasks.map(stringifyTask).join('\n') → done.txt 文本
3. Promise.all 併發 POST /api/write 寫入 todo 和 done
4. 檢查每個 response.ok
   → 任一失敗則 alert 錯誤訊息
5. try...catch 捕獲網路錯誤
```

### 5.5 事件處理
採用事件委派模式：在 `document.body` 上監聽 `click` 事件，根據 `e.target` 判斷操作類型：
- `input[type="checkbox"][data-action]` → complete / uncomplete
- `.btn-edit` → openEditModal
- `.btn-today` → toggleTaskToday
- `.btn-delete` → deleteTask
- `.desc-toggle` → toggleDesc
- `[data-tag]` → `handleFieldClick()`（點擊專案/情境/優先度/日期等標籤，根據 `click_action` 設定決定加入過濾或複製到剪貼簿）
- `.task-subject` → `handleFieldClick()`（點擊標題純文字，同上）
- 點擊非選單/按鈕區域 → 關閉所有浮動選單

---

## 6. 數據格式規範

### 6.1 任務格式 (todo.txt / done.txt)

**核心結構：**
```
[x 完成日期] [優先級] [建立日期] 任務標題 [metadata:值] [desc:"描述"]
```

**完整字段表：**

| 字段 | 標籤 | 類型 | 描述 | 範例 |
|------|------|------|------|------|
| 完成狀態 | `x` | 可選 | 已完成則以 `x YYYY-MM-DD` 開頭 | `x 2025-11-27` |
| 優先級 | `(A)-(Z)` | 可選 | 單一大寫字母，圓括號 | `(A)` |
| 建立日期 | `YYYY-MM-DD` | 可選 | 任務創建日期 | `2025-11-27` |
| 任務標題 | - | 必填 | 含純文字、`+專案`、`@情境` 等 | `+工作 撰寫報告 @電腦` |
| 專案標籤 | `+專案.子專案` | 可選 | 階層式，`.` 分隔 | `+國文作業.期末考` |
| 情境標籤 | `@情境` | 可選 | 上下文 | `@電腦` |
| 截止日期 | `due:` | 可選 | `YYYY-MM-DD` | `due:2025-12-01` |
| 隱藏日期 | `t:` | 可選 | 此日期前隱藏 | `t:2025-11-30` |
| 重複 | `rec:` | 可選 | 重複模式 | `rec:+1m` |
| 歷史 ID | `id:` | 可選 | 舊版 ID（v8.0 後可選輸出） | `id:hcadhi` |
| 詳細描述 | `desc:"..."` | 可選 | 多行文字，需轉義 | `desc:"這是\n描述"` |

### 6.2 專案過濾規則

- `+專案` — 匹配該專案及所有子專案
- `+專案.*` — `*` 匹配單一階層
- `+**.期末考` — `**` 匹配任意數量階層
- 可混合使用，如 `**.*期末考*`

### 6.3 重複模式

| 格式 | 含義 |
|------|------|
| `+1d` | 基於今日日期 +1 天 |
| `+1m` | 基於今日日期 +1 月 |
| `+1y` | 基於今日日期 +1 年 |
| `++1d` | 找下一個大於今日的日期（基於原 due），步進 1 天 |
| `++1m` | 同上，步進 1 月 |
| `++1y` | 同上，步進 1 年 |
| `1d`（無前綴） | 基於原 due 日期 +1 天 |

### 6.4 轉義規範 (desc 欄位)

- `"` → `\"`
- `\` → `\\\\`
- 換行符 → `\\n`

### 6.5 重複分隔符

描述欄位中的特殊標記：
- `---REPEAT-ABOVE---`：分隔線上方內容給新任務，下方保留在舊任務
- `---REPEAT-COPY---`：分隔線上方內容給新任務，上方+下方合併保留在舊任務

### 6.6 配置格式 (todo.rc)

```
key=value
```

複雜結構（List/Dict）以 JSON 字串儲存：
```
theme=solarized-light
confirm_delete=true
show_delete_button=false
sort_keys=[{"key": "pri", "asc": true}, {"key": "due", "asc": true}, {"key": "created", "asc": true}]
done_sort_keys=[{"key": "doneDate", "asc": false}, {"key": "", "asc": false}]
saved_filters=[{"name": "待辦工作", "q": "-work"}, {"name": "今日緊急", "q": "<tomorrow"}]
opacity=0.7
done_opacity=0.9
main_width=900
show_id=false
complete_children=true
```

### 6.7 任務定位機制（行號定位）

- 每個任務在陣列中的索引位置 = 其「行號」
- 所有操作（完成、刪除、編輯）都使用 array index
- UI 中用 `data-index` 屬性追蹤任務位置
- 舊版 `id:` 欄位仍會被解析存入 `t.legacyId`，輸出時可選是否寫入（透過 `show_id` 設定）

---

## 7. API 端點

### 7.1 列表

| 路徑 | 方法 | 參數 / Body | 回應 |
|------|------|-------------|------|
| `/` | GET | `?token=...`（選用） | index.html |
| `/api/read` | GET | `file={todo\|done\|config}` | `{"content":"..."}` 或 `{key:value}` |
| `/api/fileinfo` | GET | `file={todo\|done\|config}` | `{"mtime": timestamp}` |
| `/api/write` | POST | `{"file":"todo","content":"..."}` | `{"status":"ok"}` |

### 7.2 靜態檔案
任何非 API 路徑由 `SimpleHTTPRequestHandler.do_GET()` 處理，查詢 `./{path}`。

### 7.3 預檢請求
`OPTIONS` 方法回應 200，設置 CORS headers。

### 7.4 CORS 限制
只允許 `http://127.0.0.1:{PORT}`。

---

## 8. 認證與安全機制

### 8.1 Token 認證
- 伺服器啟動時生成隨機 `AUTH_TOKEN = secrets.token_hex(16)`
- URL 參數：`?token={AUTH_TOKEN}`（首次存取用）
- Cookie：種植 `auth={AUTH_TOKEN}`，`httponly=True`, `samesite=Strict`

### 8.2 驗證優先級
1. URL 參數 `?token=`（首次登入）
2. Cookie `auth`（後續請求）

### 8.3 CSRF 防護
POST 請求必須檢查：
- Origin 等於 `http://127.0.0.1:{PORT}`
- 或 Referer 以此開頭

### 8.4 訪問控制
認證失敗回傳 HTTP 403。

### 8.5 檔案安全
- 只允許讀寫 `FILES` dict 中定義的檔案（todo/done/config）
- 原子化寫入防止檔案損毀

---

## 9. 使用者介面設計

### 9.1 頁面佈局

```
┌──────────────────────────────────────────────────────────────────┐
│ [☕ 待辦筆記 (過濾時→☕ N)]           [+新] [🔃] [☀️] [⚙️] [🫣] [📋] │
├──────────────────────────────────────────────────────────────────┤
│ [🔍 搜尋...]                         [@] [+] [⭐]         │
├────────────────────────────────────────────────────────────┤
│ ┌────────────────────────────────────────────────────────┐ │
│ │ ☐ +工作 撰寫報告 @電腦  📅 2025-12-01  (A)  [✏️] [📅]  │ │
│ │   desc內容...                                         │ │
│ └────────────────────────────────────────────────────────┘ │
│ ┌────────────────────────────────────────────────────────┐ │
│ │ ☐ +學習 數學練習 @圖書館  📅 2025-12-05        [✏️] [📅]│ │
│ └────────────────────────────────────────────────────────┘ │
│ ...                                                       │
├────────────────────────────────────────────────────────────┤
│ ▼ 📦 已完成 (15項) (過濾時→3/8)                                    │
│   ☑ x 2025-11-20 報告完成 @電腦                           │
└────────────────────────────────────────────────────────────┘
```

### 9.2 視窗組件

| 組件 | 說明 |
|------|------|
| Header | 標題 + 功能按鈕列（新增/排序/今日/設定/隱藏/專案概覽） |
| Filter Bar | 搜尋輸入 + @/+/⭐ 快速按鈕，圓角藥丸形狀 |
| Task List | 未完成任務列表 |
| Done Section | 已完成任務可折疊區塊，預設收起 |
| Edit Modal | 任務編輯對話框（屬性/描述雙分頁） |
| Settings Modal | 設定對話框 |
| Floating Menu | 浮動選單（專案樹狀/標籤/排序/過濾器） |
| Project View Modal | 專案概覽視窗（階層式樹狀，含進度計數 (直屬完成/直屬總數)/(全部完成/全部總數)、跳轉按鈕、一鍵展開/收合、按專案名開關描述） |
| Back to Top | 右下角固定按鈕，滾動超過 300px 才顯示 |

### 9.3 Header 按鈕

| 按鈕 | 功能 |
|------|------|
| ➕ | 新增任務（編輯器） |
| 🔃 | 排序優先級（浮動選單） |
| ☀️ | 切換今日任務過濾 |
| ⚙️ | 設定視窗 |
| 🫣 | 顯示/隱藏隱藏任務（切換後變 👀） |
| 📋 | 開啟專案概覽視窗 |
| ✕ (filter bar) | 清空過濾欄 |
| @ | 插入上下文標籤選單 |
| + | 插入專案標籤選單（樹狀階層） |
| ⭐ | 常用過濾器選單 |

### 9.4 任務卡片

每項任務卡片包含：
- **Checkbox**：勾選完成 / 取消勾選復原
- **標題區**：顯示任務文字，+專案 和 @情境 用彩色高亮，可點擊加入過濾
- **日期標記**：標題與描述中的 `[YYYY-MM-DD]` / `[YYYY-MM-DD HH:MM]`（容忍括號內多餘空格，也支援裸日期）依本地日期分三色：未來（綠）、今日（主題色）、過去（紅）；滑鼠懸停時上方浮現「改為今天 / 改為現在的時間 / 指定日期…」操作
- **標籤列**：優先級標籤（紅色）+ 📅截止日 + ⏳隱藏日 + 🔄重複 + 其他
- **動作按鈕**：✏️ 編輯 / 📅 今日任務切換 / 🗑️ 刪除（可設定顯示）
- **描述區**：多行描述可展開/收起，超過 3.6 行顯示展開按鈕

### 9.5 今日任務圖示

| 圖示 | 含義 |
|------|------|
| ☀️ | 指派日期 = 今日 |
| 😱 | 指派日期 < 今日（過期） |
| 🌙 | 指派日期 > 今日（未來） |

### 9.6 主題系統

| 主題 | 說明 |
|------|------|
| `neutral` | 中性（米色底） |
| `dark` | 暗黑 |
| `girly` | 少女（粉色） |
| `solarized-light` | Solarized 亮色 |
| `nord-light` | Nord 亮色 |
| `sakura` | 櫻花粉（亮色） |
| `mint` | 薄荷綠（亮色） |
| `lavender` | 薰衣草紫（亮色） |
| `peach` | 蜜桃橙（亮色） |
| `cream` | 奶油白（亮色） |
| `sky` | 天空藍（亮色） |
| `matcha` | 抹茶綠（亮色） |
| `linen` | 亞麻灰（亮色） |
| `honey` | 蜂蜜金（亮色） |
| `seafoam` | 海沫藍（亮色） |
| `cloud` | 雲朵灰（亮色） |
| `coral` | 珊瑚粉（亮色） |
| `solarized-dark` | Solarized 暗色 |
| `nord-dark` | Nord 暗色 |
| `dim` | 柔暗灰（暗色） |
| `forest` | 森林夜（暗色） |
| `twilight` | 暮光紫（暗色） |
| `cocoa` | 可可棕（暗色） |

CSS 變數命名：`--bg-color`, `--text-color`, `--accent`, `--card-bg`, `--border`, `--tag-bg`, `--tag-text`, `--danger`, `--project-color`, `--context-color`, `--success`, `--font-main`, `--font-mono`, `--checkbox-size`, `--modal-bg`, `--opacity`, `--main-width`（以及 `--hidden-opacity`, `--done-opacity` 由 JavaScript 動態設定）

### 9.7 編輯視窗 (Edit Modal)

雙分頁設計：
- **任務屬性 (Properties) Tab**：
  - 多行標題輸入（可調大小，日期 token 同樣三色）+ 大小調整按鈕（▲/↺/▼）
  - 優先級下拉選單 (A-Z)
  - @☀️ 今日任務開關按鈕
  - 插入上下文 @ 按鈕
  - 插入專案 + 按鈕
  - 截止日期日期選擇器
  - 隱藏日期日期選擇器
  - 重複文字輸入
  - 完成日日期選擇器（僅已完成任務）
  - 上述日期欄位依本地日期顯示未來（綠）/ 今日（主題色）/ 過去（紅）
- **任務描述 (Description) Tab**：
  - 多行描述文本區（可調大小）+ 大小調整按鈕
  - 標題與描述文本區中的日期 token 即時顯示未來（綠）/ 今日（主題色）/ 過去（紅）；以透明 textarea 疊在同步的彩色覆蓋層上實作，游標、選取與捲動皆正常
  - 插入現在時間按鈕（使用裝置本地時區，格式 `[YYYY-MM-DD HH:MM]`）
  - 游標停駐於既有日期時，上方浮現「改為今天 / 改為現在的時間 / 指定日期…」操作；指定日期使用原生日期選擇器並保留原時刻
  - 插入重複分隔符按鈕（🔁 分隔符 / 🔁 複製）
  - 重新編號按鈕 🔢
- **底部按鈕**：保存並繼續 / 保存任務 / 儲存並完成任務 / 刪除任務

### 9.8 設定視窗

- 主題選擇下拉
- 刪除前確認開關
- 顯示刪除按鈕開關
- 顯示 ID 欄位開關
- 點擊任務欄位行為：添加到搜索欄 / 複製到剪貼簿
- 主界面寬度滑桿 (600-1500px)
- 隱藏任務透明度滑桿 (0.1-1.0)
- 已完成任務透明度滑桿 (0.1-1.0)
- todo.txt 最後修改時間顯示
- 同步提示文字（推薦 Syncthing / Rclone）

### 9.9 浮動選單

**排序選單：**
- 三分層排序：第1/2/3優先排序鍵（優先級/截止日/建立日/標題）+ 正序開關
- 已完成任務獨立排序設定

**專案選單：**
- 從現有任務提取所有 `+專案` 標籤
- 自動偵測為平攤式（無子層級）或階層式
- 階層式以樹狀顯示，可展開/收起子節點
- 支援「全部展開/摺疊」
- 底端有「+ 新項目」選項

**標籤選單：**
- 從現有任務提取所有 `@情境` 標籤
- 排除 `@☀️.` 今日任務標記
- 排序後顯示，點擊插入到輸入框

**常用過濾器選單：**
- 「+ 儲存當前過濾」按鈕
- 已儲存過濾器列表（點擊套用，✕ 刪除）

---

## 10. 前端功能模組

### 10.1 任務解析 (parseLines / parseLine)

`parseLines(text)` → 按行分割 → 每行呼叫 `parseLine`

`parseLine(line)` 解析順序：
1. 檢查 `x YYYY-MM-DD` 完成標記
2. 檢查 `(A-Z)` 優先級
3. 檢查 `YYYY-MM-DD` 建立日期
4. 尋找 `desc:"..."` 描述（含轉義處理）
5. 其餘部分按空白分割，辨識 `due:`/`rec:`/`id:`/`t:` 等 metadata
6. 其餘文字組成 `t.sub`

### 10.2 任務序列化 (stringifyTask)

輸出順序：
1. `x {doneDate}`（若已完成）
2. `{pri}`（若有）
3. `{created}`（若有）
4. `{sub}`
5. `due:{due}`（若有）
6. `t:{threshold}`（若有）
7. `rec:{rec}`（若有）
8. `id:{legacyId}`（若有且 show_id 開啟）
9. `desc:"{desc}"`（若有，含轉義）

### 10.3 過濾邏輯 (render)

過濾欄支援的語法：
- `+專案` 或 `+專案.子專案` — 專案過濾（含通配符 `*`/`**`）
- `@情境` — 情境過濾
- `<日期` — due 小於該日期
- `>日期` — due 大於該日期
- `<=日期` / `>=日期` — 含邊界的日期比較
- `pri=A` / `pri=A,C` / `pri=A-D` — 優先度精確/多選/範圍匹配
- `pri<C` / `pri>C` / `pri<=C` / `pri>=C` — 優先度大小比較（A 最大 Z 最小）
- `pri=!` — 無優先度任務
- `@☀️` — 今日任務過濾
- `today` — 自動取代為當天日期字串
- `tomorrow` — 自動取代為明天日期字串
- 純文字 — 搜尋標題+描述

過濾流程：
```
filterText → split by spaces → terms
每個 term 逐一檢查任務
term 若以 + 或 * 開頭 → matchProjectFilter
term 若為 <= 或 >= 開頭 → due 含邊界比較
term 若為 < 開頭 → due < 日期
term 若為 > 開頭 → due > 日期
term 若為 pri 開頭 → 優先度過濾（支援 = / <= / >= / < / >）
否則 → sub + desc 包含此文字（不分大小寫）
```

### 10.4 排序邏輯

```javascript
// 自訂排序
for (const s of config.sort_keys) {
    // 支援 pri, due, created, sub 欄位
    // pri: 無優先級排最後
    // due: 無截止日排最後（用 '9999-99-99'）
}
```

### 10.5 重複任務處理 (handleRecurrence)

當任務被完成且有 `rec:` 欄位時：
1. 解析 `rec:` 值，提取前綴（`+`/`++`/無）、數字、單位（d/m/y）
2. 根據前綴計算新的 due 日期
3. 若有 threshold，保持與 due 的相對距離
4. 處理描述中的分隔符（`---REPEAT-ABOVE---` / `---REPEAT-COPY---`）
5. 若有今日任務標記，根據新日期更新
6. 新的任務 push 到 tasks 陣列

### 10.6 排序選單初始化

三分層（第1/2/3優先順序），每個排序鍵可選：優先級/截止日/建立日/標題，附正序開關。
已完成任務增加「完成日」選項，預設按完成日倒序。

### 10.7 URL Cache Busting

靜態資源請求附加 `?v={APP_VERSION}` 參數，避免瀏覽器快取。

---

## 11. 任務操作流程

### 11.1 新增任務
```
1. 點擊 ➕ 按鈕
2. 開啟 Edit Modal（無 index，editingIndex = null）
3. 填寫標題、屬性、描述
4. 點擊「保存任務」或「保存並繼續」
5. saveTaskData() 構建新任務物件
   → tasks.push(newTask)
   → render()
   → sync()
6. 關閉視窗（saveTask）或保持開啟（saveTaskAndKeepOpen）
```

### 11.2 編輯任務
```
1. 點擊任務 ✏️ 按鈕
2. openEditModal(index, isDone)
3. 填入現有資料到表單
4. 修改後保存
5. list[editingIndex] = newTask（保留原 created 日期）
```

### 11.3 完成任務
```
1. 勾選 checkbox
2. completeTask(index)
3. t.done = true, t.doneDate = today
4. 處理重複（若有 rec）
5. doneTasks.unshift(t)
6. tasks.splice(index, 1)
7. render() + sync()
```

### 11.4 取消完成
```
1. 取消勾選 checkbox
2. uncompleteTask(index)
3. t.done = false, t.doneDate = null
4. tasks.push(t)
5. doneTasks.splice(index, 1)
6. render() + sync()
```

### 11.5 刪除任務
```
1. 點擊 🗑️ 按鈕
2. 若 confirm_delete = true → 彈出 confirm
3. tasks.splice(index, 1) 或 doneTasks.splice(index, 1)
4. render() + sync()
```

### 11.6 今日任務切換
```
1. 點擊任務旁的 📅 按鈕
2. toggleTaskToday(index)
3. 若已有 @☀️.YYYYMMDD → 移除
4. 若無 → 添加 @☀️.TODAY
5. render() + sync()
```

---

## 12. 今日任務功能

### 12.1 標記格式
使用特殊 context `@☀️.YYYYMMDD`（YYYYMMDD = 8 位數日期）

### 12.2 顯示規則
- 任務列表中自動隱藏 `@☀️.YYYYMMDD` 文字
- 今日的任務顯示 ☀️ 圖示
- 今日之前的任務顯示 😱 圖示（過期）

### 12.3 過濾
- Header 的 ☀️ 按鈕在過濾欄添加/移除 `@☀️`
- 過濾邏輯：`@☀️` 匹配所有含 `@☀️.YYYYMMDD` 的任務
- 未來日期的今日任務預設不顯示（除非 `showHiddenTasks = true`）

### 12.4 相關函數

| 函數 | 用途 |
|------|------|
| `toggleTodayFilter()` | 切換過濾欄 `@☀️` |
| `toggleTaskToday(index)` | 切換任務的今日標記 |
| `toggleTaskTodayInModal()` | 編輯器中切換 |
| `isTodayTask(task)` | 是否為今日任務 |
| `isOverdueTodayTask(task)` | 是否為過期今日任務 |

---

## 13. 國際化 i18n

### 13.1 語言資源檔
- `lang/zh-TW.json` — 繁體中文
- `lang/en.json` — 英文

### 13.2 語言偵測順序
```
1. localStorage.getItem('userLanguage')
2. navigator.language（以 zh 開頭 → zh-TW，en 開頭 → en）
3. 預設 zh-TW
```

### 13.3 翻譯更新規範
新增 UI 元素時：
1. 在 HTML 中使用 `id` 屬性
2. 在 `updateUI()` 添加更新邏輯
3. 在所有 `lang/*.json` 新增對應翻譯鍵值

### 13.4 文字獲取方式
```javascript
const getLang = (key, fallback = '') => {
    // 用點號路徑存取巢狀物件
    // 若無對應鍵值返回 fallback
};
```

### 13.5 語系鍵命名規範
- 使用 camelCase
- 語義清晰，與功能相關
- 支援巢狀結構（如 `modalTitles.addTask`, `formLabels.priority`）

---

## 14. 開發規則與慣例

### 14.1 程式碼風格
- **行內樣式**：CSS 全部在 `<style>` 中，無外部 CSS 檔案
- **無框架**：純原生 JavaScript，無 React/Vue/jQuery 等依賴
- **IIFE 封裝**：全部邏輯在 `App` 命名空間下
- **ES6+**：使用箭頭函數、`const`/`let`、模板字符串、`Promise.all` 等
- **DOM 快取**：使用 `DOM` 物件快取常用元素，避免重複 querySelector

### 14.2 Agent 工作規範
- 參考 `SPEC.md` 了解專案架構
- 施工後在 `worklog/` 留下工作總結報告
- 施工後檢查並更新 `SPEC.md`
- 忽略 `obsolete/` 和 `worklog/` 目錄（除非用戶指定）
- 注意人類可能手動修改程式碼

### 14.3 CSS 架構
- 使用 CSS 變數（`:root` + `data-theme` 屬性選擇器）
- 23 個主題透過變數切換
- 佈局字體：`--font-main`（無襯線中文字型）
- 程式碼字體：`--font-mono`（等寬中文字型）

### 14.4 重要常數

```javascript
const APP_VERSION = '7.2.2.1.5.0';
const REPEAT_SEPARATOR = '---REPEAT-ABOVE---';
const REPEAT_SEPARATOR_BOTH = '---REPEAT-COPY---';
const PORT = 6888;  // server.py 中定義
```

### 14.5 舊版相容性（v8.0 變更）
- 廢除父子任務階層（`p:` 欄位和樹狀結構）
- 改用階層式專案（`+專案.子專案`）
- 改用行號定位（array index），不再依賴 `id:` 欄位
- `show_id` 設定預設關閉（會「吞掉」舊 ID）
- 函數簽名從 `(id)` 改為 `(index, isDone?)`

---

## 附錄 A: 常用正則表達式

| 用途 | 正則 |
|------|------|
| 提取專案標籤 | `/(^|\s)\+(\S+)/g` |
| 提取情境標籤 | `/(^|\s)(@\S+)/g` |
| 識別今日標記 | `/@☀️\.\d{8}/g` |
| 解析重複格式 | `/^(\+{0,2})(\d+)([dmy])/` |
| 解析描述 | `/desc:"((?:[^"\\]|\\.)*)"/` |
| 優先級開頭 | `/^\([A-Z]\) /` |
| 日期開頭 | `/^(\d{4}-\d{2}-\d{2}) /` |

## 附錄 B: 關鍵檔案行數參考（當前版本）

| 檔案 | 行數 |
|------|------|
| `server.py` | 233 行 |
| `index.html` | 2316 行 |
| `lang/zh-TW.json` | 162 行 |
| `lang/en.json` | 161 行 |

---

*最後更新：2026-05-30*
*此文件由 AI 智能體根據 AGENT.md、SPEC.md、brief.md 及原始碼自動生成，用於給新的智能體完整復刻 HajimiTodotxt 專案。*
