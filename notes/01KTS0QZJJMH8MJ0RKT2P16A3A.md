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

SSL 证书过期会导致网站无法访问，用 [CertMonitor](https://certmonitor.xyz) 可以提前收到过期提醒。

## 功能

- 自动检测证书有效期，提前 30/7/1 天邮件通知
- 支持监控多域名、泛域名证书
- 检测证书链完整性、OCSP 状态
- 免费版支持 5 个域名，付费版不限量

## 快速开始

1. 注册账号：访问 [certmonitor.xyz](https://certmonitor.xyz) 
2. 添加域名：输入 `example.com` 或 `*.example.com`
3. 验证所有权：通过 DNS TXT 记录或上传验证文件
4. 配置通知：设置邮件、Slack、Webhook 等接收渠道

## 实际场景

```bash
# 批量添加监控（使用 API）
curl -X POST https://api.certmonitor.xyz/v1/monitors \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "domain": "api.example.com",
    "alert_days": [30, 7, 1]
  }'
```

## 为什么需要

- Let's Encrypt 证书 90 天到期，容易忘记续期
- 多域名、多环境（dev/staging/prod）管理复杂
- CI/CD 自动续期失败时缺少兜底通知
- 证书链配置错误导致部分客户端无法访问

相比自建脚本，专业服务的优势在于稳定性监控、多渠道告警和证书链深度检测。
