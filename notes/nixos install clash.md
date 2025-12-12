---
tags:
  - nixos
  - clash
  - gfw
date: 2025-11-28
id: 01KB44BDBRQ2HWAWC42Y8XRD76
---
# nixos install clash

```
  # Setup Clash
  programs.clash-verge = {
    enable = true;
    serviceMode = true;
    tunMode = true;
  };
```

开启了 tunMode 和 serviceMode