# REWORK.md — HajimiTodotxt 復刻重構規格書

> 此文檔定義 HajimiTodotxt 在**自由技術棧**下的重構方案。功能與原版完全一致（或更完整），性能不低於原版，但實作技術不受限制。

---

## 目錄

1. [核心原則](#1-核心原則)
2. [技術棧選項與比較](#2-技術棧選項與比較)
3. [推薦實作方案](#3-推薦實作方案)
4. [資料層設計](#4-資料層設計)
5. [即時同步機制](#5-即時同步機制)
6. [前後端通訊](#6-前後端通訊)
7. [建置與部署](#7-建置與部署)
8. [重點功能實作指引](#8-重點功能實作指引)

---

## 1. 核心原則

### 1.1 必須保留的原版特性

| 特性 | 原因 |
|------|------|
| 原子化寫入 | 防止檔案損毀 |
| 行號定位 | 簡化資料模型，無需 ID 維護 |
| 純文字儲存格式 (*.txt) | Unix 哲學、與外部工具互操作 |
| todo.rc 配置系統 | 使用者自訂 |
| 雙檔案分離 (todo + done) | 簡單明確 |
| 今日任務 `@☀️.YYYYMMDD` 格式 | 已有資料相容性 |
| 階層式專案過濾（`*`/`**` 通配符） | 相容現有資料 |
| Cookie/Token 認證 | 區域網路安全 |
| 主題系統（23 主題） | 使用者體驗 |
| 國際化 (zh-TW / en) | 多語言支援 |

### 1.2 可自由選擇的項目

| 項目 | 說明 |
|------|------|
| 語言／框架 | 任何通用程式語言及網頁框架 |
| 前端架構 | SPA / SSR / Islands Architecture 均可 |
| 後端 runtime | 任何 HTTP server 實作 |
| 資料庫 | 純文字 / SQLite / 其他嵌入式資料庫 |
| 建置工具 | Vite / esbuild / Webpack / 無建置 |
| 部署方式 | 單一二進位 / Docker / 純腳本 |
| 附加功能 | 在維持核心功能前提下自由擴充 |

### 1.3 性能目標

| 指標 | 目標 | 原版參考 |
|------|------|----------|
| 冷啟動至可服務 | < 500ms | ~1-2s (Python) |
| 任務列表渲染 (10,000 項) | < 100ms | ~500ms+ (未經最佳化) |
| API 回應時間 (p50) | < 5ms | ~2-5ms (Python, 本地檔案 I/O) |
| 記憶體使用 (閒置) | < 50MB | ~20-30MB (Python) |
| 二進位/產物大小 | < 20MB | N/A (Python 腳本) |
| 同步寫入延遲 | < 10ms | ~2-5ms (原子化 os.replace) |

---

## 2. 技術棧選項與比較

### 2.1 後端選項

| 方案 | 語言 | 啟動速度 | 單二進位 | 效能 | 生態 | 備註 |
|------|------|----------|----------|------|------|------|
| **Go** | Go | <10ms | ✅ | 極佳 | 充足 | **強烈推薦**，標準庫 HTTP server 品質極高，單檔部署 |
| **Rust** | Rust | <5ms | ✅ | 極致 | 良好 | 效能最佳，但開發速度較慢 |
| **FastAPI** | Python | ~300ms | ❌ | 佳 (ASGI) | 豐富 | 最接近原版，但需 Python runtime |
| **Bun** | TS/JS | <50ms | ✅ | 佳 | 良好 | 前後端統一語言，快速迭代 |
| **Node.js** | TS/JS | ~200ms | ❌ (pkg 可打包) | 佳 | 極豐富 | 成熟穩定 |
| **Deno** | TS/JS | <50ms | ✅ | 佳 | 中等 | 安全優先 |
| **Nim** | Nim | <5ms | ✅ | 極佳 | 較少 | 語法類似 Python，效能接近 C |
| **Zig** | Zig | <5ms | ✅ | 極致 | 較少 | 底層控制，但開發成本高 |

### 2.2 前端選項

| 方案 | 框架 | 產物大小 | 渲染效能 | 開發體驗 | 備註 |
|------|------|----------|----------|----------|------|
| **Vanilla + Vite** | 無 | 最小 | 極佳 | 良好 | **推薦**，延續原版精神但享受現代工具鏈 |
| **Svelte 5** | Svelte | 小 | 極佳 | 極佳 | 編譯型框架，產物極小，無虛擬 DOM 開銷 |
| **SolidJS** | Solid | 小 | 極致 | 佳 | 細粒度響應式，無虛擬 DOM |
| **Preact** | Preact | 3KB | 極佳 | 佳 | React 相容 API，體積極小 |
| **React** | React | ~40KB | 佳 | 極佳 | 生態最大，但體積與複雜度較高 |
| **Vue 3** | Vue | ~30KB | 佳 | 極佳 | 漸進式，生態豐富 |
| **HTMX** | 無 | ~10KB | 極佳 | 佳 | 伺服器渲染 + hypermedia，適合 SSR 方案 |
| **Alpine.js** | 無 | ~10KB | 佳 | 佳 | 類似 Vue 但更輕量，適合在 HTML 中直接使用 |

### 2.3 儲存層選項

| 方案 | 類型 | 效能 | 相容 todo.txt | 備註 |
|------|------|------|---------------|------|
| **純文字檔案** | 檔案 | 普通 | ✅ 原生 | 延續原版，外部工具可直接編輯 |
| **SQLite** | 嵌入式 DB | 極佳 | ⚠️ 需轉換層 | 支援交易、索引、全文搜尋 |
| **純文字 + Git** | 檔案 + VCS | 普通 | ✅ | 自動版本控制，可 diff/rollback |
| **RocksDB/LMDB** | KV 儲存 | 極致 | ❌ | 僅適合極度高效能場景，失去互通性 |

---

## 3. 推薦實作方案

### 3.1 方案 A：輕量進化（推薦）

最小的開發成本，最大的效能收益。

| 層級 | 技術選擇 | 理由 |
|------|----------|------|
| 前端 | **Vanilla JS + Vite** | 無框架心智負擔，完整沿用原版邏輯，Vite 提供 HMR、極速建置 |
| 後端 | **Go** (`net/http`) | 單一二進位部署，啟動 <10ms，效能極高，標準庫 HTTP 品質一流 |
| 儲存 | **純文字檔案** | 完全相容 todo.txt，外部工具可直接編輯 |
| Schema | 沿用原版 | 相容現有資料，無需遷移 |
| 建置 | `go build` + `vite build` | 靜態資源嵌入 Go 二進位 → 單一執行檔 |

**前後端整合方式**：
- Go 後端使用 `embed` 將 Vite 產物（`dist/`）嵌入二進位
- 最終產物：**單一執行檔**，包含所有前端資源
- 啟動指令：`./hajimi-todo`，自動在 `6888` port 啟動

### 3.2 方案 B：極致效能

| 層級 | 技術選擇 |
|------|----------|
| 前端 | **SolidJS + Vite** |
| 後端 | **Rust** (`axum` 或 `actix-web`) |
| 儲存 | **純文字檔案**（配合 `inotify`/`kqueue` 檔案監視） |
| 建置 | `cargo build --release` + `vite build` → 單一二進位 |

### 3.3 方案 C：全端統一語言

| 層級 | 技術選擇 |
|------|----------|
| 前端 | **Svelte 5 + Vite** |
| 後端 | **Bun** (`Bun.serve`) |
| 儲存 | **純文字檔案 + Bun.file** |
| 建置 | `bun build --compile` → 單一二進位 |

---

## 4. 資料層設計

### 4.1 資料模型（核心介面）

不論實作語言為何，保留此資料結構：

```typescript
// TypeScript 描述 — 與原版完全對應
interface Task {
  sub: string;        // 任務標題（含 +project @context 等）
  desc?: string;      // 詳細描述（多行，未轉義原始格式）
  done: boolean;      // 是否完成
  doneDate?: string;  // 完成日 YYYY-MM-DD（done=true 時）
  pri?: string;       // 優先級 "(A)"-"(Z)"
  created?: string;   // 建立日 YYYY-MM-DD
  due?: string;       // 截止日 YYYY-MM-DD
  threshold?: string; // 隱藏日 YYYY-MM-DD（t:）
  rec?: string;       // 重複模式（rec: 後續部分）
  legacyId?: string;  // 舊版 id: 欄位（保留向後相容）
}
```

### 4.2 檔案 I/O 模組（抽象介面）

```
interface FileIO {
  readTodo(): Promise<string>      // 讀取 todo.txt 全文
  readDone(): Promise<string>      // 讀取 done.txt 全文
  readConfig(): Promise<Config>    // 讀取 todo.rc 並解析
  writeTodo(content: string): Promise<void>   // 原子化寫入 todo.txt
  writeDone(content: string): Promise<void>   // 原子化寫入 done.txt
  writeConfig(config: Config): Promise<void>  // 寫入 todo.rc
  getFileInfo(file: string): Promise<{mtime: number}>  // 檔案修改時間
}
```

### 4.3 原子化寫入（各語言實作）

```go
// Go 版本
func atomicWrite(filename string, content string) error {
    tmpFile := filename + ".tmp"
    if err := os.WriteFile(tmpFile, []byte(content), 0644); err != nil {
        return err
    }
    return os.Rename(tmpFile, filename)  // POSIX 原子操作
}
```

```rust
// Rust 版本
fn atomic_write(filename: &str, content: &str) -> std::io::Result<()> {
    let tmp = format!("{}.tmp", filename);
    std::fs::write(&tmp, content)?;
    std::fs::rename(&tmp, filename)?;  // POSIX 原子操作
    Ok(())
}
```

### 4.4 配置解析（各語言實作）

````go
// Go
type Config struct {
    Theme           string   `json:"theme"`
    ConfirmDelete   bool     `json:"confirm_delete"`
    ShowDeleteBtn   bool     `json:"show_delete_button"`
    SortKeys        []SortRule `json:"sort_keys"`
    DoneSortKeys    []SortRule `json:"done_sort_keys"`
    SavedFilters    []Filter `json:"saved_filters"`
    Opacity         float64  `json:"opacity"`
    DoneOpacity     float64  `json:"done_opacity"`
    MainWidth       int      `json:"main_width"`
    ShowID          bool     `json:"show_id"`
    CompleteChildren bool   `json:"complete_children"`
}

// 解析 todo.rc：
// 每行 key=value
// 嘗試 json.Unmarshal value
// 若失敗則保留原始字串
````

---

## 5. 即時同步機制

原版需手動刷新或等 sync() 觸發。重構版本可添加：

### 5.1 可選方案

| 方案 | 技術 | 複雜度 | 說明 |
|------|------|--------|------|
| **SSE** (Server-Sent Events) | `EventSource` | 低 | 單向即時推送，足夠本機使用 |
| **WebSocket** | `WebSocket` | 中 | 雙向，更強大但非必要 |
| **File Watcher** | `fsnotify`(Go) / `inotify` | 低 | 偵測外部編輯（如 vim 直接改 todo.txt） |
| **Polling** | `setInterval` + `fileinfo` API | 極低 | 最簡單，1-3 秒輪詢即可 |

### 5.2 推薦：SSE + File Watcher

```
1. 前端連線 SSE: new EventSource('/api/events')
2. 後端監視 todo.txt / done.txt 檔案變更（使用 fsnotify/inotify）
3. 檔案變更時透過 SSE 推送 {type: "fileChanged", file: "todo"}
4. 前端收到後自動重新讀取並渲染
```

此方案可讓**多個瀏覽器分頁**同時反映變更，且支援**外部編輯器**直接修改檔案後自動更新 UI。

---

## 6. 前後端通訊

### 6.1 API 端點（與原版相容，可擴充）

| 方法 | 路徑 | 說明 | 變更 |
|------|------|------|------|
| GET | `/api/read?file={todo\|done\|config}` | 讀取 | 不變 |
| GET | `/api/fileinfo?file={todo\|done\|config}` | 檔案資訊 | 不變 |
| POST | `/api/write` | 寫入 | 不變 |
| GET | `/api/events` | SSE 即時推送 | **新增** |
| GET | `/api/exists` | 檢查檔案是否存在 | **可選新增** |
| DELETE | `/api/task` | 直接操作任務（更 RESTful） | **可選新增** |

### 6.2 靜態資源服務

```
原始版本：SimpleHTTPRequestHandler 自動服務
重構版本：將前端產物嵌入二進位

Go embed 範例：
//go:embed dist/*
var staticFiles embed.FS

http.Handle("/", http.FileServer(http.FS(staticFiles)))
```

---

## 7. 建置與部署

### 7.1 建置流程（方案 A：Go + Vanilla/Vite）

```bash
# 開發模式
cd frontend && vite dev          # 前端 HMR 伺服器 :5173
cd backend && go run .           # Go 後端 :6888（代理前端請求）

# 生產建置
cd frontend && vite build        # 產生 dist/
cd backend && go build -o hajimi-todo .  # 嵌入 dist/，產生單一執行檔

# 運行
./hajimi-todo                    # 單一檔案，一切就緒
```

### 7.2 產物結構

```
hajimi-todo (單一執行檔)
├── 內嵌的前端靜態資源 (dist/)
├── HTTP 伺服器 (net/http)
├── 檔案 I/O (os.ReadFile / os.WriteFile)
├── 認證 (crypto/rand token)
└── 檔案監視 (fsnotify)
```

### 7.3 Docker 支援（選用）

```dockerfile
FROM alpine:latest
COPY hajimi-todo /usr/local/bin/hajimi-todo
EXPOSE 6888
VOLUME ["/data"]
WORKDIR /data
ENTRYPOINT ["hajimi-todo"]
```

---

## 8. 重點功能實作指引

### 8.1 認證系統（各語言實作）

核心邏輯（與原版完全相同）：

```
1. 啟動時產生 random token（32 hex chars）
2. 首次請求：URL 帶 ?token=xxx → 驗證成功 → 種植 Cookie
3. 後續請求：讀取 Cookie auth 值比對 token
4. POST 除檢查 Cookie 外，額外檢查 Origin/Referer
5. 靜態資源請求也需要驗證（與原版一致）
```

### 8.2 今日任務（完全沿用原版規格）

- 格式：`@☀️.YYYYMMDD`
- 顯示規則：任務列表中隱藏完整文字，僅顯示 ☀️ / 😱 / 🌙 圖示
- 過濾規則：過濾 `@☀️`（不含日期）= 匹配所有今日任務
- 排序支援：可依 `@☀️.日期` 排序

### 8.3 階層式專案過濾（完全沿用原版規格）

- `+專案` → 匹配該專案及所有子專案
- `+專案.*` → `*` 匹配單一階層
- `+**.期末考` → `**` 匹配任意階層
- 實作提示：使用帶回溯的遞迴模式匹配

### 8.4 重複任務（完全沿用原版規格）

- 三種前綴：無前綴（基於原 due）、`+`（基於今日）、`++`（跳躍至未來）
- 重複描述分隔符：`---REPEAT-ABOVE---` 和 `---REPEAT-COPY---`
- 計算邏輯需精確一致，確保舊資料相容

### 8.4.1 任務內日期標記與快速修改

- 識別標題/描述中的 `[YYYY-MM-DD]`、`[YYYY-MM-DD HH:MM]`（容忍括號內空格，支援裸日期與 `T` 分隔）
- 依本地日期分三色：未來、今日、過去
- 懸停日期或游標停駐時，上方浮現「改為今天」（純日期）、「改為現在的時間」（本地日期 + 時分）與「指定日期…」（原生日期選擇器）
- 指定日期只替換日期部分；原本若含時刻則保留時刻
- 編輯視窗的截止日／隱藏至／完成日輸入框依本地日期套用未來／今日／過去三色
- 標題與描述輸入框以覆蓋層同步顯示相同的三色日期；文字仍由原生 textarea 持有，覆蓋層只負責顯示與捲動同步
- 編輯視窗底部提供「儲存並完成任務」：先保存本次編輯，再完成任務並觸發重複任務規則
- 所有「現在時間」與明日日期計算均使用裝置本地時區，不可使用 UTC `toISOString()` 取日期

### 8.5 主題系統（可保留原版或改用更現代方案）

保留原版 23 主題 + CSS 變數方案，或改為：
- CSS 自訂屬性的系統 + JavaScript 動態載入
- 或 SCSS/Less 變數在編譯時生成
- 或支援使用者自訂主題（透過 todo.rc 或 JSON 匯入）

### 8.6 效能最佳化建議

| 技術 | 適用場景 | 預期提升 |
|------|----------|----------|
| 虛擬捲軸 (Virtual Scroll) | 任務 > 1000 項 | DOM 節點從 N→~20 |
| 文字搜尋索引 | 頻繁文字過濾 | O(n) → O(log n) |
| requestAnimationFrame 批量渲染 | 大量任務操作 | 避免 layout thrashing |
| Web Worker | 解析/序列化大型文字 | 不阻塞 UI 執行緒 |
| HTTP/2 Server Push | 靜態資源載入 | 減少 round trip |
| 連接池（資料庫方案） | 高併發讀寫 | 減少檔案開啟次數 |

### 8.7 可選增強功能（不影響核心）

| 功能 | 說明 | 優先級 |
|------|------|--------|
| PWA / 離線支援 | Service Worker 快取，可離線操作 | 中 |
| 鍵盤快捷鍵 | `n` 新增, `/` 搜尋, `Esc` 關閉等 | 低 |
| 拖曳排序 | 直接拖曳任務調整順序 | 低 |
| 全域快速搜尋 | `Ctrl+P` 風格命令面板 | 低 |
| Markdown 渲染 | 描述欄位支援 Markdown | 低 |
| 統計儀表板 | 完成率、趨勢圖表 | 低 |
| 自動備份 | 定時備份 `.txt` 檔案 | 低 |
| WebDAV 同步 | 內建 WebDAV 用戶端 | 低（原版推薦 Syncthing） |

---

## 附錄 A：各語言啟動範例

### Go (方案 A)

```go
package main

import (
    "crypto/rand"
    "embed"
    "encoding/hex"
    "encoding/json"
    "io/fs"
    "log"
    "net/http"
    "os"
    "strconv"
)

//go:embed dist/*
var staticFiles embed.FS

var authToken string

func main() {
    tokenBytes := make([]byte, 16)
    rand.Read(tokenBytes)
    authToken = hex.EncodeToString(tokenBytes)

    port := 6888
    if p := os.Getenv("PORT"); p != "" {
        port, _ = strconv.Atoi(p)
    }

    mux := http.NewServeMux()
    
    subFS, _ := fs.Sub(staticFiles, "dist")
    fileServer := http.FileServer(http.FS(subFS))
    
    mux.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
        // 1. Auth check (skip for static files via valid cookie)
        // 2. Serve index.html for "/"
        // 3. API routing
        fileServer.ServeHTTP(w, r)
    })
    
    log.Printf("★ HajimiTodotxt 啟動於 http://127.0.0.1:%d/?token=%s", port, authToken)
    log.Fatal(http.ListenAndServe("127.0.0.1:"+strconv.Itoa(port), mux))
}
```

### Rust (方案 B)

```rust
use axum::{
    routing::{get, post},
    Router,
};
use std::sync::Arc;
use tokio::sync::RwLock;

struct AppState {
    auth_token: String,
}

#[tokio::main]
async fn main() {
    let token = hex::encode(rand::thread_rng().gen::<[u8; 16]>());
    let state = Arc::new(AppState { auth_token: token });

    let app = Router::new()
        .route("/api/read", get(api_read))
        .route("/api/write", post(api_write))
        .route("/api/fileinfo", get(api_fileinfo))
        .with_state(state);

    let addr = "127.0.0.1:6888";
    println!("★ HajimiTodotxt 啟動於 http://{}/?token={}", addr, token);
    axum::Server::bind(&addr.parse().unwrap())
        .serve(app.into_make_service())
        .await
        .unwrap();
}
```

### Bun (方案 C)

```typescript
import { serve, file } from "bun";

const AUTH_TOKEN = crypto.randomUUID().replace(/-/g, "");

serve({
  port: 6888,
  async fetch(req) {
    const url = new URL(req.url);
    // Auth check, API routing, static file serving...
  },
});

console.log(`★ HajimiTodotxt 啟動於 http://127.0.0.1:6888/?token=${AUTH_TOKEN}`);
```

---

## 附錄 B：檔案監視 (File Watcher) 實作

### Go (fsnotify)

```go
import "github.com/fsnotify/fsnotify"

func watchFile(filename string, onChange func()) error {
    watcher, _ := fsnotify.NewWatcher()
    defer watcher.Close()
    
    watcher.Add(filename)
    for event := range watcher.Events {
        if event.Op&fsnotify.Write == fsnotify.Write {
            onChange()
        }
    }
    return nil
}

// 使用 SSE 推送變更通知
// 每個連線註冊一個 chan，檔案變更時廣播
```

### Rust (notify)

```rust
use notify::{Watcher, RecursiveMode, watcher};
use std::sync::mpsc::channel;

fn watch_file(path: &str, callback: impl Fn() + Send + 'static) {
    let (tx, rx) = channel();
    let mut watcher = watcher(tx, Duration::from_secs(1)).unwrap();
    watcher.watch(path, RecursiveMode::NonRecursive).unwrap();
    
    loop {
        match rx.recv() {
            Ok(_) => callback(),
            Err(_) => break,
        }
    }
}
```

---

*此文件由 AI 根據 HajimiTodotxt 原始程式碼與 SPEC.md 生成。*

*最後更新：2026-05-13*
