---
title: "使用 post 请求触发 github action"
tags:
  - github action
  - curl
date: 2025-12-15
---

一个 curl 请求的例子：

```bash
curl -X POST 'https://api.github.com/repos/zhaochunqi/til-pages/dispatches' \
  --header 'Content-Type: application/json' \
  --header 'Accept: application/vnd.github.v3+json' \
  --header 'Authorization: Bearer github_pat_xxxxx' \
  --header 'X-GitHub-Api-Version: 2022-11-28' \
  --data '{"event_type": "til-updated"}'
```


其中 `github_pat_xxxxx` 是 github 的 token，可以在 [github token](https://github.com/settings/tokens) 页面生成。使用 fine-grained token, token 权限需要有 `Contents: Read and write`.

`til-updated` 是 github action 的事件类型，可以在 github action 的配置文件中定义。

```yaml
on:
  repository_dispatch:
    types: [til-updated]
```

这样就可以通过 curl 请求触发 github action 了。