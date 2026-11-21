"""Read-only HTTP acceptance probe for intentionally public negotiated documents."""

import argparse
import json
import re
from http.client import HTTPException, ImproperConnectionState, InvalidURL
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


_HTTP_TOKEN = r"[!#$%&'*+\-.^_\x60|~0-9A-Za-z]+"
_HTTP_QUOTED = r'"(?:[\t !\x23-\x5b\x5d-\x7e\x80-\xff]|\\[\t \x21-\x7e\x80-\xff])*"'
_MEDIA_TYPE = re.compile(rf"{_HTTP_TOKEN}/{_HTTP_TOKEN}")
_MEDIA_PARAMETER = re.compile(rf"[ \t]*;[ \t]*(?:({_HTTP_TOKEN})=({_HTTP_TOKEN}|{_HTTP_QUOTED}))?")


def _content_type(value: str) -> tuple[str, bool]:
    """Read a single HTTP media type and whether it declares exactly one UTF-8 charset."""
    value = value.strip(" \t")
    media = _MEDIA_TYPE.match(value)
    if not media:
        return "", False
    end = media.end()
    charsets = []
    while end < len(value):
        parameter = _MEDIA_PARAMETER.match(value, end)
        if not parameter:
            return "", False
        end = parameter.end()
        name, charset = parameter.groups()
        if name and name.lower() == "charset":
            if charset.startswith('"'):
                charset = re.sub(r"\\(.)", r"\1", charset[1:-1])
            charsets.append(charset.lower())
    return media[0].lower(), charsets == ["utf-8"]


def _same_page_anchor(page_url, anchor):
    if anchor.startswith('"'):
        anchor = re.sub(r"\\(.)", r"\1", anchor[1:-1])
    _, query_separator, query = anchor.partition("?")
    # Fragments select other link contexts. urljoin can also inherit a query
    # despite an explicit empty query in the anchor, so skip that form.
    if "#" in anchor or (query_separator and not query):
        return False
    try:
        return urljoin(page_url, anchor) == page_url
    except ValueError:
        return False


def _discovery_links(page_url, header):
    for target, parameters in re.findall(rf'<([^<>]+)>((?:{_HTTP_QUOTED}|[^"<>])*)', header):
        link_parameters = re.findall(rf';\s*([-\w]+)\s*=\s*({_HTTP_QUOTED}|[^";,\s]+)', parameters)
        attrs = {}
        for name, value in link_parameters:
            key = name.lower()
            if key in ("rel", "type"):
                # RFC 8288 gives the first occurrence precedence within this link-value.
                attrs.setdefault(key, value[1:-1] if value.startswith('"') else value)
        relations = set(attrs.get("rel", "").lower().split()) & DISCOVERY
        if not relations:
            continue
        # An anchored link only describes this page if its context resolves here.
        anchors = [value for name, value in link_parameters if name.lower() == "anchor"]
        if anchors and (len(anchors) != 1 or not _same_page_anchor(page_url, anchors[0])):
            continue
        yield target, relations, attrs.get("type")


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
        except (InvalidURL, ImproperConnectionState):
            raise
        except (URLError, OSError, HTTPException):
            return 0, {}, ""
        try:
            with response:
                fields = {name.lower(): ", ".join(response.headers.get_all(name)) for name in response.headers.keys()}
                return response.code, fields, response.read(2_000_000).decode("utf-8", "replace")
        except (HTTPException, OSError):
            return 0, {}, ""

    def location(pathname):
        parts = urlsplit(pathname)
        if not pathname.startswith("/") or pathname.startswith("//") or parts.netloc or parts.scheme or parts.fragment:
            raise ValueError("Probe paths must be origin-relative and have no fragment.")
        return origin + pathname

    for page in pages:
        url = location(page)
        html_links = []
        all_html_have_discovery = True
        for method, accept, expected in MATRIX:
            status, headers, body = read(url, method, accept)
            content_type = headers.get("content-type", "")
            media, utf8 = _content_type(content_type)
            vary = {item.strip().lower() for item in headers.get("vary", "").split(",")}
            ok = status == 200 and media == expected and "accept" in vary
            if expected == "text/markdown":
                ok = ok and utf8
                if method == "GET":
                    ok = ok and bool(re.search(r"^(?:#{1,6} |[-*] |\d+\. )\S", body, re.M)) and not re.search(
                        r"<(?:html|script|style|iframe|body)\b", body, re.I
                    )
            if method == "HEAD":
                ok = ok and not body
            if method == "GET" and accept == "text/html":
                html_links = list(_discovery_links(url, headers.get("link", "")))
                if ok and not html_links:
                    all_html_have_discovery = False
            checks.append({"path": page, "method": method, "accept": accept, "expect": expected,
                           "status": status, "type": content_type, "pass": ok})

        seen = set()
        for target, relations, accepted in html_links:
            destination = urljoin(url, target)
            parts = urlsplit(destination)
            same_origin = (parts.scheme, parts.netloc) == (base.scheme, base.netloc)
            identity = (destination, tuple(sorted(relations)), accepted)
            duplicate = identity in seen
            seen.add(identity)
            # External destinations are deliberately not fetched by this probe.
            if not same_origin:
                checks.append({"path": page, "expect": "same-origin Link target",
                               "pass": False, "reason": "Validate the external target separately."})
                continue
            status, fields, body = read(destination, "GET", accepted)
            ok = not duplicate and 200 <= status < 300 and bool(body)
            if accepted:
                media, _ = _content_type(fields.get("content-type", ""))
                ok = ok and media == accepted.lower()
            checks.append({"path": page, "target": parts.path, "expect": "working unique Link target",
                           "status": status, "pass": ok})
        checks.append({"path": page, "expect": "discovery Link", "pass": bool(html_links) and all_html_have_discovery})

    for pathname, expected in exclusions:
        status, headers, _ = read(location(pathname), "GET", "text/markdown")
        content_type = headers.get("content-type")
        media, _ = _content_type(content_type or "")
        checks.append({"path": pathname, "expect": expected, "status": status,
                       "type": media or content_type or "",
                       "pass": status != 0 and status == expected and (content_type is None or bool(media))
                       and media != "text/markdown" and not re.search(
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
