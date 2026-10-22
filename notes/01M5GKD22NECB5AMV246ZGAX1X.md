---
title: "starship explain 查看当前提示符每段是什么"
display: true
tags:
  - cli
  - shell
  - starship
date: 2026-10-22
---

提示符里冒出个不认识的符号，或者想确认某一段是哪来的：

```bash
starship explain
```

```
 til          -  The current working directory
 on  main     -  The active branch of the repo in your current directory
 [?]          -  Symbol representing the state of the repo
 ❯            -  A character (usually an arrow) beside where the text is entered
 09:25        -  The current local time
```

默认只反映此刻。要看别的状态，把 shell 注入的变量当参数传进去：

```bash
starship explain --status 1          # 上条命令退出码 1 时的提示符
starship explain -p /path/to/repo    # 换目录，不用 cd
starship explain --cmd-duration 5000 # 耗时 5 秒那一段
```

只解释已出现的段。查某个 module 为什么没显示，用 `starship module <name>` 单独渲染（`-l` 列全部名字）；提示符渲染结果本身用 `starship prompt`。
