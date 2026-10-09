#!/usr/bin/env python3
"""检查 notes/ 里的本地链接：必须是 notes/<ULID>.md 且文件存在。

仓内的约定是「从仓根数」的路径（`notes/<ULID>.md`），因为消费方是 til-astro-build 的
remark 插件：它在构建时把这类链接改写成站内 `/<ulid>/`，所以站点从任何页面（含把整篇
正文渲染出来的 /search/）点都对。

代价是 GitHub 的 blob 视图解析不了这种写法（它按文件所在目录解析，会变成
notes/notes/…），这是有意接受的取舍。外链交给 lychee（见 lychee.toml 的 scheme 限制）。
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
