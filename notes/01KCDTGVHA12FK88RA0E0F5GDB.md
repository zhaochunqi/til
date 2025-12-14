---
title: "direnv 中使用其他 .envrc 文件"
tags:
  - direnv
date: 2025-12-14
---

使用命令 `source_env` 可以在当前目录的 .envrc 文件中引用其他目录的 .envrc 文件。

使用具体情况可参考：

<details>
目录如下：

```bash
➜ tree -al A
drwxr-xr-x@  - zhaochunqi 14 Dec 15:02 A
.rw-r--r--@ 56 zhaochunqi 14 Dec 15:02 ├── .envrc
drwxr-xr-x@  - zhaochunqi 14 Dec 15:02 └── B
.rw-r--r--@ 57 zhaochunqi 14 Dec 15:02     └── .envrc
```

A/.envrc 文件内容如下：

```bash
export A="this is A"
export B="this is B from A folder"
```

A/B/.enrc 文件内容如下：

```bash
source_env ../.envrc
export B="This is B from B folder"
```

在 A 目录下执行 `direnv allow` 后，进入 B 目录，执行 `direnv allow` 后，可以看到如下输出：

```bash
Desktop/A/B 
➜ echo $A
this is A

Desktop/A/B 
➜ echo $B
This is B from B folder
```

可以看到，在 B 目录下，可以访问到 A 目录下的环境变量，并且 B 目录下的环境变量覆盖了 A 目录下的环境变量。这正是我们想要的。
</details>