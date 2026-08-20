---
title: "从运行中的 Pod 复制 ConfigMap 配置文件"
display: true
tags:
  - configmap
  - kubectl
  - kubernetes
  - linux
date: 2026-08-20
---

当 Kubernetes 将 `ConfigMap` 挂载为 volume 时，pod 内的文件其实是 symlink，直接 `kubectl cp` 会跳过所有文件导致拷不出内容。用 `kubectl exec` + `tar` 管道即可复制真实文件。

## 问题

```bash
# 这样拷贝会失败：目录内全是 symlink，无 .conf 文件落地
kubectl cp platform/${POD}:/app/config/ /home/laborant/config/

warning: skipping symlink: "/home/laborant/config/server.conf" -> "..data/server.conf"
# ...
# kubectl cp 退出码为 0 却什么都没拷出来
```

原因：`kubectl cp` 内部用 `tar` 流式传输，但没传 `--dereference`。挂载路径下的条目全是 symlink，tar 视其为符号链接而跳过。**`kubectl cp` 即使失败也返回 0**，必须 `ls` 验证结果。

## 解决方案

在 pod 内部 `tar` 打包（内核 VFS 透明解析 symlink），再管道给本地 `tar` 解包：

```bash
# 左侧在 pod 内打包并写 stdout，右侧本地解包并剥离前两级路径
kubectl exec -n platform "$POD" -- tar cf - /app/config \
  | tar xf - --strip-components=2 -C /home/laborant/config
```

- `--strip-components=2`：去掉 `app/config` 两级前缀，只留裸文件名
- `tar xf -`：从 stdin 读取归档，`-C` 指定解包目录

```bash
ls /home/laborant/config/
# database.conf  feature-flags.conf  logging.conf  server.conf
```

## 通用注意点与变体

- **exec 不要加 `-t`（TTY）**：TTY 会对输出做换行转换，污染二进制归档流；无 TTY 的 exec 才是干净的 stdin/stdout 回传
- **`-C` 目标目录必须先存在**：`tar` 不会自动创建目录，会报 `Cannot open` 之类错误，先 `mkdir -p /home/laborant/config`
- **等价写法**：左侧 `tar cf - -C /app config` 时归档成员只有 `config/...` 一级前缀，右侧只需 `--strip-components=1`；与"绝对路径 + strip 2"语义等价，任选一种保持一致
- **压缩变体**：网络较慢时左侧 `tar czf -`（gzip 压缩），右侧 `tar xzf -` 解压
- **依赖**：Pod 内需装有 `tar`（busybox/distroless 镜像可能没有，报 `exec: tar: not found`）；本地的 `--strip-components` 由 GNU tar / bsdtar 提供，macOS / Linux 均有
- **权限**：非 root 解包时文件 owner 会变成当前用户（tar 仅在 root 下默认保留 owner），通常无碍

## 获取运行中的 pod 名

```bash
POD=$(kubectl get pod -n platform \
  -l app=config-service \
  -o jsonpath='{.items[0].metadata.name}')
```

## 为什么 ConfigMap 是 symlink 结构

<details>
<summary>原子更新机制：两层级联导致 kubectl cp 失效</summary>

ConfigMap 以 volume 挂载时，目录结构是两层间接：

```
/app/config/
├── ..2026_08_19_10_19_29.2041564214/   ← 真实目录，存真实字节
├── ..data -> ..2026_08_19_10_19_29.2041564214   ← 指向真实目录
└── server.conf -> ..data/server.conf    ← 每个文件都是 symlink
```

- 权限串首字符 `l` 表示 symlink（`lrwxrwxrwx`）
- kubelet 更新 ConfigMap 时写入新时间戳目录，再通过一次原子 `rename()` 重指 `..data`，保证运行中的 pod 立即看到新内容且不出现新旧混合
- `tar` 默认不跟随 symlink，`kubectl cp` 因此全部跳过

</details>

