---
title: nixos install clash
tags:
  - nixos
  - clash
  - gfw
date: 2025-11-28
---

```
  # Setup Clash
  programs.clash-verge = {
    enable = true;
    serviceMode = true;
    tunMode = true;
  };
```

开启了 tunMode 和 serviceMode