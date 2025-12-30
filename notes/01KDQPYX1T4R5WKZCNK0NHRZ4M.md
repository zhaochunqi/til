---
title: "修复滚动条导致的布局偏移"
tags:
  - css
  - layout shift
  - webdev
  - 前端
  - 滚动条
date: 2025-12-30
---
开发的时候遇到右侧由于有些页面有滚动条，有些没有导致同一个布局会出现布局偏移。

添加 `scrollbar-gutter: stable;` 就可以避免此问题。

参考链接：https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/scrollbar-gutter
