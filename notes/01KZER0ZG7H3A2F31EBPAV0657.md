---
title: "pi fetch 被 fake-IP 代理拦截"
display: true
tags:
  - macos
  - pi
  - proxy
date: 2026-08-08
---

pi 的 `fetch_content` / `web_search` 报 `Blocked internal address ... 198.18.0.0/15`：TUN/fake-IP 代理（Surge、Clash、Mihomo）把公网域名解析到保留段，被 SSRF 防护误拦。

在 `~/.pi/web-search.json` 加 `ssrf.allowRanges` 豁免该网段：

```json
{
  "ssrf": { "allowRanges": ["198.18.0.0/15"] }
}
```

注意路径是 `~/.pi/web-search.json`，**不是** `~/.pi/agent/`。查找顺序：`$PI_CODING_AGENT_DIR` → `$XDG_CONFIG_HOME/pi` → `~/.pi`。

该文件同时是 credential store（放 `provider`、API key），追加字段时保留现有内容。
