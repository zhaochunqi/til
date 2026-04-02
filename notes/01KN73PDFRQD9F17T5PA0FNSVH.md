---
title: "网页上保护 email 地址的方法"
display: true
tags:
  - security
  - web
date: 2026-04-02
---

根据 2026 年最新实测数据，简单有效的 email 地址防爬虫方法：

## 纯文本 email

| 方法 | 阻止率 |
|------|--------|
| 无保护 | 0% |
| HTML Entities | 95% |
| HTML 注释 | 98% |
| HTML SVG | **100%** |
| CSS display: none | **100%** |
| JS 拼接 | **100%** |
| JS 转换 (自定义函数) | **100%** |
| JS AES 加密 | **100%** |

## 可点击 mailto 链接

| 方法 | 阻止率 |
|------|--------|
| 无保护 | 0% |
| HTML Entities | 100% |
| URL 编码 | 96% |
| HTTP 重定向 | **100%** |
| HTML SVG | **100%** |
| JS 拼接 | **100%** |
| JS 转换 | **100%** |
| JS AES 加密 | **100%** |

## 推荐方案

**最简单且有效**：CSS `display: none` + 变化诱饵标签

```html
<div class="email">ad@<span>email.</span>spencermortensen.<span>example.</span>com</div>
```

```css
div.email > span:nth-child(2) { display: none; }
```

无 JS 依赖，完全无障碍可用。

**推荐方案**：JS 转换（自定义函数）

```html
<span id="email">zibby example com</span>
```

```js
const map = { zibby: 'hello', example: 'gmail', com: 'com' };
// 自定义转换逻辑
```

原理：HTML 源码只有乱码，需要在浏览器端用 JS 转换才能得到真实 email。

**最强方案**：JS AES 加密（需 HTTPS）

```html
<span class="email">Kreuz2xa6xB8Fpjaa0lFgACNLO6n_Auu1CGjcG8z_Ec</span>
```

使用浏览器内置 SubtleCrypto 进行 AES-256 加密。

## 不推荐（破坏可用性）

- 符号替换 (ag AT email DOT com) - 用户需手动还原
- 图片 - 无法复制、屏幕阅读器无法读取
- CSS content - 文本不可选中
- CSS 文字方向反转 - 复制后是反的

关键发现：大多数爬虫很简单，即使最基础的混淆技术也能阻止 95% 以上的爬虫。建议组合使用多种技术。

> 来源: [Email obfuscation: What works in 2026?](https://spencermortensen.com/articles/email-obfuscation/)