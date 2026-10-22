"""A tiny JSON-backed HTTP API for the cloud storage coursework prototype."""

from __future__ import annotations

import json
import os
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

DATA_PATH = Path(os.environ.get("CLOUD_STORAGE_PATH", "data/items.json"))
LOCK = threading.Lock()


def read_items() -> list[dict[str, Any]]:
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not DATA_PATH.exists():
        return []
    try:
        value = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError("Файл хранилища содержит некорректный JSON") from exc
    if not isinstance(value, list):
        raise ValueError("Корень файла хранилища должен быть JSON-массивом")
    return value


def write_items(items: list[dict[str, Any]]) -> None:
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    DATA_PATH.write_text(
        json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


class RequestHandler(BaseHTTPRequestHandler):
    def send_json(self, status: int, payload: Any) -> None:
        encoded = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def do_GET(self) -> None:
        if self.path == "/health":
            self.send_json(200, {"status": "ok"})
            return
        if self.path == "/items":
            try:
                with LOCK:
                    self.send_json(200, read_items())
            except ValueError as exc:
                self.send_json(500, {"error": str(exc)})
            return
        self.send_json(404, {"error": "Маршрут не найден"})

    def do_POST(self) -> None:
        if self.path != "/items":
            self.send_json(404, {"error": "Маршрут не найден"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length))
        except (ValueError, json.JSONDecodeError):
            self.send_json(400, {"error": "Ожидалось корректное JSON-тело запроса"})
            return
        if not isinstance(payload, dict) or not isinstance(payload.get("name"), str):
            self.send_json(400, {"error": "Поле name должно быть строкой"})
            return
        name = payload["name"].strip()
        if not name:
            self.send_json(400, {"error": "Поле name не должно быть пустым"})
            return
        description = payload.get("description", "")
        if not isinstance(description, str):
            self.send_json(400, {"error": "Поле description должно быть строкой"})
            return
        with LOCK:
            items = read_items()
            item = {"id": len(items) + 1, "name": name, "description": description}
            items.append(item)
            write_items(items)
        self.send_json(201, item)

    def log_message(self, format: str, *args: Any) -> None:
        print(f"{self.address_string()} - {format % args}")


def main() -> None:
    server = ThreadingHTTPServer(("127.0.0.1", 8000), RequestHandler)
    print(f"Учебный API доступен: http://{server.server_address[0]}:{server.server_address[1]}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nСервер остановлен")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
