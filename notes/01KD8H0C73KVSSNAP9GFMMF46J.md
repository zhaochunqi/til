---
title: "修复 macos 下使用 rbw 获取密钥卡顿"
tags:
  - bitwarden
  - macos
  - pinentry
  - rbw
  - terminal
  - tty
date: 2025-12-24
---

TL,DR: 在环境中添加 `export RBW_TTY=$(tty)` 即可解决

在 macos 下使用 rbw 来获取密钥时，经常会遇到需要至少 10s 以上的情况，但是在 linux 下并没有此现象，经过一番研究发现是 macos 系统机制问题导致的：rbw 在系统中会调用 ttyname(), 这个机制在 linux 下和 macos 下不同，在 linux 下只需要读取 `/proc/self/fd/0` 即可，但是在 macos 下，需要遍历，这可能要调用 `/dev` 目录下数百个设备文件。rbw 提供了一个机制，可以通过设定 `RBW_TTY` 这个环境变量跳过此检测。

相关：[direnv 配合 rbw 一起使用](https://til.zhaochunqi.com/01kcgz1vnbesn6sdnk01cb4ex2)
