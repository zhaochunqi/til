---
title: "zsh 绑定键位"
display: true
tags:
  - emacs
  - vim
  - zsh
date: 2026-01-14
---

### 查看绑定键位

查看 `ctrl + r`绑定的键位：:

```bash
❯ bindkey '^r'
"^R" history-incremental-search-backward
```

### 绑定新的键位

比如绑定 `fzf-ghq-widget`方法：

```bash
zle -N fzf-ghq-widget

# 1. 绑定默认 (Emacs) 模式
bindkey '^g' fzf-ghq-widget

# 2. 绑定 Vi 插入模式 (防止使用 Vi 模式时失效)
bindkey -M viins '^g' fzf-ghq-widget
```

解析：

1. zle (Zsh Line Editor): 这是 Zsh 的核心模块，专门负责处理你在终端里打字、移动光标、删除文字这些交互操作。
2. -N (New): 告诉 Zsh：“我要创建一个新的 Widget”。
3. fzf-ghq-widget: 这是你要注册的名字。通常我们会让 Widget 的名字 和 函数的某些名字 保持一致，这样省事。
