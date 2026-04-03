---
title: "公司如何审计 HTTPS 访问"
tags:
  - network
  - security
  - tls
  - 审计
date: 2026-04-03
---

公司网络能审计 HTTPS 访问记录，并非"破解了加密"，而是利用了 **TLS 握手阶段明文传输的 SNI（Server Name Indication）**。

## 原理

在 HTTPS（即 TLS）连接中，代理/防火墙无需解密流量，也无需建立 CONNECT 隧道，只需**旁路观察** TLS 握手的第一个 `ClientHello` 报文。

### TLS 握手流程（简化）

1. TCP 三次握手
2. 客户端发送 **ClientHello**（明文）
3. 服务器响应 ServerHello
4. 后续加密通信

### ClientHello 中的 SNI

`ClientHello` 是**未加密的明文数据**，其中包含扩展字段。SNI 格式如下：

```
Extension: server_name
Hostname: example.com
```

代理/防火墙只需解析这个明文握手包，即可获取目标域名，无需：
- 解密 TLS 流量
- 建立了 CONNECT 隧道（传统 HTTP 代理模式）

> SNI 是 TLS 扩展，用于解决单 IP 多域名场景。客户端必须在 `ClientHello` 中**明文**告诉服务器想访问的域名，否则服务器无法选择正确证书。

## 审计边界

- ✅ 能看到：目标域名（SNI）、目标 IP、连接时间、流量大小、连接时长
- ❌ 不能看到：URL 路径、查询参数、HTTP Header、页面内容、POST 数据

> HTTPS（TLS）保护的只是 HTTP 请求内容（路径、Header、Body），但不会隐藏目标域名和 IP 等元数据。

## 防御方式

- **ECH（Encrypted Client Hello）**：TLS 1.3 扩展，使用 DNS 公钥加密 SNI
- **DoH/DoT**：防止 DNS 查询泄露，但无法阻止 SNI 泄露

<details>
<summary>更彻底的审计：HTTPS 中间人解密（MITM）</summary>

企业可在终端安装根证书，代理动态生成假证书解密流量。但已不属于纯 CONNECT 透传。
</details>