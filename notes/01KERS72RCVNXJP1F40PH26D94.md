---
title: "git 下处理换行问题"
display: true
tags:
  - git
  - linux
  - macos
  - windows
date: 2026-01-12
---

### 配置方法

在所有的 git 全局配置中，配置：

```bash
# Configure Git to ensure line endings in files you checkout are correct for macOS
git config --global core.autocrlf input
```

或者在对应的 ~/.gitconfig 中配置：

```ini
[core]
	autocrlf = input
```

但是 github 推荐在 windows 中将这个选项设置为 true，我查了下觉得在三端均采用 input 是非常合理的。

### 配置说明

| 配置值   | 含义                                                                  |
|:-----:|:-------------------------------------------------------------------:|
| true  | 双向转换：<br> • 输入（commit）时：CRLF → LF<br> • 输出（checkout）时：LF → CRLF     |
| input | 仅输入时转换：<br> • 输入（commit）时：CRLF → LF<br> • 输出（checkout）时：不做转换（保留 LF） |
| false | 完全不转换                                                               |


参考链接：https://docs.github.com/en/get-started/git-basics/configuring-git-to-handle-line-endings?platform=linux
