---
tags:
  - git
date: 2025-09-22
---
在 git config 中创建一个 alias, macOS 下位置在 `~/.gitconfig`

```gitconfig
[alias]
	nah = "!f(){ git reset --hard; git clean -xdf; if [ -d ".git/rebase-apply" ] || [ -d ".git/rebase-merge" ]; then git rebase --abort; fi; }; f"
```

然后后续的使用可以运行 `git nah` 即可