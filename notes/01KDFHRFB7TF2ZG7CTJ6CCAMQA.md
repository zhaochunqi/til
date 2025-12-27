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

<details>
<summary>命令详解</summary>
1. 下载应用时，macOS 的 Gatekeeper 安全机制会自动为文件添加 `com.apple.quarantine` 扩展属性，用于记录来源（如 Safari、Chrome）和时间戳。

2. 首次运行应用时，系统会检查该属性：
   - 如果应用具有有效的开发者签名，用户可选择 **“打开”** 一次以临时信任；
   - 如果应用未签名或签名无效，系统将直接拒绝运行（有时甚至不显示错误提示）。

3. 执行 `xattr -cr` 命令移除 `com.apple.quarantine` 属性后，系统将视该应用为可信来源。

---

#### 补充：仅移除 quarantine 属性

```bash
xattr -rd com.apple.quarantine /Applications/jmcomic-downloader.app
```
</details>
