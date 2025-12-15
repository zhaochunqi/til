---
title: "git delete remote branches"
tags:
  - git
date: 2025-12-15
---

## 获取远端分支   

> Fetch the latest changes from the default remote upstream repository (if set)

```bash
git fetch
```

## 查看所有分支

> List all branches (local and remote; the current branch is highlighted by *):

```bash
git branch --all
```

## 删除远端分支

```bash
git push origin --delete <branch_name>
```

## 删除本地分支

```bash
git branch -d <branch_name>
```