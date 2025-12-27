---
title: "macos 下载的 app 无法打开"
tags:
  - gatekeeper
  - macos
date: 2025-12-27
---
找到 app 的名字，比如 `jmcomic-downloader.app`. 执行如下命令：

```bash
xattr -cr /Applications/jmcomic-downloader.app
```

详细解释：
<details>
<summary>命令详解</summary>
1. 下载应用时，macOS 的 Gatekeeper 安全机制会自动给文件打上 `com.apple.quarantine` 属性，记录来源 (如 Safari, Chrome) 和时间戳。
2. 首次运行时，系统会检查该属性：
    * 如果 app 有有效开发者签名，用户可以选择"打开"一次来信任
    * 如果 app 未签名或者签名无效，系统直接拒绝运行，并提示无法打开 (有时候也不提示)
3. 使用 `xattr -cr` 移除了 quarantine 属性后，就认为该来源可信。

补充：
可仅移除 quarantine 属性：
```bash
xattr -rd com.apple.quarantine /Applications/jmcomic-downloader.app
```
</details>
