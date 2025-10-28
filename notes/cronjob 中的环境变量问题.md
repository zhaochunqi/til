---
tags:
  - cronjob
  - env
  - shell
date: 2025-10-29
---
# cronjob 中的环境变量问题

当我在 `cronjob` 中设置：`LOGSEQ_FOLDER=$HOME/logseq` 时 (这个语法会被 cronjob 设置为环境变量),在后续的命令调用 `LOGSEQ_FOLDER` 这个变量的时候，并不能正确的获取到 `$HOME` 变量。但是我们可以尝试在 `SHELL` 中运行命令`export LOGSEQ_FOLDER=$HOME/logseq`,然后从环境变量中查找 `env|grep LOGSEQ_FOLDER` 得到结果是：`/home/alex/logseq`, 为什么？

因为 `cronjob` 中不会对环境变量的值 `$HOME` 二次展开，但是 shell 中，是直接展开了的！

* cronjob 中，`LOGSEQ_FOLDER=$HOME/logseq` 表示的是一个键值对，原样放入子进程的模块的环境变量中。
* shell 中，`LOGSEQ_FOLDER=$HOME/logseq` 表示的是一个表达式，会先计算，再展开，所以你 export 后的环境变量就已经是展开过后的了。
