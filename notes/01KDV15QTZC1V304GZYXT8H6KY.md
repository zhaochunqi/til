---
title: "终端的输出自带换行"
tags:
  - linux
  - posix
  - terminal
date: 2026-01-01
---

根据 POSIX 标准：文本行必须以换行符结尾。这意味着 rbw get xxx 的时候，实际上屏幕输出的是带有空格的。但是为什么 export a = $(rbw get xxx) 不会存在问题呢？因为 `${}` (命令替换|Command Substitution) 会去掉尾部的换行。

参考链接：
1. https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap03.html?spm=a2ty_o01.29997173.0.0.5e825171OEmeaL#tag_03_206
2. https://www.gnu.org/software/bash/manual/html_node/Command-Substitution.html#Command-Substitution-1