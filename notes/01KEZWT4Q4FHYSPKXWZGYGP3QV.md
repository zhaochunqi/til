---
title: "使用 homebrew-tap 发布自己的项目"
display: true
tags:
  - git
  - git-open
  - homebrew
date: 2026-01-15
---

通过 homebrew-tap，可以让自己的项目通过 `brew install` 直接安装。

### 安装

```bash
brew install zhaochunqi/tap/git-open
```

### 创建自己的 tap

1. 创建 tap 仓库，命名为 `homebrew-<tap-name>`，例如 `homebrew-tap`
2. 在仓库根目录创建 `Formula/<formula-name>.rb` 文件

```ruby
class GitOpen < Formula
  desc "Open your git repo in browser using one command"
  homepage "https://github.com/zhaochunqi/git-open"
  version "2.2.1"

  on_macos do
    on_arm do
      url "https://github.com/zhaochunqi/git-open/releases/download/v2.2.1/git-open_Darwin_arm64.tar.gz"
      sha256 "9b653ba97f5095e8764f43eeb9ab0e46d01f4bbd14eadd51760b636512812a8c"
    end
    on_intel do
      url "https://github.com/zhaochunqi/git-open/releases/download/v2.2.1/git-open_Darwin_x86_64.tar.gz"
      sha256 "ab24e6fe8a49b6f526a785a94a10b56a139430f795346d30f8a5a5db1387223d"
    end
  end

  on_linux do
    on_arm64 do
      url "https://github.com/zhaochunqi/git-open/releases/download/v2.2.1/git-open_Linux_arm64.tar.gz"
      sha256 "8776da29b63a21f0949cda1814e30cc2c926bb6dee4199a9f7f0684486671c70"
    end
    on_x86_64 do
      url "https://github.com/zhaochunqi/git-open/releases/download/v2.2.1/git-open_Linux_x86_64.tar.gz"
      sha256 "cf91815149c341d718ea7b26d5d671e261bb8a5701e2de2da803d9a5a6c278c4"
    end
  end

  def install
    bin.install "git-open"
  end

  test do
    system "#{bin}/git-open", "--version"
  end
end
```

### 发布流程

1. 项目打标签并发布到 GitHub Releases，上传预编译的二进制文件
2. 更新 Formula 文件中的版本号和 sha256
3. 提交到 homebrew-tap 仓库

### 相关链接

- [homebrew-tap](https://github.com/zhaochunqi/homebrew-tap)
- [git-open](https://github.com/zhaochunqi/git-open)