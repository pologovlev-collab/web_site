from http.server import BaseHTTPRequestHandler, HTTPServer

# Текущий статус хранится здесь — в памяти сервера
current_status = "off"

def build_page(status):
    is_on = status == "on"
    color = "#00ff88" if is_on else "#ff4455"
    label = "ON" if is_on else "OFF"
    glow = "0 0 40px #00ff8888, 0 0 80px #00ff8844" if is_on else "0 0 40px #ff445588, 0 0 80px #ff445544"

    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Status Monitor</title>
  <link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

    body {{
      background: #0a0a0f;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      font-family: 'Share Tech Mono', monospace;
      overflow: hidden;
    }}

    /* Сетка на фоне */
    body::before {{
      content: '';
      position: fixed;
      inset: 0;
      background-image:
        linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
      background-size: 40px 40px;
      pointer-events: none;
    }}

    .card {{
      position: relative;
      border: 1px solid {color}44;
      border-radius: 4px;
      padding: 60px 80px;
      text-align: center;
      background: #0f0f1a;
      box-shadow: {glow};
      transition: all 0.4s ease;
    }}

    .label {{
      color: #ffffff44;
      font-size: 11px;
      letter-spacing: 6px;
      text-transform: uppercase;
      margin-bottom: 24px;
    }}

    .status {{
      font-size: 96px;
      font-weight: 400;
      color: {color};
      letter-spacing: 12px;
      text-shadow: {glow};
      animation: pulse 2s ease-in-out infinite;
    }}

    @keyframes pulse {{
      0%, 100% {{ opacity: 1; }}
      50% {{ opacity: 0.75; }}
    }}

    .divider {{
      width: 100%;
      height: 1px;
      background: {color}33;
      margin: 32px 0;
    }}

    .controls {{
      display: flex;
      gap: 16px;
      justify-content: center;
    }}

    a {{
      text-decoration: none;
      font-family: 'Share Tech Mono', monospace;
      font-size: 13px;
      letter-spacing: 3px;
      padding: 10px 24px;
      border: 1px solid;
      border-radius: 2px;
      transition: all 0.2s;
      cursor: pointer;
    }}

    .btn-on {{
      color: #00ff88;
      border-color: #00ff8866;
    }}
    .btn-on:hover {{
      background: #00ff8822;
      box-shadow: 0 0 16px #00ff8844;
    }}

    .btn-off {{
      color: #ff4455;
      border-color: #ff445566;
    }}
    .btn-off:hover {{
      background: #ff445522;
      box-shadow: 0 0 16px #ff445544;
    }}

    .footer {{
      margin-top: 32px;
      color: #ffffff22;
      font-size: 11px;
      letter-spacing: 2px;
    }}
  </style>
</head>
<body>
  <div class="card">
    <div class="label">system status</div>
    <div class="status">{label}</div>
    <div class="divider"></div>
    <div class="controls">
      <a href="/on" class="btn-on">[ ON ]</a>
      <a href="/off" class="btn-off">[ OFF ]</a>
    </div>
  </div>
  <div class="footer">GET /on &nbsp;·&nbsp; GET /off &nbsp;·&nbsp; GET /status</div>
</body>
</html>"""


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        global current_status

        if self.path == "/on":
            current_status = "on"
            self._redirect("/")

        elif self.path == "/off":
            current_status = "off"
            self._redirect("/")

        elif self.path == "/status":
            self._respond(200, "text/plain", current_status)

        else:
            # Главная страница (и любой другой путь)
            html = build_page(current_status)
            self._respond(200, "text/html", html)

    def _redirect(self, location):
        self.send_response(302)
        self.send_header("Location", location)
        self.end_headers()

    def _respond(self, code, content_type, body):
        encoded = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", f"{content_type}; charset=utf-8")
        self.send_header("Content-Length", len(encoded))
        self.end_headers()
        self.wfile.write(encoded)

    # Отключаем стандартные логи (можно убрать эту строку, если хочешь видеть логи)
    def log_message(self, format, *args):
        print(f"  {self.address_string()} → {args[0]}")


if __name__ == "__main__":
    PORT = 8080
    server = HTTPServer(("", PORT), Handler)
    print(f"Сервер запущен: http://localhost:{PORT}")
    print("Ctrl+C — остановить")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nСервер остановлен.")
