"""Build and preview the portfolio, serving only the finished website."""

import argparse
import os
import re
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

from scripts.build import OUTPUT, build


class PreviewHandler(SimpleHTTPRequestHandler):
    """Serve fresh files and byte ranges so video controls can seek."""

    def send_head(self):
        self.range_remaining = None
        path = self.translate_path(self.path)
        requested = self.headers.get("Range", "")
        if not requested or not path.endswith(".mp4") or not os.path.isfile(path):
            return super().send_head()

        match = re.fullmatch(r"bytes=(\d*)-(\d*)", requested)
        # Multiple or malformed ranges can be ignored with a normal 200 response.
        if not match or not any(match.groups()):
            return super().send_head()

        source = open(path, "rb")
        size = os.fstat(source.fileno()).st_size
        first, last = match.groups()
        if first:
            start = int(first)
            end = min(int(last), size - 1) if last else size - 1
        else:
            start, end = max(0, size - int(last)), size - 1
        if start > end or start >= size:
            source.close()
            self.send_response(416)
            self.send_header("Content-Range", f"bytes */{size}")
            self.send_header("Content-Length", "0")
            self.end_headers()
            return None

        self.send_response(206)
        self.send_header("Content-Type", "video/mp4")
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.send_header("Content-Length", str(end - start + 1))
        self.end_headers()
        source.seek(start)
        self.range_remaining = end - start + 1
        return source

    def copyfile(self, source, outputfile):
        try:
            if self.range_remaining is None:
                return super().copyfile(source, outputfile)
            remaining = self.range_remaining
            while remaining:
                chunk = source.read(min(64 * 1024, remaining))
                if not chunk:
                    break
                outputfile.write(chunk)
                remaining -= len(chunk)
        except (BrokenPipeError, ConnectionResetError):
            # A browser can cancel a download when seeking or leaving the page.
            pass

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    build()
    handler = partial(PreviewHandler, directory=str(OUTPUT))
    server = ThreadingHTTPServer(("127.0.0.1", args.port), handler)
    print(f"Local: http://localhost:{args.port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
