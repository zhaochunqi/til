---
title: "容器里应用占 PID 1 会永久堆积僵尸"
display: true
tags:
  - compose
  - docker
  - linux
  - tini
date: 2026-10-08
---

容器里 PID 1 是应用进程（如 `litestream`、`node`）时，容器内被托孤的进程无人 `wait()` 回收，会永久堆积成僵尸。来源之一是 healthcheck——每 30s 一次，跑得越久堆越多。

`docker exec`（healthcheck 走同一条路）创建的进程，其父进程在容器 PID namespace 之外，对容器不可见，于是被托孤给 namespace 里的 PID 1。Linux 要求 PID 1 用 `wait()` 回收这些孤儿，但应用只 wait 自己 fork 的子进程——托孤来的不认，于是每个孤儿退出后都留在进程表里。

解法是把 tini 放在 PID 1，它本身就是个只做 reap 和信号转发的 init：

```dockerfile
RUN apt-get update \
    && apt-get install -y --no-install-recommends tini \
    && rm -rf /var/lib/apt/lists/*

# 应用变成 tini 的子进程，托孤来的孤儿由 tini 回收
ENTRYPOINT ["/usr/bin/tini", "--", "/entrypoint.sh"]
```

Alpine 用 `apk add --no-cache tini`，路径是 `/sbin/tini`。

不改镜像时，`docker run --init`（或 compose `init: true`）等效，但镜像内建更省事——调用方不会忘。

## 数僵尸

容器里常常没装 `ps`/`procps`，直接读 `/proc`：

```sh
for p in /proc/[0-9]*; do
  [ "$(awk '{print $3}' "$p/stat" 2>/dev/null)" = Z ] && \
    awk '{print "pid="$1" ppid="$4" comm="$2}' "$p/stat"
done
```

`ppid` 就是那个没 reap 的 PID 1。

僵尸不占 CPU 和内存（只剩进程表里一个槽位），但容器 PID 上限耗尽后新进程起不来，排查别的问题时也是噪音。
