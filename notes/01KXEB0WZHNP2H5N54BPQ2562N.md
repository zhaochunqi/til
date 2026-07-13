---
title: "阿里云域名使用 Cloudflare DNS 无需备案"
display: true
tags:
  - aliyun
  - cloudflare
  - dns
  - domain
date: 2026-07-14
---

一直以为在阿里云买的域名必须完成 ICP 备案才能正常使用，所以有个域名闲置了很久。最近因为需要苹果开发者认证购买了一个域名，发现将 DNS 解析托管到 Cloudflare 即可正常使用，无需备案。

关键认知：**备案是针对"在国内使用国内服务器提供服务"的要求**。如果业务不面向国内用户、不接入境内服务器，域名本身可以自由使用，不备案也没问题。

## 操作方式

1. 在阿里云域名控制台将 DNS 服务器改为 Cloudflare 分配的 NS 地址
2. 在 Cloudflare 添加域名并配置 DNS 记录
3. Cloudflare 的代理（橙色云朵）功能也可正常使用

域名解析走 Cloudflare，源站用海外服务器，完全绕开备案流程。

