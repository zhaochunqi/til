#!/usr/bin/env python3
"""检查 notes/ 里的跨笔记链接：必须是 notes/<ULID>.md 且目标文件存在。

相对路径不能用（站点搜索页把正文渲染在 /search/ 下，会按页面 URL 解析）；站点侧由
til-astro-build 的 remark 插件改写成 /<ulid>/。
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)\)")  # (?<!!) 跳过图片 ![..](..)
ULID_NOTE = re.compile(r"^notes/[0-9A-HJKMNP-TV-Z]{26}\.md$")
SCHEME = re.compile(r"^[a-z][a-z0-9+.-]*:")


def main() -> int:
    problems: list[str] = []
    for path in sorted((ROOT / "notes").glob("*.md")):
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            for target in LINK.findall(line):
                if SCHEME.match(target) or target.startswith("#"):
                    continue
                rel = path.relative_to(ROOT)
                if not ULID_NOTE.match(target):
                    problems.append(f"{rel}:{lineno}: 本地链接要写成 notes/<ULID>.md → {target}")
                elif not (ROOT / target).is_file():
                    problems.append(f"{rel}:{lineno}: 目标不存在 → {target}")

    for problem in problems:
        print(problem)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
