---
title: "Surge Ponte 跨设备组网与 PROXY-HOME 自动选路"
display: true
tags:
  - macos
  - networking
  - subnet
  - surge
date: 2026-10-08
---

用 Surge Ponte 把家里 Mac（xiaoken）当作跳板，从外面访问家里内网。踩了一堆坑：iCloud 里残留的过期设备记录让 `xiaoken.sgponte` 永远超时、策略组 `select` 的手动选择会粘住不自动切、`smart` 组静默忽略 `DIRECT`。下面是完整结论。

## 一、Ponte 的两种用法

```
# 1. 直接访问目标设备上的服务
http://xiaoken.sgponte:8388/

# 2. 当跳板访问整个内网（本文主用法）
DOMAIN-SUFFIX,nas.zhaochunqi.com,DEVICE:XIAOKEN
IP-CIDR,192.168.31.0/24,DEVICE:XIAOKEN,no-resolve
```

`DEVICE:NAME` 是**动态策略**，不需要在 `[Proxy]` 里声明。`.sgponte` 域名在远端被解析为 `127.0.0.1`，所以连只监听 loopback 的服务也能访问。

## 二、排查 Ponte 连不上：看 verbose 日志里的实际目标地址

症状：`xiaoken.sgponte` 所有端口都超时，报「Ping 超时，请确认该设备的 Ponte 状态并检查防火墙」。

**关键排查命令**（比猜有用得多）：

```bash
SC=/Applications/Surge.app/Contents/Applications/surge-cli
$SC set-log-level verbose
# 复现请求，然后看它实际往哪个地址发 ping
grep -a "SGPonteManager\|SGPonteClient" ~/Library/Logs/Surge/*.log | tail -30
$SC set-log-level notify
```

暴露问题的日志长这样：

```
[SGPonteManager] _startPonteToDevice: xiaoken, configuration:
  {"lanAddresses":["192.168.31.10","192.168.31.131"],   ← 旧地址！真实是 .120
   "directAccessAddress":"114.102.37.94:6208"}          ← 旧公网 IP！现在是 60.169.113.178
[SGPonteManager] LAN mode
[SGPonteClient-18] Start with remote address: 192.168.31.10:6208
[SGUDPSocket] send() failed: No route to host, dest: 192.168.31.10:6208
```

**根因**：`~/Library/Application Support/com.nssurge.surge-mac/SGCore.plist` 的 `PonteDeviceList` 里有**两条同名记录**——一条是当前 iCloud 账号注册的，另一条是**早期跨 iCloud 分享留下的 `shared=true` 残留**。Surge 选中了残留那条，于是永远往废弃地址发包。

```
"ponteName" => "XIAOKEN"   shared => false   ← 正确，更新于今天
"ponteName" => "xiaoken"   shared => true    ← 残留，lan 地址还是 192.168.31.10
```

**修复**：在 Ponte 界面删掉那条标记为共享/外部的残留设备记录。注意 `.sgponte` 域名匹配**不区分大小写**，`XIAOKEN.sgponte` 和 `xiaoken.sgponte` 会落到同一条记录，改名没用。

**验证**（Ponte 专项测试，比 `nc` 权威）：

```bash
$SC test-ponte XIAOKEN
# ✅ 收到有效的 ping 响应，延迟 12 ms
# ✅ 局域网连接已成功建立
```

## 三、`[Ponte]` 段的两个键都要配

```ini
[Ponte]
server-proxy-name = PROXY           # 本机作服务端时，NAT 打洞用哪个代理（要支持 UDP 转发）
client-proxy-name = 🇯🇵snell-bwh-2   # 本机作客户端时，访问其他 Ponte 设备走哪个代理
```

**删掉 `client-proxy-name` 会立刻坏掉**：日志里连接会显示 `via (null)`，意味着裸 UDP 打洞。国内到境外 UDP 丢包严重时基本必挂，两边必须配成同一个能转发 UDP 的节点。

## 四、策略组：按网络自动切换

### `[SSID Setting]` 做不到

```ini
[SSID Setting]
SSID:MyHome suspend=true            # 只有 suspend / cellular-mode / cellular-fallback
```

它**不能**切换策略组选择。

### 用 Subnet Group（原 SSID Group）

```ini
[Proxy Group]
PROXY-HOME = subnet, default = PROXY-HOME-SMART, SSID:LearningCenter = DIRECT
```

- 条件按声明顺序求值，**首个匹配生效**，都不匹配则用 `default`
- **网络变化时自动重新求值** —— 这正是「在家直连、离家走代理」需要的
- 条件支持 `SSID:` / `BSSID:` / `ROUTER:` / `TYPE:WIFI|WIRED|CELLULAR` / `MCCMNC:`
- `SSID:` 匹配**大小写敏感**，值要跟 `dump summary` 里读到的完全一致

### 别用 `select`：手动选择会粘住

```ini
PROXY-HOME = select, DEVICE:XIAOKEN, DIRECT     # ❌
```

`select` 组的选择是**持久化手动覆盖**。在家选了 `DIRECT`，离家后**不会自动切回**，表现就是「在外访问不了内网」。诊断方法：

```bash
$SC environment | python3 -c "import sys,json;print(json.load(sys.stdin)['ProxyGroupSelection'])"
# {"PROXY-HOME": "DIRECT"}  ← 这个键存在 = 手动覆盖粘住了
```

换成 `subnet` 组后该键自动消失，恢复自动判断。

