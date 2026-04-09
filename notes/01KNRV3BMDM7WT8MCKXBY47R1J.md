---
title: "Docker Compose tty 和 stdin_open 配置"
tags:
  - compose
  - docker
date: 2026-04-09
---

`docker-compose.yml` 中 `tty: true` 和 `stdin_open: true` 这两个配置项分别对应 `docker run` 的 `-t` 和 `-i` 参数。

## tty: true

分配虚拟终端（Pseudo-TTY），让程序输出像在普通命令行中运行，保留颜色和交互式输出。

## stdin_open: true

保持标准输入开启，即使没有 attach 到容器也能接收指令。

## 适用场景

Minecraft 服务器等需要交互式控制台的服务。

## 为什么 Minecraft 必须用它们

Minecraft 服务器有**交互式控制台**，可以：
- 手动输入命令：`/op yourname` 给自己管理员权限，或 `/stop` 安全关闭服务器
- 使用 `docker attach` 进入游戏控制台直接输入指令

如果没开这两个选项，`docker attach` 只能看输出，无法输入命令。

```yaml
services:
  mc:
    image: itzg/minecraft-server
    tty: true
    stdin_open: true
```

> 总结：`tty` 负责输出，`stdin_open` 负责输入。
