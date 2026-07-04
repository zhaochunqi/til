---
title: Safari 提示可下载 App 的机制
display: true
tags:
  - ios
  - safari
  - universal-links
  - web
date: 2026-07-05
---

在 iOS Safari 中，顶部“下载/打开 App”大概率来自 **Smart App Banner**，而“点链接直接跳转 App”通常是 **Universal Links**。

```html
<meta name="apple-itunes-app" content="app-id=544007664">
```

YouTube 能显示“下载 YouTube”是因为网页声明了与 App Store App 绑定的 `apple-itunes-app`。

如果带上 `app-argument`，用户点击“打开”可跳转到指定内容页：

```html
<meta
  name="apple-itunes-app"
  content="app-id=544007664, app-argument=https://www.youtube.com/watch?v=dQw4w9WgXcQ"
>
```

如果 App 未上架 App Store，这一步无法生效，因为 `app-id` 无法对应有效应用。

## Universal Links（网页链接直接唤起 App）

你要额外配置苹果的关联域：网站提供 `apple-app-site-association`，App 开启 `Associated Domains`。

```text
https://www.youtube.com/.well-known/apple-app-site-association
```

```json
{
  "applinks": {
    "details": [
      {
        "appIDs": ["TEAMID.com.google.ios.youtube"],
        "components": [
          {
            "/": "/*"
          }
        ]
      }
    ]
  }
}
```

### 快速判断

- Safari 顶部提示“下载/打开 App” → **Smart App Banner**
- 点击 YouTube 链接直接切到 App → **Universal Links**
- 想让“打开”跳具体内容页：`app-argument` + App 内处理深链
