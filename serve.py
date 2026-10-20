"""Serve Interview Desk on http://localhost:8080 (this Mac only).

Same as `python3 -m http.server`, but tells the browser not to keep an old copy
of the page, so you always get the latest version after an update.
"""
import errno, functools, http.server, os

PORT = 8080
HERE = os.path.dirname(os.path.abspath(__file__))


class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


if __name__ == "__main__":
    handler = functools.partial(NoCacheHandler, directory=HERE)
    try:
        server = http.server.ThreadingHTTPServer(("127.0.0.1", PORT), handler)
    except OSError as e:
        if e.errno in (errno.EADDRINUSE, 48, 98):
            raise SystemExit(f"Port {PORT} is already in use — Interview Desk is probably already running in another Terminal tab.\n"
                             f"Just open http://localhost:{PORT}. (To restart it, press Ctrl+C in that other tab first.)")
        raise
    with server:
        print(f"Interview Desk running at http://localhost:{PORT}  (press Ctrl+C to stop)")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nStopped.")
