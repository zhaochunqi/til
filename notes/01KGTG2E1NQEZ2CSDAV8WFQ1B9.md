---
title: "git diff 别名: 用 ds 调用 delta"
display: true
tags:
  - delta
  - git
date: 2026-02-07
---

AI 时代 LLM 经常需要读取 git diff，默认行为不要用 delta 修改。

[Delta](https://github.com/dandavison/delta) 安装时可能会自动添加配置：

```bash
[core]
    pager = delta
```

需要先移除这个配置，然后在 `.gitconfig` 中添加：

```bash
[alias]
    ds = -c pager.diff=delta diff
```

- `git diff` 保持原生格式，便于 LLM 读取
- `git ds` 查看带 delta 的漂亮 diff 效果
