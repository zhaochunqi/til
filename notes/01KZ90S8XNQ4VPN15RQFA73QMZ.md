---
title: "Open With for GitHub：从 GitHub 打开 DeepWiki 与本地 Logseq/VSCode"
display: true
tags:
  - chrome
  - github
  - productivity
date: 2026-08-05
---

在 GitHub 页面一键打开对应仓库的 DeepWiki 文档，以及通过 url scheme 唤起本地 Logseq、VSCode 等应用，减少手动拼 URL 的操作。

插件地址：https://chromewebstore.google.com/detail/open-with-for-github/iaicdcencbmacjlfdbgaggfmikfpicig?authuser=0&hl=en

## 原理

利用 GitHub 仓库页当前的 `owner/repo` 拼出目标地址，并用 `chrome.tabs` 或 URL scheme 打开。

## 实际配置（ghq 管理，本地路径 `~/ghq/github.com/{owner}/{repo}`）

- DeepWiki：`https://deepwiki.com/{owner}/{repo}`
- Logseq：`logseq://graph/MyLifeRecorded?page=github.com/{owner}/{repo}`
- Zed：`zed://file/Users/zhaochunqi/ghq/github.com/{owner}/{repo}`
- VSCode：`vscode://file/Users/zhaochunqi/ghq/github.com/{owner}/{repo}`

## 示例代码

在 content script 中读取仓库路径，把 `github.com/a/b` 转为 `{owner}/{repo}`：

```js
// location.href 形如 https://github.com/tauri-apps/tauri
const match = location.href.match(/github\.com\/([^/]+)\/([^/]+)/);
const owner = match[1];
const repo = match[2];

// 打开 DeepWiki
chrome.tabs.create({ url: `https://deepwiki.com/${owner}/${repo}` });

// 打开本地应用（ghq 路径，注意需要 encode 路径中的空格等字符）
location.href =
  `vscode://file/Users/zhaochunqi/ghq/github.com/${owner}/${repo}`;
```

## 注意

- 本地 url scheme 需要系统已注册对应 handler（VSCode 默认注册 `vscode://`，Zed 注册 `zed://`），否则会被浏览器忽略。

