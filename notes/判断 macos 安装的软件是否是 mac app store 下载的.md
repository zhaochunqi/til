---
tags:
  - macos
date: 2025-10-26
---
# 判断 macos 安装的软件是否是 mac app store 下载的

以 `Bitwarden` 为例：

## 确定软件已安装

```bash
ls -la /Applications/ | grep -i bitwarden
```

## 使用 SPCTL 查看该应用的信息

```bash
spctl -a -t exec -vvv /Applications/Bitwarden.app
```

输出如下：

```
/Applications/Bitwarden.app: accepted
source=Notarized Developer ID
origin=Developer ID Application: 8bit Solutions LLC (LTZ2PFU5D6)
```

如果 source 是 `Mac App Store`, 那就是通过 app store 下载的，反之如果 source 是 `Notarized Developer ID`, 那就是通过 DMG 下载的。

<details>
<summary>这个命令的详细解析</summary>


这个命令是 macOS 系统中用于 Gatekeeper（门禁）安全机制的 `spctl` 工具的一个用法。具体解释如下：

```bash
spctl -a -t exec -vvv /Applications/Bitwarden.app
```

### 各部分含义：

- **`spctl`**  
  是 macOS 自带的命令行工具，全称是 *System Policy Control*，用于管理系统策略，尤其是 Gatekeeper 对应用程序的验证和授权。

- **`-a`**（或 `--assess`）  
  表示“评估”（assess）指定的项目，即检查该应用是否被系统策略允许运行。

- **`-t exec`**（或 `--type execute`）  
  指定评估类型为“可执行”（executable），即检查该应用是否可以被当作可执行程序运行。这是针对应用程序（.app）的标准类型。

- **`-vvv`**  
  表示输出详细（verbose）信息，`v` 越多，输出越详细。`-vvv` 是非常详细的输出，会显示签名信息、证书链、权限来源等。

- **`/Applications/Bitwarden.app`**  
  要评估的目标应用程序路径，这里是安装在应用程序文件夹中的 Bitwarden 密码管理器。

---

### 这个命令的作用：

**检查 Bitwarden.app 是否通过了 macOS 的 Gatekeeper 验证，是否被允许运行。**

运行后，你会看到类似这样的输出（取决于实际情况）：

- 如果应用已正确签名且被信任：
  ```
  /Applications/Bitwarden.app: accepted
  source=Apple Notarized Developer ID
  origin=Developer ID Application: Bitwarden Inc. (XXXXX)
  ```

</details>