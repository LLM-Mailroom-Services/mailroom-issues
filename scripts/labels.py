#!/usr/bin/env python3
"""GitHub label taxonomy sync driver (issue hub).

Keeps this repository's GitHub labels in lockstep with the declarative
taxonomy in ``.github/labels.json``. The manifest is the source of truth:
every label the hub's routing workflow uses (``type/*``, ``domain/*``,
``priority/*``, ``status/*`` and the GitHub lifecycle labels) is created or
updated from it — never hand-edited on GitHub.

Usage:
    python scripts/labels.py sync  [--dry-run] [--repo OWNER/NAME] [--json]
    python scripts/labels.py audit [--repo OWNER/NAME] [--json]

  sync   create missing labels, update drifted color/description, no-op on match
  audit  report drift without writing: manifest labels missing from the repo
         (exit 1) and repo labels absent from the manifest (informational)

Commands are read-only unless ``sync`` runs without ``--dry-run``. Requires
``gh`` authenticated against the target repo (``GH_TOKEN`` / ``GITHUB_TOKEN``).
Stdlib only.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST = REPO_ROOT / ".github" / "labels.json"

DEFAULT_REPO = "LLM-Mailroom-Services/mailroom-issues"


def run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=REPO_ROOT, check=False, text=True, capture_output=True)


def load_manifest() -> dict:
    if not MANIFEST.is_file():
        raise SystemExit(f"manifest missing: {MANIFEST}")
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    labels = data.get("labels")
    if not isinstance(labels, list) or not labels:
        raise SystemExit(f"manifest has no labels: {MANIFEST}")
    names = [entry["name"] for entry in labels]
    dupes = sorted({n for n in names if names.count(n) > 1})
    if dupes:
        raise SystemExit(f"manifest duplicate label names: {dupes}")
    return data


def default_repo() -> str:
    result = run(["git", "remote", "get-url", "origin"])
    url = result.stdout.strip() if result.returncode == 0 else ""
    if url.endswith(".git"):
        url = url[:-4]
    if "github.com" in url:
        return url.split("github.com")[-1].lstrip(":/")
    return DEFAULT_REPO


def repo_labels(repo: str) -> dict[str, dict]:
    result = run(["gh", "label", "list", "--repo", repo, "--json", "name,color,description", "--limit", "500"])
    if result.returncode != 0:
        err = (result.stderr or result.stdout or "").strip()
        # Do not echo env/token material — gh errors are usually auth/permission.
        raise SystemExit(
            f"gh label list failed (exit {result.returncode}). "
            f"Ensure GH_TOKEN/GITHUB_TOKEN is set for this job.\n{err}"
        )
    return {entry["name"]: entry for entry in json.loads(result.stdout or "[]")}


def norm(value: str | None) -> str:
    return (value or "").strip()


def diff_labels(manifest: dict, existing: dict[str, dict]) -> tuple[list[dict], list[dict], list[str]]:
    """Return (creates, updates, extras).

    creates: manifest labels absent from the repo.
    updates: manifest labels present but with drifted color/description.
    extras:  repo labels absent from the manifest (never touched — deletion
             is out of scope so open issues never lose their flair).
    """
    creates, updates = [], []
    for entry in manifest["labels"]:
        name, color, desc = entry["name"], norm(entry["color"]), norm(entry.get("description"))
        current = existing.get(name)
        if current is None:
            creates.append(entry)
            continue
        # GitHub stores colors lowercased; compare case-insensitively.
        if norm(current.get("color")).lstrip("#").lower() != color.lower() or norm(current.get("description")) != desc:
            updates.append(entry)
    extras = sorted(set(existing) - {e["name"] for e in manifest["labels"]})
    return creates, updates, extras


def append_step_summary(markdown: str) -> None:
    """Append neat markdown to the Actions job summary when available."""
    path = os.environ.get("GITHUB_STEP_SUMMARY")
    if not path:
        return
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(markdown)
        if not markdown.endswith("\n"):
            fh.write("\n")


def cmd_sync(args: argparse.Namespace) -> int:
    manifest = load_manifest()
    existing = repo_labels(args.repo)
    creates, updates, extras = diff_labels(manifest, existing)

    if args.json:
        print(json.dumps({"repo": args.repo, "create": [c["name"] for c in creates],
                          "update": [u["name"] for u in updates], "extras": extras,
                          "dry_run": args.dry_run}, indent=2))
    else:
        print(f"### Label sync — `{args.repo}`")
        print()
        if creates:
            print("**Create**")
            for entry in creates:
                print(f"- `{entry['name']}` `#{entry['color']}`")
            print()
        if updates:
            print("**Update**")
            for entry in updates:
                print(f"- `{entry['name']}` `#{entry['color']}`")
            print()
        if extras:
            print("**Extras** (in repo, not in manifest — informational)")
            for name in extras:
                print(f"- `{name}`")
            print()
        if not creates and not updates:
            print(f"✅ In sync: **{len(manifest['labels'])}** labels match `{args.repo}`")

    summary_lines = [
        f"## Label sync — `{args.repo}`",
        "",
        f"| Metric | Count |",
        f"| --- | ---: |",
        f"| Create | {len(creates)} |",
        f"| Update | {len(updates)} |",
        f"| Extras (informational) | {len(extras)} |",
        f"| Manifest total | {len(manifest['labels'])} |",
        "",
    ]
    if creates:
        summary_lines.append("### Create")
        for entry in creates:
            summary_lines.append(f"- `{entry['name']}`")
        summary_lines.append("")
    if updates:
        summary_lines.append("### Update")
        for entry in updates:
            summary_lines.append(f"- `{entry['name']}`")
        summary_lines.append("")
    if extras:
        summary_lines.append("### Extras (informational)")
        for name in extras:
            summary_lines.append(f"- `{name}`")
        summary_lines.append("")
    if not creates and not updates:
        summary_lines.append(f"✅ In sync with manifest ({len(manifest['labels'])} labels).")
        summary_lines.append("")
    if args.dry_run:
        summary_lines.append("_Dry run — nothing written._")
        summary_lines.append("")
    append_step_summary("\n".join(summary_lines))

    if args.dry_run:
        print("dry run — nothing written", file=sys.stderr)
        return 0

    failures = 0
    update_names = {entry["name"] for entry in updates}
    for entry in creates + updates:
        cmd = ["gh", "label", "create", entry["name"], "--repo", args.repo,
               "--color", entry["color"], "--description", entry.get("description") or ""]
        if entry["name"] in update_names:
            cmd[2] = "edit"
        result = run(cmd)
        if result.returncode != 0:
            failures += 1
            err = (result.stderr or "").strip()
            print(f"FAILED  {entry['name']}: {err}", file=sys.stderr)
            print(f"::error title=Label sync failed::{entry['name']}: {err}")
    verb = "created/updated" if (creates or updates) else "no changes to"
    print(f"synced {args.repo}: {len(creates)} created, {len(updates)} updated ({verb})")
    return 1 if failures else 0


def cmd_audit(args: argparse.Namespace) -> int:
    manifest = load_manifest()
    existing = repo_labels(args.repo)
    creates, updates, extras = diff_labels(manifest, existing)
    missing = creates + updates  # audit counts drifted labels as missing-from-truth

    payload = {"repo": args.repo, "missing_or_drifted": [e["name"] for e in missing],
               "extras": extras, "in_sync": not missing}
    if args.json:
        print(json.dumps(payload, indent=2))
        # Still write a short summary for Actions UI when present
        status = "✅ in sync" if not missing else f"❌ {len(missing)} missing/drifted"
        append_step_summary(
            f"## Label audit — `{args.repo}`\n\n**Result:** {status}\n"
        )
        return 0 if not missing else 1

    print(f"### Label audit — `{args.repo}`")
    print()

    summary_lines = [
        f"## Label audit — `{args.repo}`",
        "",
    ]

    if missing:
        print(f"❌ **DRIFT:** {len(missing)} manifest label(s) missing or drifted")
        print()
        print("| Status | Label |")
        print("| --- | --- |")
        for entry in missing:
            kind = "drifted" if entry["name"] in existing else "missing"
            print(f"| {kind} | `{entry['name']}` |")
        print()
        print(f"**Fix:** `python scripts/labels.py sync --repo {args.repo}`")

        summary_lines.extend(
            [
                f"❌ **DRIFT:** {len(missing)} manifest label(s) missing or drifted",
                "",
                "| Status | Label |",
                "| --- | --- |",
            ]
        )
        for entry in missing:
            kind = "drifted" if entry["name"] in existing else "missing"
            summary_lines.append(f"| {kind} | `{entry['name']}` |")
        summary_lines.extend(
            [
                "",
                f"**Fix:** `python scripts/labels.py sync --repo {args.repo}`",
                "",
            ]
        )
        if extras:
            summary_lines.append(
                f"_Also: {len(extras)} repo label(s) not in manifest (informational)._"
            )
            summary_lines.append("")

        print(
            f"::error title=Label manifest drift::"
            f"{len(missing)} label(s) missing or drifted in {args.repo}"
        )
        append_step_summary("\n".join(summary_lines))
        return 1

    print(f"✅ **In sync:** {len(manifest['labels'])} manifest labels present in `{args.repo}`")
    summary_lines.append(
        f"✅ **In sync:** {len(manifest['labels'])} manifest labels present."
    )
    summary_lines.append("")
    if extras:
        print()
        print(f"ℹ️ **Note:** {len(extras)} repo label(s) not in manifest (informational):")
        for name in extras:
            print(f"- `{name}`")
        summary_lines.append(
            f"ℹ️ **Note:** {len(extras)} repo label(s) not in manifest (informational):"
        )
        for name in extras:
            summary_lines.append(f"- `{name}`")
        summary_lines.append("")
    append_step_summary("\n".join(summary_lines))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)

    def add_common(p: argparse.ArgumentParser) -> None:
        p.add_argument("--repo", default=None, help="OWNER/NAME (default: git origin)")
        p.add_argument("--json", action="store_true", help="machine-readable output")

    p_sync = sub.add_parser("sync", help="create/update labels from the manifest")
    p_sync.add_argument("--dry-run", action="store_true", help="show actions without writing")
    add_common(p_sync)
    p_sync.set_defaults(func=cmd_sync)

    p_audit = sub.add_parser("audit", help="report manifest<->repo drift (exit 1 on missing/drifted)")
    add_common(p_audit)
    p_audit.set_defaults(func=cmd_audit)

    args = parser.parse_args(argv)
    if args.repo is None:
        args.repo = default_repo()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
