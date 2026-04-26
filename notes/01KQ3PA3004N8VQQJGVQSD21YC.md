---
title: "先学领域词汇再让 AI 干活"
display: true
tags:
  - ai
  - design
  - llm
  - ui
date: 2026-04-26
---

想让 AI 在不熟悉的领域里产出更好，先学那个领域的 glossary。

很多 vibecoding 前端看起来差，不一定是模型不会写，而是 prompt 里只有「菜单」「按钮」「页面」这种粗粒度词。换成更准确的 UI component 名称，模型会更容易命中它内部已经学过的 pattern。

例如不要只说：

```text
做一个有菜单和按钮的设置页。
```

先补一点 domain knowledge，再说：

```text
做一个 settings surface：
- 左侧用 sidebar navigation
- 顶部用 toolbar，包含 segmented control 和 search field
- 主区域用 form section、field group、select、switch、slider
- 危险操作放到 destructive action zone
- 保存状态用 inline validation 和 toast feedback
```

这不是堆术语，而是在给 LLM 更精确的索引词。对任何陌生领域都一样：先问 AI 或文档要一份 glossary，掌握关键概念和对象名，再开始让它做事。磨刀不误砍柴工。
