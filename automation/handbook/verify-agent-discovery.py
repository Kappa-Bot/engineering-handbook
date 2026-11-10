"""Read-only HTTP acceptance probe for intentionally public negotiated documents."""

import argparse
import json
import re
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, *_args, **_kwargs):
        return None


DISCOVERY = {"alternate", "describedby", "api-catalog", "service-doc", "service-desc"}
MATRIX = (
    ("GET", "text/html", "text/html"),
    ("GET", "text/markdown", "text/markdown"),
    ("GET", None, "text/html"),
    ("GET", "*/*", "text/html"),
    ("GET", "text/markdown;q=0, */*;q=1", "text/html"),
    ("GET", "text/html;q=0.9, text/markdown;q=0.2", "text/html"),
    ("GET", "text/html;q=0.2, text/markdown;q=0.9", "text/markdown"),
    ("HEAD", "text/markdown", "text/markdown"),
    ("HEAD", "text/html", "text/html"),
    ("GET", "text/html", "text/html"),
)


def verify(origin, pages, exclusions):
    base = urlsplit(origin)
    if (base.scheme not in {"http", "https"} or not base.hostname or base.username or base.password
            or base.path not in {"", "/"} or base.query or base.fragment):
        raise ValueError("Provide an HTTP(S) origin without credentials, path, query or fragment.")
    origin = origin.rstrip("/")
    client = build_opener(NoRedirect())
    checks = []

    def read(url, method, accept):
        headers = {"Accept-Encoding": "identity"}
        if accept is not None:
            headers["Accept"] = accept
        request = Request(url, method=method, headers=headers)
        try:
            response = client.open(request, timeout=12)
        except HTTPError as error:
            response = error
        except (URLError, OSError):
            return 0, {}, ""
        with response:
            fields = {name.lower(): ", ".join(response.headers.get_all(name)) for name in response.headers.keys()}
            return response.code, fields, response.read(2_000_000).decode("utf-8", "replace")

    def location(pathname):
        parts = urlsplit(pathname)
        if not pathname.startswith("/") or pathname.startswith("//") or parts.netloc or parts.scheme or parts.fragment:
            raise ValueError("Probe paths must be origin-relative and have no fragment.")
        return origin + pathname

    for page in pages:
        url = location(page)
        html_links = ""
        for method, accept, expected in MATRIX:
            status, headers, body = read(url, method, accept)
            content_type = headers.get("content-type", "")
            vary = {item.strip().lower() for item in headers.get("vary", "").split(",")}
            ok = status == 200 and content_type.split(";")[0].lower() == expected and "accept" in vary
            if expected == "text/markdown":
                ok = ok and bool(re.search(r"charset\s*=\s*\"?utf-8\"?", content_type, re.I))
                if method == "GET":
                    ok = ok and bool(re.search(r"^(?:#{1,6} |[-*] |\d+\. )\S", body, re.M)) and not re.search(
                        r"<(?:html|script|style|iframe|body)\b", body, re.I
                    )
            if method == "HEAD":
                ok = ok and not body
            if method == "GET" and accept == "text/html":
                html_links = headers.get("link", "")
            checks.append({"path": page, "method": method, "accept": accept, "expect": expected,
                           "status": status, "type": content_type, "pass": ok})

        seen = set()
        discovery_count = 0
        for target, parameters in re.findall(r"<([^<>]+)>([^<>]*)", html_links):
            attrs = {name.lower(): quoted or bare for name, quoted, bare in re.findall(
                r';\s*([-\w]+)\s*=\s*(?:"([^"]*)"|([^;,\s]+))', parameters
            )}
            relations = set(attrs.get("rel", "").lower().split()) & DISCOVERY
            if not relations:
                continue
            discovery_count += 1
            destination = urljoin(url, target)
            parts = urlsplit(destination)
            same_origin = (parts.scheme, parts.netloc) == (base.scheme, base.netloc)
            identity = (destination, tuple(sorted(relations)), attrs.get("type"))
            duplicate = identity in seen
            seen.add(identity)
            # External destinations are deliberately not fetched by this probe.
            if not same_origin:
                checks.append({"path": page, "expect": "same-origin Link target",
                               "pass": False, "reason": "Validate the external target separately."})
                continue
            accepted = attrs.get("type")
            status, fields, body = read(destination, "GET", accepted)
            ok = not duplicate and 200 <= status < 300 and bool(body)
            if accepted:
                ok = ok and fields.get("content-type", "").split(";")[0].lower() == accepted.lower()
            checks.append({"path": page, "target": parts.path, "expect": "working unique Link target",
                           "status": status, "pass": ok})
        checks.append({"path": page, "expect": "discovery Link", "pass": discovery_count > 0})

    for pathname, expected in exclusions:
        status, headers, _ = read(location(pathname), "GET", "text/markdown")
        media = headers.get("content-type", "").split(";")[0].lower()
        checks.append({"path": pathname, "expect": expected, "status": status, "type": media,
                       "pass": status == expected and media != "text/markdown" and not re.search(
                           r"\b(?:describedby|api-catalog|text/markdown)\b", headers.get("link", ""), re.I
                       )})
    return checks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--origin", required=True)
    parser.add_argument("--page", action="append", help="Negotiated route; repeat (default /)")
    parser.add_argument("--exclude", action="append", default=[], metavar="PATH=STATUS")
    args = parser.parse_args()
    try:
        exclusions = [(route, int(status)) for route, status in (item.rsplit("=", 1) for item in args.exclude)]
        checks = verify(args.origin, args.page or ["/"], exclusions)
    except (TypeError, ValueError) as error:
        parser.error(str(error))
    passed = sum(check["pass"] for check in checks)
    print(json.dumps({"passed": passed, "total": len(checks), "checks": checks}, ensure_ascii=False))
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
