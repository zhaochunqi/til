---
title: "Bitwarden SSH Agent 指定特定密钥"
display: true
tags:
  - bitwarden
  - ssh
  - ssh-agent
date: 2026-02-04
---

Bitwarden SSH Agent 默认会暴露所有可用密钥给 SSH 客户端，可能导致 `Too many authentication failures` 错误。通过 SSH Config 指定特定密钥解决。

```bash
# ~/.ssh/config

Host vps1
  HostName domain.com
  StrictHostKeyChecking no
  User root
  Port 26456
  IdentityFile ~/.ssh/bw_keys/vps-auth.pub
  IdentitiesOnly yes

Host vps2
  HostName 1.1.1.1
  StrictHostKeyChecking no
  User root
  Port 27644
  IdentityFile ~/.ssh/bw_keys/vps-auth.pub
  IdentitiesOnly yes
```

`IdentitiesOnly yes` 强制 SSH 只使用指定的密钥，跳过 Agent 中的其他密钥。
