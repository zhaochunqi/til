---
title: "GitHub auto-merge 怎么开"
display: true
tags:
  - github
  - pr
  - renovate
date: 2026-10-21
---

想让 PR 在 CI 绿了之后自动合并，光在 repo Settings 里勾 **Allow auto-merge** 不够——那只是「允许存在这个动作」，一个 PR 都不会自动合。每个 PR 还得单独开：

```bash
gh pr merge <number> --auto --squash
# 等价于 PR 页面上的 Enable auto-merge
```

## required checks 才是「等什么」

auto-merge 只等 **required** status checks，也就是 branch protection / ruleset 里显式声明为必需的那些，不是等所有 checks 跑完。

没配 required 的时候，一个 mergeable 的 PR 开了 auto-merge 会**立刻合并**——`build` job 可能还在跑，代码已经进 main 了。按钮看着像「排队等 CI」，实际是个立即合并键。

先确认当前分支有没有 required：

```bash
gh api repos/<owner>/<repo>/branches/main/protection   # 404 表示没开 branch protection
gh api repos/<owner>/<repo>/rules/branches/main        # [] 表示没有 ruleset 生效
```

两条都空，就是 required checks 为空。想让 auto-merge 真的等 CI，就得在其中一处把 job 名（跟 workflow 的 job id 一致，比如 `build`）声明为必需。

## 别跟 Renovate 的 automerge 混

Renovate 的 `automerge: true` 是另一套：它在自己的运行周期里判断版本、冷静期、checks，然后直接调 merge API，既不点这个按钮，也不受 Settings 里那个开关影响（只有 `platformAutomerge: true` 才借用）。所以 Renovate 造的 PR 上看不到 auto-merge 标记，不代表没生效——看 `mergedBy` 是不是 `app/renovate`。

免费版私有仓库连原生 auto-merge 都不可用的情况，见 [Renovate 免费版私有仓库的 automerge 配置](notes/01KZENXYBZWCHJNWJW5X8VY7P1.md)。
