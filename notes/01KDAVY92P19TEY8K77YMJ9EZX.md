---
title: "杀掉 8000 端口的应用"
tags:
  - cli
  - pkill
  - port
  - terminal
date: 2025-12-25
---

kill 掉运行在 `8000` 端口的应用

```bash
lsof -ti :8000 | xargs kill -9
```
