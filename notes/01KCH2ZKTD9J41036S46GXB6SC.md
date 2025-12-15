---
title: "删除 git 幽灵分支"
tags:
  - git
date: 2025-12-15
---

`git clone` 或 `git fetch` 的时候，git 会在本地创建一些"快照",记录远程仓库的最新状态，但这些不是真正的分支，当远端的 branch 删除之后，本地还会留着。

## 解决方法 1

```bash
git fetch --prune
```

## 解决方法 2

直接配置全局的 gitconfig 即可：

```bash
git config --global fetch.prune true
```