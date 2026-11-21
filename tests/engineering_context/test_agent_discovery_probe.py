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

    def test_checks_content_type_in_inert_responses(self):
        from email.message import Message
        from io import BytesIO
        from unittest.mock import patch
        from urllib.parse import urlsplit

        spec = importlib.util.spec_from_file_location("verify_agent_discovery", SCRIPT)
        probe = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(probe)

        class Opener:
            def open(self, request, timeout):
                path = urlsplit(request.full_url).path
                assert path in ("/", "/index", "/private")
                markdown = request.get_header("Accept") in (
                    "text/markdown", "text/html;q=0.2, text/markdown;q=0.9",
                )
                body = b"# Public fixture" if markdown else b"<!doctype html>"
                if request.get_method() == "HEAD":
                    body = b""
                response = BytesIO(body)
                response.headers = Message()
                response.code = 401 if path == "/private" else 200
                if path == "/":
                    response.headers["Vary"] = "Accept"
                    response.headers["Link"] = '</index>; rel="describedby"; type="text/plain"'
                if path == "/private":
                    types = private
                elif path == "/index":
                    types = ('text/plain \t; note="quoted; value"',)
                elif markdown:
                    types = public
                else:
                    types = ("text/html",)
                for content_type in types:
                    response.headers.add_header("Content-Type", content_type)
                return response

        markdown = ("text/markdown; charset=utf-8",)
        for public, private, bad in (
            ((r' TeXT/Markdown ; variant="optional; data"; Charset="UTF\-8"',), (), set()),
            (("text/markdown; x-charset=utf-8",), (), {"/"}),
            (("text/markdown; charset=utf-8-fixture",), (), {"/"}),
            (('text/markdown; note="charset=utf-8"',), (), {"/"}),
            ((*markdown, "text/html"), (), {"/"}),
            (markdown, ("text/markdown \t; charset=utf-8",), {"/private"}),
            (markdown, ("text/plain; charset=utf-8", *markdown), {"/private"}),
        ):
            with self.subTest(public=public, private=private), patch.object(probe, "build_opener", return_value=Opener()):
                checks = probe.verify("https://fixture.invalid", ["/"], [("/private", 401)])
                self.assertEqual({row["path"] for row in checks if not row["pass"]}, bad)

    def test_accepts_real_variants_link_targets_and_private_denial(self):
        self.assertTrue(all(check["pass"] for check in self.run_probe()))

    def test_rejects_mixed_variants_and_private_markdown(self):
        failures = [check for check in self.run_probe(mix_variants=True, publish_private=True) if not check["pass"]]
        self.assertTrue(any(check["path"] == "/" and check["expect"] == "text/html" for check in failures))
        self.assertTrue(any(check["path"] == "/private" for check in failures))

    def test_counts_link_targets_only_in_the_reviewed_page_context(self):
        from email.message import Message
        from io import BytesIO
        from unittest.mock import patch
        from urllib.parse import urlsplit

        spec = importlib.util.spec_from_file_location("verify_agent_discovery", SCRIPT)
        probe = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(probe)

        class Opener:
            def open(self, request, timeout):
                path = urlsplit(request.full_url).path
                md = request.get_header("Accept") in ("text/markdown", "text/html;q=0.2, text/markdown;q=0.9")
                if path == "/guide/overview":
                    body = b"# Public guide" if md else b"<!doctype html>"
                    content_type = "text/markdown; charset=utf-8" if md else "text/html"
                else:
                    assert path == "/docs/index"
                    visited.append(path)
                    body, content_type = b"Public index", "text/plain"
                response = BytesIO(body if request.get_method() != "HEAD" else b"")
                response.code, response.headers = 200, Message()
                response.headers["Content-Type"] = content_type
                response.headers["Vary"] = "Accept"
                if path == "/guide/overview":
                    response.headers["Link"] = header
                return response

        link = '</docs/index>; rel="describedby"; type="text/plain"'
        elsewhere = link + '; anchor="/guide/introduction"'
        for header, finds_discovery in (
            (link, True),
            ('</docs/index>; rel="describedby"; type="text/plain"; title="The \\"quick\\" guide; anchor=local label"', True),
            ('</docs/index>; rel="describedby"; type="text/plain"; title="Page examples; anchor=editor <label>"', True),
            ('</docs/index>; rel="describedby"; type="text/plain"; anchor="./overvie\\w?lang=es"', True),
            (link + '; anchor="./overview?lang=es"', True),
            (link + '; anchor="#part"', False),
            (link + '; anchor="?"', False),
            (elsewhere, False),
            (elsewhere + ", " + link, True),
            (elsewhere + '; anchor="./overview?lang=es"', False),
        ):
            visited = []
            with self.subTest(header=header), patch.object(probe, "build_opener", return_value=Opener()):
                checks = probe.verify("https://fixture.invalid", ["/guide/overview?lang=es"], [])
            self.assertEqual(visited, ["/docs/index"] if finds_discovery else [])
            self.assertEqual(checks[-1]["pass"], finds_discovery)
            self.assertTrue(all(check["pass"] for check in checks[:-1]))

    def test_first_relation_and_type_apply_to_each_link_value(self):
        from email.message import Message
        from io import BytesIO
        from unittest.mock import patch
        from urllib.response import addinfourl

        spec = importlib.util.spec_from_file_location("verify_agent_discovery", SCRIPT)
        probe = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(probe)
        origin = "https://fixture.invalid"
        page = Message()
        page["Content-Type"] = "text/html"
        page["Vary"] = "Accept"
        page["Link"] = ('</manual>; ReL="next DESCRIBEDBY"; rel=next; TYPE="text/plain"; type=text/html, '
                        '</other>; rel=next; rel=alternate')
        target = Message()
        target["Content-Type"] = "text/plain"
        with patch.object(probe, "MATRIX", [("GET", "text/html", "text/html")]), patch.object(probe, "build_opener") as factory:
            client = factory.return_value
            client.open.side_effect = [
                addinfourl(BytesIO(b"Guide"), page, origin, 200),
                addinfourl(BytesIO(b"Manual"), target, origin + "/manual", 200),
            ]
            checks = probe.verify(origin, ["/guide"], [])
        self.assertTrue(all(check["pass"] for check in checks))
        requests = [call.args[0] for call in client.open.call_args_list]
        self.assertEqual([(req.full_url, req.get_header("Accept")) for req in requests],
                         [(origin + "/guide", "text/html"), (origin + "/manual", "text/plain")])

    def test_requires_discovery_on_each_successful_explicit_html_sample(self):
        from email.message import Message
        from io import BytesIO
        from unittest.mock import patch
        from urllib.response import addinfourl

        spec = importlib.util.spec_from_file_location("verify_agent_discovery", SCRIPT)
        probe = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(probe)
        origin = "https://fixture.invalid"

        def response(media, link=None):
            headers = Message()
            headers["Content-Type"] = media
            headers["Vary"] = "Accept"
            if link:
                headers["Link"] = link
            return addinfourl(BytesIO(b"Public fixture"), headers, origin, 200)

        last = '</catalog>; rel="describedby"; type="text/plain"; title="Warm page"'
        for first, expected in (
            (None, False),
            ('</style>; rel="stylesheet"', False),
            ('</catalog>; rel="describedby"; anchor="/elsewhere"', False),
            ('</catalog>; rel="stylesheet"; rel="describedby"', False),
            ('</catalog>; rel="describedby"; title="Cold page"', True),
            ('</earlier>; rel="service-doc"', True),
        ):
            with self.subTest(first=first), patch.object(probe, "MATRIX", [
                ("GET", "text/html", "text/html"), ("GET", "text/html", "text/html"),
            ]), patch.object(probe, "build_opener") as factory:
                client = factory.return_value
                client.open.side_effect = [
                    response("text/html", first), response("text/html", last), response("text/plain"),
                ]
                checks = probe.verify(origin, ["/guide"], [])
                self.assertEqual([check["pass"] for check in checks], [True, True, True, expected])
                self.assertEqual([call.args[0].full_url for call in client.open.call_args_list],
                                 [origin + "/guide", origin + "/guide", origin + "/catalog"])

    def test_probes_same_origin_link_authority_aliases_only(self):
        from email.message import Message
        from io import BytesIO
        from unittest.mock import patch
        from urllib.response import addinfourl

        spec = importlib.util.spec_from_file_location("verify_agent_discovery", SCRIPT)
        probe = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(probe)
        selector = "/Guide/Item?lang=ES&mark=%2F"
        for origin, authorities, expected in (
            ("https://fixture.invalid", ["https://FiXtUrE.Invalid:443"], [True]),
            ("https://fixture.invalid:443", ["https://fixture.invalid"], [True]),
            ("http://fixture.invalid", ["//FiXtUrE.Invalid:80"], [True]),
            ("https://fixture.invalid", ["https://fixture.invalid", "https://fixture.invalid:443"], [True, False]),
            ("https://fixture.invalid", ["http://fixture.invalid"], []),
            ("https://fixture.invalid", ["https://other.fixture.invalid"], []),
            ("https://fixture.invalid", ["https://fixture.invalid:8443"], []),
            ("https://fixture.invalid", ["https://reviewer@fixture.invalid"], []),
            ("https://fixture.invalid", ["https://fixture.invalid:preview"], []),
            ("https://fixture.invalid", ["https://fixture.invalid:"], []),
        ):
            with self.subTest(origin=origin, authorities=authorities):
                link = ", ".join(f'<{authority + selector}>; rel="describedby"; type="application/json"'
                                 for authority in authorities)
                requests = []

                def respond(request, timeout):
                    headers = Message()
                    if request.full_url == origin + "/manual":
                        headers["Content-Type"] = "text/html"
                        headers["Vary"] = "Accept"
                        headers["Link"] = link
                    else:
                        requests.append((request.full_url, request.selector))
                        headers["Content-Type"] = "application/json"
                    return addinfourl(BytesIO(b"Fixture payload"), headers, request.full_url, 200)

                with patch.object(probe, "MATRIX", [("GET", "text/html", "text/html")]), \
                     patch.object(probe, "build_opener") as opener:
                    opener.return_value.open.side_effect = respond
                    checks = probe.verify(origin, ["/manual"], [])
                self.assertEqual(requests, [(origin + selector, selector)] * len(expected))
                self.assertEqual([check["pass"] for check in checks if check["expect"] == "working unique Link target"],
                                 expected)
                if not expected:
                    self.assertTrue(any(check["expect"] == "same-origin Link target" and not check["pass"]
                                        for check in checks))

    def test_body_read_failure_leaves_later_checks_available(self):
        from email.message import Message
        from http.client import IncompleteRead
        from io import BytesIO
        from unittest.mock import patch
        from urllib.error import URLError
        from urllib.response import addinfourl

        class Interrupted(BytesIO):
            def read(self, size=-1):
                raise IncompleteRead(super().read(size), 3)

        spec = importlib.util.spec_from_file_location("verify_agent_discovery", SCRIPT)
        probe = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(probe)
        origin = "https://fixture.invalid"
        headers = Message()
        headers["Content-Type"] = "text/plain"
        incomplete = Interrupted(b"partial document")
        with patch.object(probe, "build_opener") as factory:
            factory.return_value.open.side_effect = [
                addinfourl(incomplete, headers, origin, 200),
                URLError("fixture unavailable"),
                addinfourl(BytesIO(b"denied"), headers, origin, 403),
            ]
            checks = probe.verify(origin, [], [("/incomplete", 200), ("/unavailable", 0), ("/later", 403)])
        self.assertTrue(incomplete.closed)
        self.assertEqual([(row["status"], row["pass"]) for row in checks], [(0, False), (0, False), (403, True)])

    def test_open_protocol_failure_is_unavailable_and_later_checks_continue(self):
        from email.message import Message
        from http.client import BadStatusLine, HTTPException, InvalidURL, ResponseNotReady
        from io import BytesIO
        from unittest.mock import patch
        from urllib.error import HTTPError

        spec = importlib.util.spec_from_file_location("verify_agent_discovery", SCRIPT)
        probe = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(probe)
        origin = "https://fixture.invalid"
        headers = Message()
        headers["Content-Type"] = "text/plain"
        with patch.object(probe, "build_opener") as factory:
            client = factory.return_value
            client.open.side_effect = [
                BadStatusLine("incomplete response"), HTTPException("headers unavailable"),
                HTTPError(origin + "/later", 403, "denied", headers, BytesIO(b"denied")),
            ]
            checks = probe.verify(origin, [], [("/first", 403), ("/second", 0), ("/later", 403)])
            self.assertEqual([(row["status"], row["pass"]) for row in checks], [(0, False), (0, False), (403, True)])
            for problem in (InvalidURL("invalid fixture URL"), ResponseNotReady("client state")):
                with self.subTest(problem=type(problem).__name__), self.assertRaises(type(problem)):
                    client.open.side_effect = problem
                    probe.verify(origin, [], [("/first", 403)])
