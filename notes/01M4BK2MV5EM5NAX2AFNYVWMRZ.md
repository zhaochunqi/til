---
title: "Surge 按网络自动切换策略组，以及使用 app 自带的 agent skill"
display: true
tags:
  - agent
  - macos
  - networking
  - subnet
  - surge
date: 2026-10-08
---

## 需求

在外工作时走代理回家里的内网，在家时自动切回直连。也就是策略组要跟着所在网络自动切。

## 配置

`[SSID Setting]` 做不到（它只管 suspend / cellular-mode），得用 **Subnet Group**：

```ini
[Proxy Group]
PROXY-HOME = subnet, default = PROXY-HOME-SMART, SSID:LearningCenter = DIRECT
# 中间层必需：smart 不能直接放进 subnet
PROXY-HOME-SMART = smart, DEVICE:XIAOKEN, 🇨🇳http-home-mac
```

条件按声明顺序求值，首个匹配生效，**网络变化时自动重新求值**——这就是「在家直连、出门走代理」。条件支持 `SSID:` / `BSSID:` / `ROUTER:` / `TYPE:WIFI|WIRED|CELLULAR`，其中 `SSID:` **大小写敏感**。

两个选型要点：

- 别用 `select` 组：手动选过一次就粘住，网络变了也不会切回来
- 组内用 `smart` 而不是 `fallback`：后者按声明顺序取第一个可用，好节点排后面永远轮不到

## app 自带 agent skill

Surge.app 里带了一份完整的 agent skill，只是不在 agent 的搜索路径里，软链过去即可（app 升级自动跟随）：

```bash
find /Applications/<App>.app -iname "SKILL.md" 2>/dev/null
ln -s /Applications/Surge.app/Contents/Resources/Skills/surge ~/.agents/skills/surge
```

```bash
SC=/Applications/Surge.app/Contents/Applications/surge-cli
$SC rule match github.com      # 这个域名会走哪条规则
$SC http probe <url> "<policy>"                        # 端到端验证策略
$SC rule temp add "DOMAIN-SUFFIX,example.com,Proxy"    # 调试用临时规则，别改 profile
```
