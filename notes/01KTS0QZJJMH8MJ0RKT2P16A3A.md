---
title: "使用 CertMonitor 监控 SSL 证书过期"
display: true
tags:
  - certificate
  - devops
  - monitoring
  - ssl
date: 2026-06-10
---

SSL 证书过期会导致网站无法访问，用 [CertMonitor](https://certmonitor.xyz) 可以监控证书有效期并邮件通知。

## 快速开始

1. 注册账号：访问 [certmonitor.xyz](https://certmonitor.xyz) 
2. 添加域名：输入要监控的域名
3. 配置通知：设置邮件接收地址

## 为什么需要

- Let's Encrypt 证书 90 天到期，容易忘记续期
- 自动续期失败时能及时发现
