---
title: "gitignore 里 pattern 以 / 结尾的含义，以及 .terraform.lock.hcl 为什么不会被误伤"
display: true
tags:
  - git
  - terraform
date: 2026-10-12
---

TL,DR: gitignore 的 pattern 匹配**整段路径组件**（不是前缀），所以 `.terraform` 永远匹配不到
`.terraform.lock.hcl`；而 pattern 以 `/` 结尾表示**只匹配目录**。这是两套互相独立的机制，别混着理解。

## 两个容易混淆的语义

| pattern | 匹配目录 `.terraform/` | 匹配**普通文件** `.terraform` | 匹配 `.terraform.lock.hcl` |
| --- | --- | --- | --- |
| `.terraform` | ✅ | ✅ | ❌ |
| `.terraform/` | ✅ | ❌ | ❌ |

### ① 尾斜杠 = 只匹配目录

`gitignore(5)` 原文：

> If the pattern ends with a slash, it is removed for the purpose of the following description,
> but it would only find a match with a directory.

即 `foo/` 只匹配名为 `foo` 的**目录**（以及其下的路径），不匹配同名的普通文件或符号链接。
想忽略「某个缓存目录」时写尾斜杠，语义更准确。

### ② pattern 匹配整段组件，不是前缀

gitignore 的 pattern 是按路径组件（component）匹配的，**不做前缀匹配**：

```bash
printf '.terra\n' > .gitignore
git check-ignore -v .terraform.lock.hcl   # 无输出 —— 证明不是前缀匹配
```

所以 `.terraform`（无论有没有尾斜杠）都**不会**误伤 `.terraform.lock.hcl`。
推论：**别拿「怕误伤 lock 文件」当写尾斜杠的理由** —— 那是另一条机制在起作用。

## 怎么自己验

`git check-ignore -v <path>` 会打出命中的**规则文件 + 行号 + pattern**，是判断「到底哪条规则生效」
最可靠的方式：

```bash
git check-ignore -v some/sub/dir/.terraform/providers/x
# /home/you/.gitignore:26:.terraform/	some/sub/dir/.terraform/providers/x
```

它只对**未跟踪**文件有意义 —— ignore 规则本身也只作用于未跟踪文件，已入库的文件不受任何影响。

## 实用推论：全局忽略 Terraform / Terragrunt 缓存

放在 `~/.gitignore`（由 `core.excludesFile` 指定，通常用 chezmoi 管）：

```gitignore
.terraform/
.terragrunt-cache/
```

- 不带路径分隔符的 pattern 会在**任意层级**匹配（`some/sub/dir/.terraform/` 也命中），
  正好覆盖 monorepo 里每个子模块自己的 `.terraform/`。
- `.terraform.lock.hcl` 必须入库（Terraform Stack 与 module 仓都依赖它）—— 按上面的机制，它本来就安全。
- 为什么值得放全局：仓库自己那份 `.gitignore` 可能**只存在于某些分支**，切分支时该目录就失去保护
  （真实踩过：一次提交里混进了 300MB 的 provider 二进制，被 GitHub 的 100MB 单文件限制挡下）。
- 局限：全局 ignore **对别人不可见**，只保护本机。仓库自己的 `.gitignore` 仍是正解，
  全局这份是安全网，不是替代品。
- 需要时 `git add -f` 仍可强制添加。
