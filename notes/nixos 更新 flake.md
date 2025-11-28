---
tags:
  - nixos
date: 2025-11-28
---
# nixos 更新 flake

> flakes 的设计初衷是“重现性”（Reproducibility），而不是“实时性”。

## 获取最新的分支构建信息

```bash
# 只更新 nixpkgs 这个 input
nix flake update nixpkgs

# 或者更新所有 inputs
nix flake update
```
