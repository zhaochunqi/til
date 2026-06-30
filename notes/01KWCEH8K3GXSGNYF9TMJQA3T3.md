---
title: "GHCR multi-arch 镜像为什么会出现很多 untagged"
display: true
tags:
  - docker
  - ghcr
  - github
  - github-action
  - 构建
date: 2026-06-30
---

在 GHCR 里看到很多 `untagged`，不一定代表清理任务漏删了垃圾镜像。

如果一个 Docker 镜像是 multi-arch 构建，比如同时构建：

```yaml
platforms: linux/amd64,linux/arm64
```

那么一个 tag 通常不是直接贴在某个具体平台镜像上，而是贴在一个“目录”上。这个目录的正式名字叫 OCI image index 或 manifest list。

可以把它理解成：

```text
ghcr.io/org/app:sha-xxxxxxx
  -> 一个总入口 / 目录
      -> amd64 机器用的镜像
      -> arm64 机器用的镜像
```

用户拉镜像时还是用同一个 tag：

```bash
docker pull ghcr.io/org/app:sha-xxxxxxx
```

Docker 会根据本机架构自动挑正确的子镜像。amd64 机器拿 amd64，arm64 机器拿 arm64。

## 为什么会显示成 1 tagged + 4 untagged

以一个同时构建 `linux/amd64` 和 `linux/arm64`，并且没有关掉 buildx 默认 provenance 的镜像为例，一次构建大致会产生：

```text
1 个 tagged image index
2 个 untagged platform image manifest
2 个 untagged provenance attestation manifest
```

所以 GHCR 页面上看起来就是：

```text
1 tagged + 4 untagged
```

这里的 2 个 platform manifest 是真正给不同 CPU 架构运行用的镜像。它们没有自己的 tag，因为 tag 贴在上层 image index 上。

另外 2 个 provenance attestation manifest 不是运行镜像，而是构建证明。它们记录“这个镜像是从哪个 repo、哪个 commit、哪个 Dockerfile、哪次 GitHub Actions run 构建出来的，以及用了哪些基础镜像/构建依赖”。常见格式是 in-toto statement，predicate 是 SLSA provenance。

## 这些 untagged 可以删吗

不要只看 GHCR UI 上写着 `untagged` 就手动删。

如果这些 untagged 是被某个保留 tag 引用的子 manifest，删掉以后可能会破坏 multi-arch 镜像，或者丢掉 provenance 证明。正确的清理逻辑应该理解 image index 和它下面的子 manifest，而不是把所有 UI 上的 untagged 都当成孤立垃圾。

像 `dataaxiom/ghcr-cleanup-action` 这类专门处理 GHCR 清理的工具，会把 multi-arch image、attestation、referrer 这些关系一起考虑。删除旧 tagged image 时，它会连同下面的子 manifest 一起处理；保留新 tagged image 时，被引用的 untagged 子 manifest 也应该留下。

## GitHub 能避免这种显示吗

GHCR 目前没有一个开关可以说“不要把被 image index 引用的子 manifest 显示为 untagged”。它是按 registry 里的 manifest/version 展示，所以 UI 会显得比较吵。

能减少数量，但都有代价：

- 关掉 provenance：每批少两个 attestation，代价是没有构建来源证明。
- 只构建单平台：少一个平台镜像，代价是不再同时支持 amd64/arm64。
- 单平台并关掉 provenance：最干净，但功能和供应链信息都缩水。

更实用的判断是：不要追求 GHCR 页面上完全没有 untagged，而是区分“孤立 untagged”和“被保留 tag 引用的 untagged 子 manifest”。前者可以清理，后者是镜像结构的一部分。
