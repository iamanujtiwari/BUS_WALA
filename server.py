from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import json
import urllib.parse
import mimetypes
import re
import os

ROOT = Path(__file__).resolve().parent
SONGS = ROOT / "songs"
SONGS.mkdir(exist_ok=True)

AUDIO_EXTENSIONS = {".mp3", ".wav", ".m4a", ".ogg", ".flac", ".aac", ".opus"}
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


class MusicHandler(SimpleHTTPRequestHandler):
    """Music server with HTTP Range support for audio seeking."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/api/songs":
            files = []
            for audio in sorted(
                [p for p in SONGS.iterdir()
                 if p.is_file() and p.suffix.lower() in AUDIO_EXTENSIONS],
                key=lambda p: p.name.casefold(),
            ):
                files.append({"name": audio.name})

            body = json.dumps(files, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        file_path = self._resolve_audio_path(path)
        if file_path is not None:
            self._serve_audio_with_ranges(file_path)
            return

        super().do_GET()

    def _resolve_audio_path(self, url_path):
        prefix = "/songs/"
        if not url_path.startswith(prefix):
            return None

        relative = urllib.parse.unquote(url_path[len(prefix):])
        if not relative or "/" in relative or "\\" in relative:
            return None

        candidate = (SONGS / relative).resolve()
        try:
            candidate.relative_to(SONGS.resolve())
        except ValueError:
            return None

        if candidate.is_file() and candidate.suffix.lower() in AUDIO_EXTENSIONS:
            return candidate
        return None

    def _serve_audio_with_ranges(self, file_path):
        size = file_path.stat().st_size
        content_type = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
        range_header = self.headers.get("Range")

        if size == 0:
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Accept-Ranges", "bytes")
            self.send_header("Content-Length", "0")
            self.end_headers()
            return

        if not range_header:
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Accept-Ranges", "bytes")
            self.send_header("Content-Length", str(size))
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            self._write_file_range(file_path, 0, size - 1)
            return

        match = re.fullmatch(r"bytes=(\d*)-(\d*)", range_header.strip())
        if not match:
            self.send_response(416)
            self.send_header("Content-Range", f"bytes */{size}")
            self.end_headers()
            return

        start_s, end_s = match.groups()

        if start_s == "" and end_s == "":
            self.send_response(416)
            self.send_header("Content-Range", f"bytes */{size}")
            self.end_headers()
            return

        if start_s == "":
            try:
                length = min(int(end_s), size)
            except ValueError:
                self.send_response(416)
                self.send_header("Content-Range", f"bytes */{size}")
                self.end_headers()
                return
            start = max(0, size - length)
            end = size - 1
        else:
            try:
                start = int(start_s)
                end = int(end_s) if end_s else size - 1
            except ValueError:
                self.send_response(416)
                self.send_header("Content-Range", f"bytes */{size}")
                self.end_headers()
                return

            if start >= size or start < 0:
                self.send_response(416)
                self.send_header("Content-Range", f"bytes */{size}")
                self.end_headers()
                return

            end = min(end, size - 1)

        if end < start:
            self.send_response(416)
            self.send_header("Content-Range", f"bytes */{size}")
            self.end_headers()
            return

        length = end - start + 1

        self.send_response(206)
        self.send_header("Content-Type", content_type)
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.send_header("Content-Length", str(length))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self._write_file_range(file_path, start, end)

    def _write_file_range(self, file_path, start, end):
        remaining = end - start + 1

        with file_path.open("rb") as f:
            f.seek(start)

            while remaining > 0:
                chunk = f.read(min(1024 * 1024, remaining))
                if not chunk:
                    break
                self.wfile.write(chunk)
                remaining -= len(chunk)

    def log_message(self, fmt, *args):
        print(f"{self.address_string()} - {fmt % args}")


def main():
    # Render provides PORT. Local development falls back to 8000.
    host = "0.0.0.0"
    port = int(os.environ.get("PORT", "8000"))

    server = ThreadingHTTPServer((host, port), MusicHandler)

    print("Monsoon Music Player running at:")
    print(f"  http://{host}:{port}")
    print("Put your music files in the 'songs' folder, then refresh the browser.")
    print("HTTP Range support is enabled for smooth seeking.")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
