---
title: "gitignore 里 pattern 以 / 结尾只匹配目录"
display: true
tags:
  - git
date: 2026-10-12
---

想忽略某个缓存目录，又怕误伤同名前缀的文件（例如 `.terraform/` 与必须入库的 `.terraform.lock.hcl`）。

pattern 以 `/` 结尾时只匹配**目录**（及其下路径），不匹配同名的普通文件或符号链接：

```gitignore
.terraform/
```

不带斜杠的 `.terraform` 会连「名叫 `.terraform` 的普通文件」一起忽略。两种写法都不会误伤
`.terraform.lock.hcl` —— pattern 按整段路径组件匹配，不做前缀匹配。

用 `git check-ignore -v <path>` 确认到底哪条规则命中（它打出规则文件、行号与 pattern）。
