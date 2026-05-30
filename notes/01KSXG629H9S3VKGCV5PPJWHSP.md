---
title: "GitHub token 格式不要写死长度"
display: true
tags:
  - github
  - github-action
  - security
date: 2026-05-31
---

GitHub token 校验不要依赖固定长度，尤其不要写类似 `ghs_[A-Za-z0-9]{36}` 的正则。

GitHub 官方文档列出的 token 前缀包括：

- `ghp_`: classic personal access token
- `github_pat_`: fine-grained personal access token
- `gho_`: OAuth access token
- `ghu_`: GitHub App user access token
- `ghs_`: GitHub App installation access token
- `ghr_`: GitHub App refresh token

2026-04-27 起，GitHub App installation token 会逐步切到 stateless 格式，`ghs_` token 会变成类似 `ghs_APPID_JWT` 的结构，长度约 520 字符且会变化。JWT 部分也不应该由客户端解析或校验语义。

如果业务只是想拦住明显错误的输入，可以只做轻量格式检查：

```ts
const githubTokenRe = /^(?:(?:ghp|gho|ghu|ghs|ghr)_|github_pat_)[A-Za-z0-9_.-]+$/;
```

这个校验只确认是 GitHub 已知 token 前缀，并允许 JWT 常见的 `.` 和 `-`。真正有效性仍然应该交给 GitHub API 返回 `401 Bad credentials` 之类的结果判断。

更稳的原则：

- token 当作 opaque string，不解析内部内容
- 不限制固定长度
- 存储字段至少能放下 520 字符以上
- Actions 里优先使用内置 `GITHUB_TOKEN`，跨 repo 或特殊权限才使用 PAT 或 GitHub App

参考：

1. [GitHub Docs: GitHub's token formats](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/about-authentication-to-github#githubs-token-formats)
2. [GitHub Changelog: Notice about upcoming new format for GitHub App installation tokens](https://github.blog/changelog/2026-04-24-notice-about-upcoming-new-format-for-github-app-installation-tokens/)
