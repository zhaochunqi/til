---
title: 网页中设置自动发现 RSS
tags:
  - html
  - rss
date: 2025-10-07
---

可以使用 <link> 标签在 HTML 的 <head> 中声明 RSS, 这样大多数现代浏览器会自动发现。

示例：

```html
<!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>你的网站标题</title>

    <!-- RSS Feed 声明 -->
    <link
      rel="alternate"
      type="application/rss+xml"
      title="技术博客 RSS"
      href="/rss.xml"
    />

    <!-- 如果是 Atom Feed -->
    <link
      rel="alternate"
      type="application/atom+xml"
      title="技术博客 Atom"
      href="/atom.xml"
    />
  </head>
  <body>
    <!-- 网页内容 -->
  </body>
</html>
```
