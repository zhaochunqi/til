---
title: "tar 管道不落盘传输文件与目录"
display: true
tags:
  - kubernetes
  - posix
  - shell
  - tar
date: 2026-08-20
---

用 tar 的 `-`（stdin/stdout）配合 `|` 管道，把目录内容从一端流式送到另一端，全程不落临时文件。比逐文件拷贝更快、更稳，还保留目录结构与权限。

## 基本形态

```bash
# 左侧：tar 打包写到 stdout；右侧：从 stdin 解包到目标目录
tar cf - -C /src dir \
  | tar xf - -C /dst
```

- `c` 创建归档、`f -` 输出到 `-`（stdout）；`x` 解包、`f -` 从 `-`（stdin）读取归档
- `-C dir` 先切换目录再操作，避免把绝对/相对路径的前缀带进归档

## 跨主机/跨进程传送

管道两侧不必是同一进程，常见于 kubectl exec、ssh、curl 等场景：

```bash
# 从远端 Pod 拉目录到本地，剥离前两级路径
kubectl exec -n platform "$POD" -- tar cf - /app/config \
  | tar xf - --strip-components=2 -C /home/laborant/config

# 等价写法：左侧把 /app 设为根，归档内只剩 config/ 一级前缀，右侧只需 strip 1
kubectl exec -n platform "$POD" -- tar cf - -C /app config \
  | tar xf - --strip-components=1 -C /home/laborant/config
```

- `--strip-components=N`：去掉每个成员路径最前面的 N 个分量（本例去掉 `app/config` 两级）
- exec 不加 `-t`（TTY），避免换行转换污染二进制流
- `-C` 目标目录须先存在，否则报 `Cannot open`，先 `mkdir -p`

## 变体

- **压缩**（网络慢）：左侧 `tar czf -`，右侧 `tar xzf -`（gzip）
- **本地备份**：`tar cf - dir | tar xf -` 等价 `cp -a`，但保留更完整属性

## 注意

- 两端都需安装 `tar`（busybox/distroless 容器可能没有）
- `--strip-components` 由 GNU tar / bsdtar 提供，macOS / Linux 均有
- 非 root 解包时文件 owner 变成当前用户（root 下才默认保留）

