---
title: "Go CLI 工具更适合通过 Homebrew Cask 分发预编译二进制"
display: true
tags:
  - go
  - homebrew
  - macos
date: 2026-01-15
---

**Formula** 用于从源码编译，**Cask** 用于分发预编译二进制。

Homebrew 团队希望统一 CLI 和 GUI 的安装体验，推动 `brew install` 作为唯一入口。因此 GoReleaser 官方推荐使用 Cask：

- 安装更快（无编译过程）
- 自动化程度更高
- 符合 Homebrew 官方发展方向

**何时用 Cask**：Go CLI 工具官方通常提供预编译二进制。

**何时用 Formula**：上游只提供源码、需要编译定制、或依赖本地库的软件。

自定义 tap 可同时包含两者：
```bash
# Formula
brew install zhaochunqi/homebrew-tap/<tool>

# Cask
brew install --cask zhaochunqi/homebrew-tap/<tool>
```

参考：[GoReleaser v2.10 Blog Post](https://goreleaser.com/blog/goreleaser-v2.10/)