#!/usr/bin/env python3
"""Offline inventory and narrowly scoped removal of legacy Handbook agent hooks.

This does NOT configure coding agents or disable their permissions, approvals,
security checks, plugins, or provider-managed hooks. It modifies only local user
JSON hook entries that invoke the EXACT Codex Handbook bootstrap with
"preflight --hook". Everything else is read-only or flagged for human review.
No network calls, packages, subprocesses, prompt or transcript reads.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import stat
import sys
import uuid

MAX_FILE_BYTES = 1_048_576
MAX_TARGETS = 300
MAX_SCRIPT_CHILDREN = 20
AUDIT_SCHEMA = "handbook-agent-hook-audit/v1"


@dataclass(frozen=True)
class Target:
    client: str
    path: Path
    scope: str
    kind: str = "json"

    @property
    def editable(self) -> bool:
        return self.scope == "user" and self.kind == "json"


def _safe_file(path: Path) -> bool:
    """Avoid following links/reparse points or rewriting managed/unknown data."""
    if not path.is_file() or path.is_symlink():
        return False
    for parent in (path, *path.parents):
        try:
            if parent.is_symlink() or getattr(parent.lstat(), "st_file_attributes", 0) & 0x400:
                return False
        except OSError:
            return False
    try:
        return stat.S_ISREG(path.stat().st_mode) and path.stat().st_size <= MAX_FILE_BYTES
    except OSError:
        return False


ALTERNATE_COMMAND_FIELDS = {
    "powershell", "bash", "cmd", "exec", "script", "commandWindows", "windows", "linux", "osx",
}


def is_owned_bootstrap_command(command: str, script: Path) -> bool:
    """Exact installed-script ownership, never a filename/keyword-only guess."""
    if not isinstance(command, str):
        return False
    try:
        argv = shlex.split(command)
    except ValueError:
        return False
    if shlex.join(argv) != command:
        if os.name != "nt" or re.search(r"""['"&|<>^%!]""", command):
            return False
        # Preserve backslashes in the exact unquoted native spelling.
        argv = command.split()
        if " ".join(argv) != command:
            return False
    if len(argv) not in (5, 7) or argv[1] != "-I" or argv[3:5] != ["preflight", "--hook"]:
        return False
    if len(argv) == 7 and (argv[5] != "--event" or argv[6] not in ("SessionStart", "UserPromptSubmit")):
        return False
    name = argv[0].replace("\\", "/").rsplit("/", 1)[-1].casefold()
    return (os.path.normcase(argv[2]) == os.path.normcase(str(script))
            and bool(re.fullmatch(r"(?:python(?:\d+(?:\.\d+)*t?)?|py)(?:\.exe)?", name)))


def _looks_like_handbook_hook(command: str) -> bool:
    if not isinstance(command, str):
        return False
    low = command.casefold()
    return (("handbook_update.py" in low or "engineering-handbook" in low
             or "handbook-bootstrap" in low)
            and any(token in low for token in ("hook", "preflight", "update", "check")))


def _standalone_command(entry: dict) -> bool:
    return ("hooks" not in entry and entry.get("type", "command") == "command"
            and not ALTERNATE_COMMAND_FIELDS.intersection(entry))


def _hybrid_group(entry: dict) -> bool:
    return isinstance(entry.get("hooks"), list) and (
        "command" in entry or bool(ALTERNATE_COMMAND_FIELDS.intersection(entry))
    )


def _commands(value, *, review_only: bool = False):
    """Find command-like values without interpreting/executing hook code."""
    if isinstance(value, dict):
        review_only = review_only or _hybrid_group(value)
        for key, child in value.items():
            if isinstance(child, str) and (key == "command" or key in ALTERNATE_COMMAND_FIELDS):
                if key == "exec" and isinstance(value.get("args"), list):
                    child = " ".join([child, *(arg for arg in value["args"] if isinstance(arg, str))])
                yield key, child, not review_only and key == "command" and _standalone_command(value)
            elif isinstance(child, (dict, list)):
                yield from _commands(child, review_only=review_only)
    elif isinstance(value, list):
        for child in value:
            yield from _commands(child, review_only=review_only)


def _strip_owned(groups: list, script: Path) -> tuple[list, int]:
    """Only recognized hook-group shapes are edited; mixed groups are preserved."""
    kept = []
    removed = 0
    for group in groups:
        if not isinstance(group, dict):
            kept.append(group)
            continue
        inner = group.get("hooks")
        if isinstance(inner, list):
            if _hybrid_group(group):
                kept.append(group)
                continue
            remaining, count = _strip_owned(inner, script)
            removed += count
            if remaining:
                clone = dict(group)
                clone["hooks"] = remaining
                kept.append(clone)
            elif not count:
                kept.append(group)
        elif _standalone_command(group) and is_owned_bootstrap_command(group.get("command"), script):
            removed += 1
        else:
            kept.append(group)
    return kept, removed


def strip_config(data: object, script: Path) -> tuple[dict, int]:
    if not isinstance(data, dict):
        raise ValueError("hook configuration root must be an object")
    raw = data.get("hooks")
    if raw is None:
        return data, 0
    if not isinstance(raw, dict):
        raise ValueError("hooks must be an event-to-array object")
    # Refuse edits to partially malformed structures rather than lose them.
    if not all(isinstance(groups, list) for groups in raw.values()):
        raise ValueError("unrecognized hook event structure; file unchanged")
    result = dict(data)
    hooks = dict(raw)
    count = 0
    for event, groups in raw.items():
        updated, removed = _strip_owned(groups, script)
        count += removed
        if not removed:
            continue
        if updated:
            hooks[event] = updated
        else:
            hooks.pop(event, None)
    if count:
        result["hooks"] = hooks
    return result, count


def _add_target(items: dict[str, Target], client: str, path: Path, scope: str,
                kind: str = "json") -> None:
    key = os.path.normcase(str(path.absolute()))
    # A user-scoped target is allowed to replace a project/audit-only duplicate
    # only when it was discovered from a known user config location.
    if key not in items:
        items[key] = Target(client, path.absolute(), scope, kind)


def _record_limit_hit(limit_hits: list[dict] | None, bound: str, count: int, limit: int,
                      **location: str) -> None:
    if limit_hits is not None and count > limit:
        limit_hits.append({"bound": bound, "candidate_count": count, "limit": limit,
                           "omitted_candidates": count - limit, **location})


def _config_dir(items: dict[str, Target], client: str, directory: Path,
                scope: str, glob: str = "*.json", kind: str = "json", *,
                limit_hits: list[dict] | None = None) -> None:
    if not directory.is_dir() or directory.is_symlink():
        return
    paths = sorted(directory.glob(glob))
    _record_limit_hit(limit_hits, "directory", len(paths), MAX_TARGETS,
                      client=client, scope=scope, path=str(directory.absolute()))
    del paths[MAX_TARGETS:]
    for path in paths:
        if path.is_file():
            _add_target(items, client, path, scope, kind)
        elif kind == "script" and path.is_dir() and not path.is_symlink():
            # OpenCode plugins may be packaged in one directory per plugin.
            # One bounded level, never an unrestricted recursive home scan.
            children = sorted(path.glob("*"))
            _record_limit_hit(limit_hits, "script_directory_children", len(children), MAX_SCRIPT_CHILDREN,
                              client=client, scope=scope, path=str(path.absolute()))
            del children[MAX_SCRIPT_CHILDREN:]
            for child in children:
                if child.is_file():
                    _add_target(items, client, child, scope, kind)


def _client_home(home: Path, directory: str, env_key: str, use_environment: bool) -> Path:
    configured = os.environ.get(env_key) if use_environment else None
    return Path(configured).expanduser() if configured else home / directory


def discover(home: Path, projects: list[Path], extras: list[Path], *,
             use_environment: bool = False, limit_hits: list[dict] | None = None) -> list[Target]:
    """Bounded, explicit locations: never traverse a home or repository tree."""
    items: dict[str, Target] = {}
    codex_home = _client_home(home, ".codex", "CODEX_HOME", use_environment)
    claude_home = _client_home(home, ".claude", "CLAUDE_CONFIG_DIR", use_environment)
    copilot_home = _client_home(home, ".copilot", "COPILOT_HOME", use_environment)
    for client, path in (
        ("codex", codex_home / "hooks.json"),
        ("claude-code", claude_home / "settings.json"),
        ("cursor", home / ".cursor/hooks.json"),
        ("gemini-cli", home / ".gemini/settings.json"),
        ("github-copilot", copilot_home / "settings.json"),
        ("windsurf", home / ".codeium/windsurf/hooks.json"),
        ("windsurf-jetbrains", home / ".codeium/hooks.json"),
    ):
        _add_target(items, client, path, "user")
    _config_dir(items, "github-copilot", copilot_home / "hooks", "user", limit_hits=limit_hits)
    # Cline and OpenCode hooks are executable scripts/plugins, not generic JSON
    # maps. Audit them, but never edit them as if they used Codex hook syntax.
    for client, path in (
        ("cline", home / "Documents/Cline/Hooks"),
        ("cline-cli", home / ".cline/hooks"),
        ("opencode", home / ".config/opencode/plugins"),
        ("opencode", home / ".opencode/plugins"),
    ):
        _config_dir(items, client, path, "audit-only", "*", "script", limit_hits=limit_hits)
    for project in projects:
        root = project.expanduser().absolute()
        for client, relative in (
            ("codex", ".codex/hooks.json"),
            ("claude-code", ".claude/settings.json"),
            ("claude-code", ".claude/settings.local.json"),
            ("cursor", ".cursor/hooks.json"),
            ("gemini-cli", ".gemini/settings.json"),
            ("windsurf", ".windsurf/hooks.json"),
            ("github-copilot", ".github/copilot/settings.json"),
            ("github-copilot", ".github/copilot/settings.local.json"),
        ):
            _add_target(items, client, root / relative, "project")
        _config_dir(items, "github-copilot", root / ".github/hooks", "project", limit_hits=limit_hits)
        for client, relative in (
            ("cline", ".clinerules/hooks"),
            ("cline-cli", ".cline/hooks"),
            ("opencode", ".opencode/plugins"),
        ):
            _config_dir(items, client, root / relative, "audit-only", "*", "script", limit_hits=limit_hits)
    for extra in extras:
        _add_target(items, "unknown", extra.expanduser(), "audit-only")
    _record_limit_hit(limit_hits, "targets", len(items), MAX_TARGETS)
    return list(items.values())[:MAX_TARGETS]


class _DuplicateConfigMember(ValueError):
    """The JSON configuration cannot be interpreted without discarding a member."""


def _read_config(path: Path) -> tuple[bytes, object]:
    def unique_members(pairs: list[tuple[str, object]]) -> dict[str, object]:
        members = dict(pairs)
        if len(members) != len(pairs):
            raise _DuplicateConfigMember
        return members

    raw = path.read_bytes()
    if len(raw) > MAX_FILE_BYTES:
        raise ValueError("configuration exceeds the supported size limit")
    return raw, json.loads(raw.decode("utf-8-sig"), object_pairs_hook=unique_members)


def _render_config(data: object, old: bytes) -> bytes:
    # Preserve BOM/newline shape; keep unknown keys and values.
    bom = b"\xef\xbb\xbf" if old.startswith(b"\xef\xbb\xbf") else b""
    newline = "\r\n" if b"\r\n" in old else "\n"
    trailing = bool(old.endswith((b"\n", b"\r")))
    text = json.dumps(data, ensure_ascii=False, indent=2)
    text = text.replace("\n", newline)
    return bom + (text + (newline if trailing else "")).encode("utf-8")


def _write_backup(path: Path, backup_root: Path, source: bytes) -> Path:
    # Backups contain the entire original hook config, possibly user secrets.
    # Never redirect them through a symbolic-link or Windows reparse directory.
    for parent in (backup_root, *backup_root.parents):
        if parent.exists() and (
            parent.is_symlink() or getattr(parent.lstat(), "st_file_attributes", 0) & 0x400
        ):
            raise ValueError("unsafe backup directory; original configuration untouched")
    backup_root.mkdir(mode=0o700, parents=True, exist_ok=True)
    label = re.sub(r"[^a-zA-Z0-9._-]", "_", path.name)
    name = f"{label}.{hashlib.sha256(str(path).encode()).hexdigest()[:12]}.{uuid.uuid4().hex}.bak"
    destination = backup_root / name
    with destination.open("xb") as handle:
        handle.write(source)
        handle.flush()
        os.fsync(handle.fileno())
    os.chmod(destination, 0o600)
    return destination


def _atomic_update(path: Path, before: bytes, updated: bytes) -> None:
    # A backup was written first; refuse concurrent changes. No symlink writes.
    if not _safe_file(path) or path.read_bytes() != before:
        raise RuntimeError("configuration changed during review; no edit made")
    stage = path.with_name(path.name + ".handbook-stage-" + uuid.uuid4().hex)
    try:
        with stage.open("xb") as output:
            output.write(updated)
            output.flush()
            os.fsync(output.fileno())
        os.chmod(stage, stat.S_IMODE(path.stat().st_mode))
        if path.read_bytes() != before:
            raise RuntimeError("configuration changed before atomic replacement")
        os.replace(stage, path)
    finally:
        if stage.exists():
            stage.unlink()


def run(*, home: Path | None, projects: list[Path], extras: list[Path],
        apply: bool, clients_stopped: bool) -> dict:
    if apply and not clients_stopped:
        raise ValueError("--apply requires --clients-stopped; close affected agents first")
    use_environment = home is None
    home = (home or Path.home()).expanduser().absolute()
    script = _client_home(home, ".codex", "CODEX_HOME", use_environment).absolute()
    script = script / "handbook-bootstrap" / "handbook_update.py"
    limit_hits: list[dict] = []
    targets = discover(home, projects, extras, use_environment=use_environment, limit_hits=limit_hits)
    result = {"schema": AUDIT_SCHEMA, "mode": "apply" if apply else "audit",
              "checked": 0, "owned_entries": 0, "suspected_entries": 0, "opaque_entries": 0,
              "coverage": {"user_paths": "KNOWN_LOCAL_PATHS_ONLY",
                           "project_paths": "EXPLICIT_PROJECT_ARGUMENTS_ONLY",
                           "managed_remote_hooks": "NOT_INSPECTED",
                           "plugin_runtime_state": "NOT_VERIFIED",
                           "opaque_platform_commands": "CONTENT_NOT_INSPECTED",
                           "unknown_coding_clients": "NOT_INSPECTED",
                           "limit_hits": limit_hits},
              "changed_files": [], "findings": [], "warnings": []}
    backup_root = home / ".agents" / "handbook-hook-backups"
    for target in targets:
        if not target.path.exists():
            continue
        if not _safe_file(target.path):
            result["warnings"].append({"client": target.client, "path": str(target.path),
                                       "issue": "unsafe, linked, oversized or unreadable; skipped"})
            continue
        result["checked"] += 1
        try:
            if target.kind != "json":
                content = target.path.read_text(encoding="utf-8", errors="replace")
                if _looks_like_handbook_hook(content):
                    result["suspected_entries"] += 1
                    result["findings"].append({"client": target.client, "scope": target.scope,
                        "path": str(target.path), "classification": "REVIEW_SCRIPT_ONLY"})
                continue
            raw, data = _read_config(target.path)
            if not isinstance(data, dict):
                raise ValueError("JSON root is not an object")
            hooks = data.get("hooks", {})
            suspected = opaque = 0
            exact_standalone_seen = False
            for field, command, standalone in _commands(hooks):
                if field == "commandWindows" and re.search(r"\s-encodedcommand\s", command, re.I):
                    opaque += 1
                elif _looks_like_handbook_hook(command):
                    if standalone and is_owned_bootstrap_command(command, script):
                        exact_standalone_seen = True
                    else:
                        suspected += 1
            result["opaque_entries"] += opaque
            if opaque:
                result["findings"].append({"client": target.client, "scope": target.scope,
                    "path": str(target.path), "classification": "REVIEW_OPAQUE_PLATFORM_COMMAND",
                    "count": opaque})
            try:
                rewritten, owned = strip_config(data, script)
                if exact_standalone_seen:
                    # An exact spelling is review-only if it survives the scoped edit preview.
                    suspected += sum(
                        standalone and is_owned_bootstrap_command(command, script)
                        for _, command, standalone in _commands(rewritten.get("hooks", {}))
                    )
            finally:
                result["suspected_entries"] += suspected
                if suspected:
                    result["findings"].append({"client": target.client, "scope": target.scope,
                        "path": str(target.path), "classification": "REVIEW_UNKNOWN_HOOK",
                        "count": suspected})
            result["owned_entries"] += owned
            if owned:
                result["findings"].append({"client": target.client, "scope": target.scope,
                    "path": str(target.path), "classification": (
                        "REMOVABLE_EXACT_HANDBOOK_HOOK" if target.editable else "PROJECT_REVIEW_REQUIRED"),
                    "count": owned})
            if not (apply and owned and target.editable):
                continue
            backup = _write_backup(target.path, backup_root, raw)
            _atomic_update(target.path, raw, _render_config(rewritten, raw))
            result["changed_files"].append({"client": target.client, "path": str(target.path),
                                            "removed": owned, "backup": str(backup)})
        except (OSError, UnicodeError, ValueError, RuntimeError, RecursionError) as error:
            # Do not echo config content, tokens or commands to diagnostics.
            issue = "duplicate JSON member" if isinstance(error, _DuplicateConfigMember) else type(error).__name__
            result["warnings"].append({"client": target.client, "path": str(target.path),
                                       "issue": issue, "action": "not modified"})
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Offline audit of coding-agent Handbook hooks")
    parser.add_argument("--home", type=Path, help="Use user paths under this root, ignoring client home overrides")
    parser.add_argument("--project", type=Path, action="append", default=[],
                        help="Explicit workspace to AUDIT; project configs are never modified")
    parser.add_argument("--extra-file", type=Path, action="append", default=[],
                        help="Additional file to AUDIT read-only")
    parser.add_argument("--apply", action="store_true",
                        help="Remove exact owned Handbook hooks in recognized USER JSON files")
    parser.add_argument("--clients-stopped", action="store_true",
                        help="Confirm all affected coding-agent clients were fully stopped")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        report = run(home=args.home, projects=args.project, extras=args.extra_file,
                     apply=args.apply, clients_stopped=args.clients_stopped)
    except (ValueError, OSError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"Mode: {report['mode']}; files checked: {report['checked']}; "
              f"exact owned hooks: {report['owned_entries']}; "
              f"uncertain findings: {report['suspected_entries']}; "
              f"opaque platform commands: {report['opaque_entries']}; "
              f"files changed: {len(report['changed_files'])}")
        limit_hits = report["coverage"]["limit_hits"]
        if limit_hits:
            print("  Coverage: partial local inventory. "
                  "See --json for exceeded candidate limits, counts, and locations.")
        for finding in report["findings"]:
            print(f"  {finding['classification']}: {finding['client']} {finding['path']}")
        for warning in report["warnings"]:
            print(f"  WARNING {warning['client']}: {warning['path']} ({warning['issue']})")
        for change in report["changed_files"]:
            print(f"  BACKUP: {change['backup']}")
    return 0 if not report["warnings"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
