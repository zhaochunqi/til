#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
import os
import re
import sys
import hashlib
from datetime import datetime
from pathlib import Path
from urllib.parse import quote

WORKDIR = Path(__file__).resolve().parent.parent
NOTES_DIR = WORKDIR / "notes"
README_PATH = WORKDIR / "README.md"

# Use Terraform-like markers
MARKER_START = "<!-- BEGINNING OF NOTES INDEX HOOK -->"
MARKER_END = "<!-- END OF NOTES INDEX HOOK -->"
# Backward compatibility: older markers that we may replace
OLD_MARKERS = [
    ("<!-- notes:start -->", "<!-- notes:end -->"),
]

FRONT_MATTER_RE = re.compile(r"^---\n(.*?)\n---\n?", re.DOTALL)
HEADING_RE = re.compile(r"^#\s+(.+)$", re.MULTILINE)

DATE_RE = re.compile(r"^\s*date:\s*([0-9]{4}-[0-9]{2}-[0-9]{2})\s*$", re.MULTILINE)
TITLE_RE = re.compile(r"^\s*title:\s*[\"']?(.+?)[\"']?\s*$", re.MULTILINE)
DISPLAY_RE = re.compile(
    r"^\s*display:\s*(true|false)\s*$", re.MULTILINE | re.IGNORECASE
)
# Support both list and single string formats for tags
TAGS_BLOCK_RE = re.compile(r"^\s*tags:\s*(\n(?:\s*-\s*.+\n?)+)", re.MULTILINE)
TAGS_INLINE_RE = re.compile(r"^\s*tags:\s*\[(.*?)\]\s*$", re.MULTILINE)


def parse_front_matter(text: str):
    tags = []
    date = None
    display = True

    m = FRONT_MATTER_RE.search(text)
    if not m:
        return tags, date, display
    fm = m.group(1)

    # date
    dm = DATE_RE.search(fm)
    if dm:
        date = dm.group(1)

    # display
    dpm = DISPLAY_RE.search(fm)
    if dpm:
        display = dpm.group(1).lower() == "true"

    # tags - block style
    bm = TAGS_BLOCK_RE.search(fm)
    if bm:
        block = bm.group(1)
        for line in block.splitlines():
            line = line.strip()
            if line.startswith("- "):
                tag = line[2:].strip()
                if tag:
                    tags.append(tag)
    else:
        # tags - inline style [a, b, c]
        im = TAGS_INLINE_RE.search(fm)
        if im:
            inner = im.group(1)
            for part in inner.split(","):
                tag = part.strip().strip("\"'")
                if tag:
                    tags.append(tag)

    return tags, date, display
    fm = m.group(1)

    # date
    dm = DATE_RE.search(fm)
    if dm:
        date = dm.group(1)

    # tags - block style
    bm = TAGS_BLOCK_RE.search(fm)
    if bm:
        block = bm.group(1)
        for line in block.splitlines():
            line = line.strip()
            if line.startswith("- "):
                tag = line[2:].strip()
                if tag:
                    tags.append(tag)
    else:
        # tags - inline style [a, b, c]
        im = TAGS_INLINE_RE.search(fm)
        if im:
            inner = im.group(1)
            for part in inner.split(","):
                tag = part.strip().strip("\"'")
                if tag:
                    tags.append(tag)

    return tags, date


def extract_title(text: str, fallback: str) -> str:
    # First try to extract title from YAML front matter
    m = FRONT_MATTER_RE.search(text)
    if m:
        fm = m.group(1)
        tm = TITLE_RE.search(fm)
        if tm:
            return tm.group(1).strip()

    # Fallback to first level-1 heading after front matter; fallback to filename stem
    t = FRONT_MATTER_RE.sub("", text, count=1)
    hm = HEADING_RE.search(t)
    if hm:
        return hm.group(1).strip()
    return fallback


