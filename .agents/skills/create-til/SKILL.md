---
name: create-til
description: 添加新的 TIL 笔记
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: documentation
---

## 功能

`just new "标题"` 生成笔记入口（ULID 文件名 + front matter），然后按下述风格写正文。

## 风格

**标题就是需求那一句**：单一主题，不要「以及…」这类并列——写不成一句话就拆成两篇。≤50 字。

**正文三段式**：

1. **需求** —— 什么场景、要达成什么。一两句开门见山，不铺垫技术细节。
2. **原因** —— 为什么现成做法不行。结论先行（根因一句话），再给必要依据。
3. **解法** —— 可直接复制的配置或命令，配关键说明。

**不写**：排查过程、踩坑清单、个人取舍、结尾总结。这些让读者自己踩。看起来更对但走不通的做法，在括号里一句带过即可，不单独成段。

**其他**：tags 用英文；正文中文，技术术语保留英文；代码真实可跑，域名/IP/凭据脱敏。

小节标题可选，用就用 `## 需求` / `## 原因` / `## 解法`，短篇直接连着写。

## 模板

```markdown
---
title: "需求那一句"
display: true
tags:
  - tag1
  - tag2
date: YYYY-MM-DD
---

## 需求

什么场景、要达成什么。

## 原因

根因一句话。为什么现成做法不行（看起来更对的做法在这里括号带过）。

## 解法

可直接复制的配置或命令。

关键说明。
```

## 收口

写完跑 `just maintain`（normalize front matter + 重排 README 索引）再提交。pre-commit 还会跑 autocorrect、索引生成和链接检查。
