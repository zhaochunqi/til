---
title: "修改 Git 默认主分支为 main"
display: true
tags:
  - git
date: 2026-01-19
---

将 Git 仓库的默认分支从 master 修改为 main。

```bash
# 重命名本地分支
git branch -m master main

# 获取远程更新
git fetch origin

# 设置本地 main 分支跟踪远程 main 分支
git branch -u origin/main main

# 设置远程仓库的默认分支
git remote set-head origin -a
```

