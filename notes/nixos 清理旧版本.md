---
tags:
  - nixos
date: 2025-11-28
---
# nixos 清理旧版本

```bash
# 删除所有 7 天前的旧世代（Generations）
sudo nix-collect-garbage --delete-older-than 7d
```