## 五、`smart` 组：哪个好用哪个（但有硬约束）

`fallback` 是**按声明顺序取第一个可用**，好用的排后面永远轮不到。要「按实测质量动态选」得用 `smart`：

```ini
PROXY-HOME-SMART = smart, DEVICE:XIAOKEN, 🇨🇳http-home-mac
```

- 评分 = 真实连接首字节延迟的时间加权移动平均 + 丢包惩罚（约 50ms / 1% 重传）
- 选中的策略失败会自动重试下一个候选；连接未收到数据会显著拉低评分
- 固定 5 分钟重测，**`interval` 参数无效**

**三个硬约束**（都踩过）：

| 约束 | 后果 |
| --- | --- |
| **只接受 proxy 策略** | 嵌套组和 `DIRECT` 这类内置策略被**静默忽略**（无报错！） |
| **不能作为 `subnet` 的成员** | 所以必须加一层中间组，`subnet → smart` 直连是不行的 |
| 不能作为 `url-test`/`load-balance` 的子策略 | 需要时用 `include-other-group` 复制成员 |

因为「smart 忽略 DIRECT」，所以「smart + 去掉 DIRECT」是天然自洽的。

## 六、最终结构

```ini
[Proxy Group]
# 在家直连；离家走 smart 动态选路
PROXY-HOME = subnet, default = PROXY-HOME-SMART, SSID:LearningCenter = DIRECT
# 中间层是必需的：smart 不能直接放进 subnet
PROXY-HOME-SMART = smart, DEVICE:XIAOKEN, 🇨🇳http-home-mac

[Rule]
DOMAIN,homelab.zhaochunqi.com,PROXY-HOME
IP-CIDR,192.168.31.0/24,PROXY-HOME,no-resolve
DOMAIN-SUFFIX,nas.zhaochunqi.com,PROXY-HOME
```

三层职责：`subnet` 判断在哪 → `smart` 选哪个代理 → `DEVICE:XIAOKEN` 走 Ponte。

## 七、几个容易搞错的细节

**`https` 类型的代理要用 HTTPS 测，不能用 `-x http://`**

Surge 的 `https` 代理是**用 TLS 包住的 HTTP 代理**。用 `curl -x http://host:port` 拿明文去打 TLS 端口，会得到 `Empty reply from server`，看起来像服务挂了——实际是测试方法错了。

```bash
# ❌ 错：明文打 TLS 端口
curl -x http://ddns.mac.zhaochunqi.com:8388 http://ipinfo.io/ip

# ✅ 对：用 Surge 自己的协议栈
$SC http probe http://www.gstatic.com/generate_204 "🇨🇳http-home-mac"
# Status: 204   Duration: 159.16 ms
```

**`test-policy` 会假阳性，`http probe` 才是端到端**

```bash
$SC test-policy "🇨🇳http-home-mac"      # RTT 157ms ← 只握手，端口活着就绿
$SC http probe <url> "<policy>"          # 真正发请求，才能确认能通
$SC test-policy-external-ip "<policy>"   # 查真实出口 IP
```

**`FINAL,...,dns-failed` 是合法且官方推荐的**

不是笔误。DNS 解析失败时，用 FINAL 的策略（通常是代理）接管，避免直接报 DNS 错误：

```ini
FINAL,PROXY,dns-failed
```

**`[URL Rewrite]` 对 HTTPS 需要 MITM**

```ini
[URL Rewrite]
api.example.com https://... 302    # 没开 MITM 的话，这条对 HTTPS 永远不生效
```

官方：「HTTPS 请求只有在为该 hostname 启用 MITM 后才能重写」。没有 `[MITM]` 段 = 这条规则是死的。

**IP-CIDR 的网段写法**

`192.168.31.1/24` 和 `192.168.31.0/24` 的 CIDR 前缀相同（掩码只取前 24 位），行为一致，但前者语义绕，写 `.0/24`。

## 八、surge-cli 值得记的命令

Surge.app 自带 skill（`/Applications/Surge.app/Contents/Resources/Skills/surge/`，含 696 行命令参考），软链到 `~/.agents/skills/surge` 即可让 agent 用上。**优先用 CLI 而不是改 profile 文件**：

```bash
SC=/Applications/Surge.app/Contents/Applications/surge-cli

$SC --check xiaopei.conf          # 校验配置，不 reload
$SC rule match github.com          # 这个域名会走哪条规则
$SC rule temp add "DOMAIN-SUFFIX,x.com,Proxy"   # 临时规则：立即生效、优先级最高、重启即消失
$SC dump summary                   # 被动健康快照（先跑这个）
$SC dump rule-usage                # 哪些规则从没命中过 → 找死规则
$SC test-ponte XIAOKEN             # Ponte 专项测试
$SC log memory 500                 # 比 grep 日志文件干净
$SC profile diff                   # original vs effective（modules 改了什么）
```

**调试时用临时规则，不要改 profile 文件。** 临时规则立即生效、优先级高于所有 profile 规则、Surge 停止后自动消失，无需清理。

## 一句话总结

Ponte 连不上优先看 `set-log-level verbose` 后日志里**实际发送的目标地址**——iCloud 里跨账号分享的残留设备记录会让它一直往废弃的 LAN/公网地址发包；按网络自动切换策略用 `subnet` 组而不是 `select`（手动选择会粘住），组内动态选路用 `smart`（但它静默忽略 `DIRECT` 和嵌套组，所以需要一层中间组）。
