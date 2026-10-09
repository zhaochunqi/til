---
title: "WSL 下使用 Windows 的 Clash 做代理"
display: true
tags:
  - clash
  - networking
  - proxy
  - windows
  - wsl
  - zsh
date: 2026-10-09
---

WSL2 默认是 NAT 模式，`127.0.0.1` 在 WSL 里指 WSL 自己，所以 Windows 上 Clash 监听的端口在 WSL 里连不到——代理地址要写 **Windows 宿主 IP**（default route 的 gateway）：

```bash
HOST_IP=$(ip route show default | awk '{print $3; exit}')
export http_proxy=http://$HOST_IP:7897 https_proxy=http://$HOST_IP:7897 all_proxy=socks5://$HOST_IP:7897
export no_proxy=localhost,127.0.0.1,::1,.local,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16
```

Clash 侧两个前置：**局域网连接**要开（否则只监听 127.0.0.1，WSL 连不到）、端口用 **mixed 端口**（同一个口同时吃 HTTP 和 SOCKS5，所以 `all_proxy` 可以指它）。

换端口或换客户端时先探端点：

```bash
timeout 1 bash -c "exec 3<>/dev/tcp/$HOST_IP/7897" && echo ok
```

别用 zsh 内建的 `ztcp` 做这个判断，它对已关闭的端口同样返回 0。

## 开了 DNS 覆写就别关 TUN

DNS 覆写开着时，WSL 的 DNS 查询也走 Windows 宿主，域名被解析成 fake-ip（`198.18.0.0/16`），这些地址只有 Windows 侧的 TUN 能路由回去。所以 TUN 是 WSL 网络的地基：关掉它，WSL 里所有不走 proxy 环境变量的直连都会因为 `198.18.x.x` 不可路由而挂。

同理 `198.18.0.0/16` 不要加进 `no_proxy`——它是 fake-ip 不是真实地址，加了只会让分流失效。
