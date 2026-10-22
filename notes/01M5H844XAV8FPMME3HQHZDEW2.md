---
title: "ghq migrate 把位置不对的仓搬回 ghq 目录结构"
display: true
tags:
  - ghq
  - git
date: 2026-10-22
---

`ghq migrate <目录>` 把一个已经 clone 下来、但不在 ghq 目录结构里的仓，按它的 remote URL 挪到 `<ghq root>/<host>/<owner>/<repo>`。

典型场景：当初 `ghq get` 时 URL 写错了（比如多打一段 `owner/`），仓落到了嵌套路径，`ghq list` 里看着别扭，按 owner 分类的脚本也会分错。不用删了重 clone：

```bash
ghq migrate --dry-run -y ~/ghq/github.com/alice/alice/bob/repo   # 先看会挪到哪
ghq migrate -y ~/ghq/github.com/alice/alice/bob/repo
```

它只读 remote URL 推目标路径，不碰内容、不碰 remote。所以 remote 本身是错的（比如指错了 owner），migrate 只会把错误原样搬过去 —— 先 `git remote set-url` 改对再 migrate。

拒绝搬 worktree 和 submodule（`.git` 是文件而非目录，单独挪会断链）。