def slugify(s: str) -> str:
    # ASCII-only slug: lowercase, replace whitespace with hyphens, strip non-alnum
    s = s.strip().lower()
    s = re.sub(r"\s+", "-", s)
    s = re.sub(r"[^a-z0-9\-]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s or "tag"


def anchor_id_for_tag(tag: str) -> str:
    base = slugify(tag)
    if re.fullmatch(r"[a-z0-9\-]+", base):
        return base
    # Fallback to a hash-based ASCII id for non-ascii-heavy tags
    digest = hashlib.sha1(tag.encode("utf-8")).hexdigest()[:8]
    return f"tag-{digest}"


def collect_notes():
    entries = []
    if not NOTES_DIR.exists():
        return entries
    for root, _dirs, files in os.walk(NOTES_DIR):
        for fname in files:
            if not fname.lower().endswith(".md"):
                continue
            fpath = Path(root) / fname
            try:
                text = fpath.read_text(encoding="utf-8")
            except Exception:
                continue
            tags, date, display = parse_front_matter(text)
            if not display:
                continue
            title = extract_title(text, fallback=fpath.stem)
            rel_path = fpath.relative_to(WORKDIR).as_posix()

            # Normalize date to comparable form; allow None
            dt_sort = None
            if date:
                try:
                    dt_sort = datetime.strptime(date, "%Y-%m-%d")
                except ValueError:
                    dt_sort = None

            # File modification time as fallback for last-updated computation
            try:
                mtime = datetime.fromtimestamp(fpath.stat().st_mtime)
            except Exception:
                mtime = None

            entries.append(
                {
                    "path": rel_path,
                    "title": title,
                    "tags": tags or [],
                    "date": date,
                    "dt_sort": dt_sort,
                    "mtime": mtime,
                }
            )
    return entries
    for root, _dirs, files in os.walk(NOTES_DIR):
        for fname in files:
            if not fname.lower().endswith(".md"):
                continue
            fpath = Path(root) / fname
            try:
                text = fpath.read_text(encoding="utf-8")
            except Exception:
                continue
            tags, date = parse_front_matter(text)
            title = extract_title(text, fallback=fpath.stem)
            rel_path = fpath.relative_to(WORKDIR).as_posix()

            # Normalize date to comparable form; allow None
            dt_sort = None
            if date:
                try:
                    dt_sort = datetime.strptime(date, "%Y-%m-%d")
                except ValueError:
                    dt_sort = None

            # File modification time as fallback for last-updated computation
            try:
                mtime = datetime.fromtimestamp(fpath.stat().st_mtime)
            except Exception:
                mtime = None

            entries.append(
                {
                    "path": rel_path,
                    "title": title,
                    "tags": tags or [],
                    "date": date,
                    "dt_sort": dt_sort,
                    "mtime": mtime,
                }
            )
    return entries


def compute_last_updated(entries):
    latest = None
    for e in entries:
        candidate = e["dt_sort"] or e["mtime"]
        if candidate is None:
            continue
        if latest is None or candidate > latest:
            latest = candidate
    return latest


def render_section(entries):
    # Group by tag; if no tags, group under 'untagged'
    by_tag = {}
    for e in entries:
        ts = e["tags"] or ["untagged"]
        for tag in ts:
            by_tag.setdefault(tag, []).append(e)

    # Sort tags alphabetically case-insensitive
    tag_keys = sorted(by_tag.keys(), key=lambda s: s.lower())

    lines = []
    lines.append("## Notes by Tag")
    lines.append("")

    # Stable last updated: based on latest note date or file mtime, day precision
    last_updated_dt = compute_last_updated(entries)
    if last_updated_dt is not None:
        lines.append(f"Last updated: {last_updated_dt.strftime('%Y-%m-%d')}")
        lines.append("")

    if not tag_keys:
        lines.append("(No notes found)")
        return "\n".join(lines) + "\n"

    # Tag navigation
    lines.append("### Tags")
    for tag in tag_keys:
        aid = anchor_id_for_tag(tag)
        lines.append(f"- [{tag}](#{aid})")
    lines.append("")

    for tag in tag_keys:
        aid = anchor_id_for_tag(tag)
        # Explicit anchor for compatibility across renderers
        lines.append(f'<a id="{aid}"></a>')
        lines.append(f"### {tag}")
        # Sort entries by date desc then title
        items = sorted(
            by_tag[tag],
            key=lambda e: (
                (e["dt_sort"] or e["mtime"] or datetime.min),
                e["title"].lower(),
            ),
            reverse=True,
        )
        for e in items:
            enc_path = quote(e["path"], safe="/-_.()~")
            if e["date"]:
                lines.append(f"- [{e['title']}]({enc_path}) - {e['date']}")
            else:
                # If no date, but we have mtime, show YYYY-MM-DD from mtime
                if e["mtime"]:
                    lines.append(
                        f"- [{e['title']}]({enc_path}) - {e['mtime'].strftime('%Y-%m-%d')}"
                    )
                else:
                    lines.append(f"- [{e['title']}]({enc_path})")
        lines.append("")

    return "\n".join(lines)


def _replace_block(text: str, start: str, end: str, section_md: str):
    pattern = re.compile(re.escape(start) + r"[\s\S]*?" + re.escape(end), re.MULTILINE)
    new_block = start + "\n" + section_md.rstrip() + "\n" + end
    if pattern.search(text):
        return pattern.sub(new_block, text)
    return None


def update_readme(section_md: str):
    if not README_PATH.exists():
        content = [
            "# TIL - Today I Learn",
            "",
            MARKER_START,
            section_md,
            MARKER_END,
            "",
        ]
        README_PATH.write_text("\n".join(content), encoding="utf-8")
        return

    readme = README_PATH.read_text(encoding="utf-8")

    # Try replacing new markers first
    updated = _replace_block(readme, MARKER_START, MARKER_END, section_md)

    # If not present, try replacing any old markers
    if updated is None:
        for s, e in OLD_MARKERS:
            updated = _replace_block(readme, s, e, section_md)
            if updated is not None:
                # Also rename markers to new ones
                updated = updated.replace(s, MARKER_START).replace(e, MARKER_END)
                break

    # If still not present, append block to end
    if updated is None:
        sep = "\n" if readme.endswith("\n") else "\n\n"
        updated = (
            readme
            + sep
            + MARKER_START
            + "\n"
            + section_md.rstrip()
            + "\n"
            + MARKER_END
            + "\n"
        )

    if updated != readme:
        README_PATH.write_text(updated, encoding="utf-8")


def main():
    entries = collect_notes()
    section = render_section(entries)
    update_readme(section)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
