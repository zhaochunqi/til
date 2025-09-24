---
tags:
  - github
date: 2025-09-24
---
github 中有一些垃圾钓鱼信息会 `@` 你，在 官方 处理之后，你的 github 信息中的 notification 由于已经不存在了导致无法正常清理。

![通知截图](<../assets/Screenshot 2025-09-24 at 12.47.07.png>)

解决方法如上如：`gh api notifications -X PUT -F last_read_at=2025-09-24` 这样即可。

[来源](https://x.com/zhangjintao9020/status/1970690699948630455)