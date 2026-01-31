---
title: "homebrew cask install 与 brew bundle 的区别"
display: true
tags:
  - homebrew
  - macos
date: 2026-02-01
---

使用 `brew install` 命令安装某些 cask 软件时，可以省略 `cask` 关键字，直接 `brew install yaak` 也能安装成功。

但在使用 `brew bundle` 命令时，必须在 Brewfile 中明确指定 `cask` 关键字：

```ruby
# 正确写法
cask "yaak"

# 错误写法，会报错
brew "yaak"
```

原因：`brew bundle` 解析 Brewfile 时需要明确区分安装类型，而命令行 `brew install` 有自动检测能力。