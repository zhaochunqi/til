---
title: nixos install clash
tags:
  - clash
  - gfw
  - nix
  - nixos
date: 2025-11-28
---

在 nixos 配置中添加：

```nix
# Setup Clash
programs.clash-verge = {
  enable = true;
  serviceMode = true;
  tunMode = true;
};
```

开启了 tunMode 和 serviceMode
