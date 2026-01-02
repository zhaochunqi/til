---
title: "删除 acme.json 中不再使用的证书"
tags:
  - cert
  - traefik
date: 2026-01-03
---

traefik 中生成的证书如果已经不再使用 (表现其实就是过期了) 的证书，经查询发现有人写了相关的脚本来处理，稍作修改直接使用 `uv` 来管理避免需要手动安装依赖。

- 参考这个使用即可：[Traefik ACME Certificate Cleanup Script](https://gist.github.com/zhaochunqi/798167c6e4c92e4dc2a3e51016ee1953)
- 原 gist 见 fork: [Traefik ACME Certificate Cleanup Script](https://gist.github.com/colinmollenhour/6db6014aa7a72406d32f1e8e782d29e6)
