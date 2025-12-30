---
title: "direnv 配合 rbw 一起使用"
tags:
  - bitwarden
  - direnv
  - env
  - rbw
date: 2025-12-15
---

`direnv` 配合 `rbw` 平常用起来很好用，还不用担心密钥硬编码到代码中泄露。

```bash
export TF_VAR_ntfy_token=$(rbw get ntfy_github_action_token)
export TF_VAR_gmail_token=$(rbw get gmail_github_action_token)
```

## ⚠️ **重要注意**
我在 macos 下配合 rbw 会有很大延迟 (解锁之后使用 rbw get 有时候会有接近 10s 的延迟),我研究发现是因为 `rbw` 的获取 `ttyname()` 有性能问题。

**请在 `.zshrc` 中添加以下环境变量来解决这个问题：**

```bash
export RBW_TTY=$(tty)
```

配置后响应时间可缩短到 1 秒内。

相关：[修复 macos 下使用 rbw 获取密钥卡顿](https://til.zhaochunqi.com/01kd8h0c73kvssnap9gfmmf46j)]
