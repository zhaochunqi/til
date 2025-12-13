---
title: "获取终端命令运行的平均时间"
tags:
  - linux
  - terminal
  - hyperfine
  - cli
date: 2025-12-12
---

使用 hyperfine 来运行，参考：https://github.com/chinanf-boy/hyperfine-zh#%E7%94%A8%E6%B3%95

比如：`hyperfine 'sleep 0.3'`, 运行结果如下

```bash
[nix-shell:~/ghq/github.com/zhaochunqi/til]$ hyperfine 'sleep 0.3'
Benchmark 1: sleep 0.3
  Time (mean ± σ):     319.5 ms ±   4.8 ms    [User: 6.8 ms, System: 3.8 ms]
  Range (min … max):   311.0 ms … 326.1 ms    10 runs
```