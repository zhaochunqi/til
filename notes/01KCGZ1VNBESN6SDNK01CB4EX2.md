---
title: "direnv 配合 rbw 一起使用"
tags:
  - direnv
  - rbw
date: 2025-12-15
---

`direnv` 配合 `rbw` 平常用起来很好用，还不用担心密钥硬编码到代码中泄露。

```bash
export TF_VAR_ntfy_token=$(rbw get ntfy_github_action_token)
export TF_VAR_gmail_token=$(rbw get gmail_github_action_token)
```

## 备注
我在 macos 下配合 rbw 会有很大延迟 (解锁之后使用 rbw get 有时候会有接近 10s 的延迟),我研究发现是因为 `rbw` 的获取 `ttyname()` 有性能问题，在 `.zshrc` 中配置 `export RBW_TTY=$(tty)` 即可 (1s 内)。