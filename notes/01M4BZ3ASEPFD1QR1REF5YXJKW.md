---
title: "容器里的托孤：PID 1 为什么要学会 wait？"
display: true
tags:
  - compose
  - docker
  - linux
  - tini
date: 2026-10-08
---

三国里，托孤是刘备把阿斗交给诸葛亮；Linux 里，托孤是内核把孤儿进程交给 PID 1。
区别在于：诸葛亮会管，很多容器里的 PID 1 不会。

## 什么是「托孤」

Linux 里每个进程都有父进程。父进程先退出，子进程就成了**孤儿进程**；内核不会让孤儿无家可归，会把它过继给当前 PID namespace 里的 PID 1。

普通系统里 PID 1 是 init / systemd，它的职责之一就是不断调用 `wait()`，回收退出的子进程。这就是「托孤」：父进程走了，孩子交给 PID 1。

## 为什么容器里会出问题

容器里 PID 1 往往不是 init，而是应用本身（`litestream`、`node`、`nginx`、`python`…）。这些应用只 `wait()` 自己 fork 出来的子进程，托孤来的**不认账**，于是每个孤儿退出后都留在进程表里——`ps` 里显示为 `<defunct>`。

容器里这类孤儿的常见来源是 **healthcheck**：每 30s 一次，跑得越久堆得越多。`docker exec`（healthcheck 走同一条路）创建的进程，其父进程在容器 PID namespace 之外、对容器不可见，因此被托孤给 namespace 里的 PID 1。

僵尸不占 CPU、也不占内存（只剩进程表里一个槽位），但会一直占用 PID 表项；攒够了，容器连新进程都创建不了，排查别的问题时也是噪音。

## 解法：给容器一个真正的 PID 1

把 tini 放到 PID 1——它只做两件事：reap 托孤来的进程、把信号转发给真正的应用。

```dockerfile
RUN apt-get update \
    && apt-get install -y --no-install-recommends tini \
    && rm -rf /var/lib/apt/lists/*

# 应用变成 tini 的子进程，托孤来的孤儿由 tini 回收
ENTRYPOINT ["/usr/bin/tini", "--", "/entrypoint.sh"]
```

Alpine 用 `apk add --no-cache tini`，路径是 `/sbin/tini`。

不改镜像时，`docker run --init`（或 compose `init: true`）等效，但镜像内建更省事——调用方不会忘。Kubernetes 没有等价的开关，做法同上：把 tini 作为镜像的 `ENTRYPOINT`，让容器里的 PID 1 真正承担「家长」的责任。应用若自己实现了 `SIGCHLD` 处理与 `wait()` 循环，也可以不用 tini——但大多数业务应用并不想管这些事。

## 数僵尸

容器里常常没装 `ps`/`procps`，直接读 `/proc`：

```sh
for p in /proc/[0-9]*; do
  [ "$(awk '{print $3}' "$p/stat" 2>/dev/null)" = Z ] && \
    awk '{print "pid="$1" ppid="$4" comm="$2}' "$p/stat"
done
```

`ppid` 就是那个没 reap 的 PID 1。

## 总结

「托孤」听起来很人文，在 Linux 里却是一次很具体的责任转移：内核把孤儿进程交给 PID 1。

PID 1 不只是一个编号，它意味着**收养孤儿、回收僵尸、转发信号**。容器里让普通应用当 PID 1，却不给它配一个 tini 这样的「诸葛亮」，结果往往就是一群没人收尸的僵尸，慢慢把容器拖死。

所以，别让 PID 1 只挂名，不干活。
