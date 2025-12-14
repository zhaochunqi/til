---
title: "github action 中开启 pr 权限"
tags:
  - github action
  - github
  - pr
date: 2025-12-14
---

使用 https://github.com/marketplace/actions/create-pull-request 的时候遇到无法创建 pr 的问题，需要做如下配置：

1. 检查仓库设置

请访问：如：`https://github.com/zhaochunqi/dns/settings/actions`  (替换成你自己的)
找到 "Workflow permissions" 部分，确保：
- ✅ 选择 "Read and write permissions" 
- ✅ 勾选 "Allow GitHub Actions to create and approve pull requests"

2. workflow 中添加

```yml
permissions:
  contents: write
  pull-requests: write
```