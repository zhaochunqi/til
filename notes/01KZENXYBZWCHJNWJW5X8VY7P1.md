---
title: "Renovate 免费版私有仓库的 automerge 配置"
display: true
tags:
  - github
  - renovate
date: 2026-08-08
---

免费版私有仓库不支持 GitHub 原生 auto-merge（API 对 `allow_auto_merge=true` 返回 200 但静默不生效，和 branch protection 一样提示 "Upgrade to GitHub Pro"）。此时 Renovate 托管版 App 默认的 `platformAutomerge: true` 会失效：PR 上写着 "Automerge: Enabled" 却永远不会合并。

解法：让 Renovate 自己合并 PR，并去掉周期限制（依赖 `group:allNonMajor` 已把所有 minor/patch 合并成一个 PR，提高频率不会增加噪音）：

```json5
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": [
    "config:recommended",
    "group:allNonMajor"
  ],
  "rangeStrategy": "bump",
  "dependencyDashboard": false,
  "labels": ["dependencies", "renovate"],
  "automerge": true,
  // 免费版私有仓库用不了 GitHub 原生 auto-merge，由 Renovate 自己合并
  "platformAutomerge": false,
  "packageRules": [
    {
      matchDepTypes: ["peerDependencies"],
      enabled: false,
    },
  ],
  "ignoreDeps": ["node"],
}
```

排查要点：PR API 返回 `autoMergeRequest: null` 且 CI 全绿、无 branch protection，却仍不合并，基本就是这个原因。
