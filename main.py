import os
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer

# Путь к папке с файлами
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


class MyServer(BaseHTTPRequestHandler):

    def do_GET(self) -> None:
        """Обработка GET‑запросов (отдача файлов)"""
        print(f"[GET] Запрос: {self.path}")

        # Определяем путь к файлу
        if self.path == "/":
            filepath = os.path.join(CURRENT_DIR, "html", "contacts.html")
        elif self.path == "/favicon.ico":  # ← Добавляем обработку favicon
            filepath = os.path.join(CURRENT_DIR, "img", "favicon.ico")
        elif self.path.startswith("/css/"):
            filepath = os.path.join(CURRENT_DIR, "css", self.path[5:])
        elif self.path.startswith("/js/"):
            filepath = os.path.join(CURRENT_DIR, "js", self.path[4:])
        elif self.path.startswith("/img/"):
            filepath = os.path.join(CURRENT_DIR, "img", self.path[5:])
        else:
            filepath = os.path.join(CURRENT_DIR, "html", self.path.lstrip("/"))

        # Определяем Content-Type
        if filepath.endswith(".css"):
            content_type = "text/css"
        elif filepath.endswith((".js", ".json")):
            content_type = "application/javascript"
        elif filepath.endswith((".png", ".jpg", ".jpeg", ".gif")):
            content_type = "image/jpeg"
        elif filepath.endswith(".ico"):
            content_type = "image/x-icon"  # ← Правильный тип для .ico
        else:
            content_type = "text/html"

        try:
            # Открываем файл
            if "image" in content_type:
                with open(filepath, "rb") as f:
                    content = f.read()
            else:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read().encode("utf-8")

            self.send_response(200)
            self.send_header("Content-type", content_type)
            self.end_headers()
            self.wfile.write(content)

        except FileNotFoundError:
            self.send_error(404, "File not found")  # ← Только латиница!
        except Exception as e:
            self.send_error(500, "Internal server error")


    def do_POST(self) -> None:
        """Обработка POST‑запросов и вывод в консоль"""
        print(f"[POST] Получен запрос: {self.path}")
        # print(f"[HEADERS] {dict(self.headers)}")  # Отладка

        if self.path != '/submit':
            print(f"[404] Неизвестный endpoint: {self.path}")
            self.send_error(404, "Endpoint not found")
            return

        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            parsed_data = urllib.parse.parse_qs(post_data)

            print("\n" + "=" * 40)
            print("ПОЛУЧЕНЫ ДАННЫЕ ФОРМЫ")
            print("=" * 40)
            for key, values in parsed_data.items():
                print(f"{key}: {values[0]}")
            print("=" * 40 + "\n")

            # Редирект на главную
            self.send_response(303)
            self.send_header('Location', '/')
            self.end_headers()

        except Exception as e:
            print(f"[EXCEPTION] {e}")
            self.send_error(500, "Internal server error")


if __name__ == "__main__":
    hostName = "localhost"
    serverPort = 8080
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print(f"Сервер запущен: http://{hostName}:{serverPort}")
    print("завершение работы (по Ctrl+D)")

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
    webServer.server_close()
    print("Сервер остановлен.")
