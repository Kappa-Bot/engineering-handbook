import importlib.util
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread


SCRIPT = Path(__file__).resolve().parents[2] / "automation/handbook/verify-agent-discovery.py"


class AgentDiscoveryProbeTests(unittest.TestCase):
    def run_probe(self, *, mix_variants=False, publish_private=False):
        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *_args):
                pass

            def do_GET(self):
                accept = self.headers.get("Accept", "")
                markdown = mix_variants or accept in (
                    "text/markdown", "text/html;q=0.2, text/markdown;q=0.9",
                )
                media = "text/markdown" if markdown else "text/html"
                code = 200
                headers = {}
                if self.path == "/":
                    headers = {
                        "Link": '</llms.txt>; rel="describedby", </>; rel="alternate"; type="text/markdown"',
                        "Vary": "Accept, RSC",
                    }
                    body = b"# Services\n\nUseful public details." if markdown else b"<!doctype html><h1>Services</h1>"
                elif self.path == "/llms.txt":
                    media, body = "text/plain", b"# Public content index"
                else:
                    media = "text/markdown" if publish_private else "text/plain"
                    code, body = (200, b"# Internal") if publish_private else (401, b"Unauthorized")
                self.send_response(code)
                self.send_header("Content-Type", media + "; charset=utf-8")
                for key, value in headers.items():
                    self.send_header(key, value)
                self.end_headers()
                if self.command != "HEAD":
                    self.wfile.write(body)

            do_HEAD = do_GET

        spec = importlib.util.spec_from_file_location("verify_agent_discovery", SCRIPT)
        probe = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(probe)
        with ThreadingHTTPServer(("127.0.0.1", 0), Handler) as server:
            worker = Thread(target=server.serve_forever)
            worker.start()
            try:
                return probe.verify("http://127.0.0.1:" + str(server.server_port), ["/"], [("/private", 401)])
            finally:
                server.shutdown()
                worker.join()

    def test_accepts_real_variants_link_targets_and_private_denial(self):
        self.assertTrue(all(check["pass"] for check in self.run_probe()))

    def test_rejects_mixed_variants_and_private_markdown(self):
        failures = [check for check in self.run_probe(mix_variants=True, publish_private=True) if not check["pass"]]
        self.assertTrue(any(check["path"] == "/" and check["expect"] == "text/html" for check in failures))
        self.assertTrue(any(check["path"] == "/private" for check in failures))
