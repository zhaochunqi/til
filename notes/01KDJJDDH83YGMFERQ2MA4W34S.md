---
title: "iOS 截图自定义时间和 wifi"
tags:
  - ios
  - macos
  - screenshot
date: 2025-12-28
---

```bash
xcrun simctl status_bar booted override --time "9:41" --dataNetwork "wifi" --wifiMode active --wifiBars 3 --cellularMode active --cellularBars 4 --batteryState charged --batteryLevel 100
```

参考链接：https://jocmp.com/2025/08/08/demo-mode-for-ios-simulators/
