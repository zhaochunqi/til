---
title: "iOS 截图自定义时间和 wifi"
tags:
  - ios
  - macos
  - screenshot
date: 2025-12-28
---

```bash
xcrun simctl status_bar booted override \
    --time "9:41" \
    --dataNetwork "wifi" --wifiMode active --wifiBars 3 \
    --cellularMode active --cellularBars 4 \
    --batteryState charged --batteryLevel 100
```

![Simulator Screenshot](<../assets/Simulator Screenshot - iPhone 16 - 2025-12-29 at 02.59.55.webp>)

参考链接：https://jocmp.com/2025/08/08/demo-mode-for-ios-simulators/
