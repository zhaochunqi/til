---
title: nixos 更新 flake
tags:
  - nixos
  - nix
date: 2025-11-28
---

> flakes 的设计初衷是“重现性”（Reproducibility），而不是“实时性”。

## 获取最新的分支构建信息

```bash
# 只更新 nixpkgs 这个 input
nix flake update nixpkgs

# 或者更新所有 inputs
nix flake update
```

**注意，建议更新所有 inputs，不然可能会出现 nixpkgs 和 home-manager 版本不一致的问题**
