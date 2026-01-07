---
title: "使用 Software Heritage Archive 下载已删除的代码"
tags:
  - bitbucket
  - git
  - gitea
  - github
  - gitlab
date: 2026-01-07
---

Software Heritage Archive 是一个代码档案库，可以下载已被删除的 GitHub、GitLab 等平台的代码。

```bash
# 1. 搜索已删除的代码
# 访问 https://archive.softwareheritage.org/search/
# 搜索格式：https://github.com/owner/repo

# 2. 找到 Permalinks 区域，复制 snapshot ID
# 格式：swh:1:snp:1930ecd7bcc8c8666c721c4def3944c98d650abf

# 3. 请求 Git bundle
curl -XPOST 'https://archive.softwareheritage.org/api/1/vault/git-bare/swh:1:snp:1930ecd7bcc8c8666c721c4def3944c98d650abf/'

# 4. 下载 Git bundle（返回的 fetch_url）
curl -L -o bundle.tar.gz 'https://archive.softwareheritage.org/api/1/vault/git-bare/swh:1:snp:1930ecd7bcc8c8666c721c4def3944c98d650abf/raw/'

# 5. 解压（得到本地 bare Git 仓库目录）
tar -xzvf bundle.tar.gz

# 6. 克隆为可用的 Git 仓库
# swh:1:snp:...git 是解压后的本地目录，不是远程 URL
git clone swh:1:snp:1930ecd7bcc8c8666c721c4def3944c98d650abf.git repo-name
```

参考：https://til.simonwillison.net/github/software-archive-recovery
