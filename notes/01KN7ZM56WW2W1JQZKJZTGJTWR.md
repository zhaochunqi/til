---
title: "公司代理如何审计 HTTPS 访问"
tags:
  - network
  - proxy
  - security
  - tls
date: 2026-04-03
---

公司代理能审计 HTTPS 访问记录，并非"破解了加密"，而是利用了 **TLS 握手阶段协议设计的历史妥协（明文 SNI）**。

## 原理

客户端通过代理访问 `https://example.com/page` 时：

1. 客户端发送 `CONNECT example.com:443 HTTP/1.1`
2. 代理返回 `200 Connection Established`，TCP 隧道建立
3. **客户端发起 TLS 握手**，发送第一个明文 `ClientHello` 报文
4. 代理解析 `ClientHello` 中的 SNI（Server Name Indication）字段，记录域名
5. 后续流量仅做 TCP 转发，不解密

> SNI 是 TLS 扩展，用于解决单 IP 多域名场景。客户端必须在 `ClientHello` 中**明文**告诉服务器想访问的域名，否则服务器无法选择正确证书。

## 审计边界

- ✅ 能看到：目标域名（SNI）、连接时间、流量大小、连接时长
- ❌ 不能看到：URL 路径、查询参数、HTTP Header、页面内容、POST 数据

## 防御方式

- **ECH（Encrypted Client Hello）**：TLS 1.3 扩展，使用 DNS 公钥加密 SNI
- **DoH/DoT**：防止 DNS 查询泄露，但无法阻止 SNI 泄露

<details>
<summary>更彻底的审计：HTTPS 中间人解密（MITM）</summary>

企业可在终端安装根证书，代理动态生成假证书解密流量。但已不属于纯 CONNECT 透传。
</details>