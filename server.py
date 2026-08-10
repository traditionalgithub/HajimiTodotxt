import http.server
import socketserver
import json
import os
import sys
import secrets
import hashlib
from http import cookies
from urllib.parse import urlparse, parse_qs

# 配置
PORT = 6888
FILES = {"todo": "todo.txt", "done": "done.txt", "config": "todo.rc"}
# 生成本次運行的隨機 Token (安全核心)
AUTH_TOKEN = secrets.token_hex(16)

# 初始化文件
for f in FILES.values():
    if not os.path.exists(f):
        open(f, "a").close()


class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


class SecureTodoHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def _set_cors_headers(self):
        """設置 CORS 防護，只允許本機訪問"""
        self.send_header("Access-Control-Allow-Origin", f"http://127.0.0.1:{PORT}")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def check_auth(self):
        """驗證權限：檢查 Cookie 或 URL 中的 Token"""
        # 1. 如果是靜態資源 (css/js/favicon) 且來自本機 Referer，適度放行 (可選，這裡嚴格處理)

        # 2. 檢查 URL 參數是否包含正確的 Token (用於首次登入)
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)
        if "token" in query and query["token"][0] == AUTH_TOKEN:
            return True, True  # (Auth Success, Is Login Request)

        # 3. 檢查 Cookie
        if "Cookie" in self.headers:
            c = cookies.SimpleCookie(self.headers["Cookie"])
            if "auth" in c and c["auth"].value == AUTH_TOKEN:
                return True, False

        return False, False

    def do_OPTIONS(self):
        """處理預檢請求"""
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()

    def do_GET(self):
        # --- 安全檢查 ---
        is_auth, is_login_req = self.check_auth()

        if not is_auth:
            # 驗證失敗，返回 403
            self.send_response(403)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(
                b"<h1>403 Forbidden</h1><p>Missing or invalid token. Check your terminal for the login URL.</p>"
            )
            return
        # ----------------

        parsed = urlparse(self.path)

        if parsed.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self._set_cors_headers()
            # 如果是帶 Token 的登入請求，種植 Cookie
            if is_login_req:
                c = cookies.SimpleCookie()
                c["auth"] = AUTH_TOKEN
                c["auth"]["path"] = "/"
                c["auth"]["httponly"] = True  # 防止 JS 讀取，增加安全性
                c["auth"]["samesite"] = "Strict"  # 防止 CSRF
                self.send_header("Set-Cookie", c.output(header="").strip())

            self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
            self.end_headers()

            try:
                with open("index.html", "rb") as f:
                    self.wfile.write(f.read())
            except FileNotFoundError:
                self.wfile.write(b"index.html not found.")
            return

        # API 讀取邏輯 (與舊版相同，但加上了權限檢查)
        if parsed.path == "/api/read":
            query = parse_qs(parsed.query)
            file_key = query.get("file", ["todo"])[0]
            filename = FILES.get(file_key, FILES["todo"])

            try:
                with open(filename, "r", encoding="utf-8") as f:
                    content = f.read()

                if file_key == "config":
                    config = {}
                    for line in content.splitlines():
                        if "=" in line:
                            k, v = line.split("=", 1)
                            k, v = k.strip(), v.strip()
                            try:
                                config[k] = json.loads(v)
                            except:
                                config[k] = v
                    data = config
                else:
                    data = {"content": content}

                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self._set_cors_headers()  # Add CORS
                self.send_header("Cache-Control", "no-store")
                self.end_headers()
                self.wfile.write(json.dumps(data).encode("utf-8"))
            except Exception as e:
                self.send_error(500, f"Read error: {str(e)}")
            return

        # API 獲取文件資訊 (修改時間)
        if parsed.path == "/api/fileinfo":
            query = parse_qs(parsed.query)
            file_key = query.get("file", ["todo"])[0]
            filename = FILES.get(file_key, FILES["todo"])
            try:
                mtime = os.path.getmtime(filename)
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self._set_cors_headers()
                self.send_header("Cache-Control", "no-store")
                self.end_headers()
                self.wfile.write(json.dumps({"mtime": mtime}).encode("utf-8"))
            except Exception as e:
                self.send_error(500, f"File info error: {str(e)}")
            return

        # 靜態文件或其他
        super().do_GET()

    def do_POST(self):
        # --- 安全檢查 ---
        # POST 請求必須依賴 Cookie，且檢查 Origin/Referer 防止 CSRF
        is_auth, _ = self.check_auth()

        # CSRF 檢查：確保請求來自本機
        origin = self.headers.get("Origin")
        referer = self.headers.get("Referer")
        valid_origin = f"http://127.0.0.1:{PORT}"
        is_csrf_safe = (origin == valid_origin) or (
            referer and referer.startswith(valid_origin)
        )

        if not is_auth or not is_csrf_safe:
            self.send_response(403)
            self.end_headers()
            print(f"[WARN] Blocked unauthorized POST from {self.client_address}")
            return
        # ----------------

        parsed = urlparse(self.path)
        if "Content-Length" not in self.headers:
            self.send_error(400)
            return

        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)

        if parsed.path == "/api/write":
            try:
                req_data = json.loads(post_data.decode("utf-8"))
                file_key = req_data.get("file", "todo")
                filename = FILES.get(file_key, FILES["todo"])
                content_to_write = req_data.get("content", "")

                if file_key == "config":
                    config_obj = content_to_write
                    lines = []
                    for k, v in config_obj.items():
                        if isinstance(v, (dict, list)):
                            v = json.dumps(v, ensure_ascii=False)
                        lines.append(f"{k}={v}")
                    content_to_write = "\n".join(lines)

                # Atomic write: write to temp file first, then rename
                temp_filename = filename + ".tmp"
                with open(temp_filename, "w", encoding="utf-8") as f:
                    f.write(content_to_write)
                os.replace(temp_filename, filename)

                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self._set_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps({"status": "ok"}).encode("utf-8"))
                sys.stdout.write(".")
                sys.stdout.flush()
            except Exception as e:
                print(f"\n[ERROR] Write failed: {e}", file=sys.stderr)
                self.send_error(500, f"Write error: {str(e)}")
            return

        self.send_error(404)


if __name__ == "__main__":
    try:
        if not os.path.exists("index.html"):
            print("注意：index.html 不存在。")

        with ReusableTCPServer(("127.0.0.1", PORT), SecureTodoHandler) as httpd:
            print("=" * 60)
            print(f"★ HajimiTodotxt Backend Service Launched!")
            print(f"★ 安全驗證鏈接 (請複製並在瀏覽器打開):")
            print(f"   http://127.0.0.1:{PORT}/?token={AUTH_TOKEN}")
            print("=" * 60)
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n伺服器已關閉。")
