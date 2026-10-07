---
title: "Surge 按网络自动切换策略组，以及使用 app 自带的 agent skill"
display: true
tags:
  - agent
  - macos
  - networking
  - subnet
  - surge
date: 2026-10-08
---

## 一、按网络自动切换策略组

`[SSID Setting]` 只能 suspend/cellular-mode，**不能**切策略组。要按网络选路得用 **Subnet Group**：

```ini
[Proxy Group]
PROXY-HOME = subnet, default = PROXY-HOME-SMART, SSID:LearningCenter = DIRECT
```

条件按声明顺序求值，首个匹配生效，网络变化时自动重新求值。条件支持 `SSID:` / `BSSID:` / `ROUTER:` / `TYPE:WIFI|WIRED|CELLULAR`，其中 `SSID:` **大小写敏感**。

### 坑 1：`select` 组的手动选择会粘住

```ini
PROXY-HOME = select, DEVICE:XIAOKEN, DIRECT     # ❌ 在家选了 DIRECT，离家不会自动切回
```

诊断（`ProxyGroupSelection` 里有这个组 = 手动覆盖粘住了）：

```bash
surge-cli environment | python3 -c "import sys,json;print(json.load(sys.stdin)['ProxyGroupSelection'])"
# 坏: {"PROXY-HOME": "DIRECT"}   好: {} （换成 subnet 组后该键自动消失）
```

`url-test` / `fallback` / `smart` / `load-balance` 同样可被手动覆盖，「自动切换不灵了」先查这个。

### 坑 2：组内选路用 `smart` 而不是 `fallback`

`fallback` 按声明顺序取**第一个可用**——好用的排后面永远轮不到，坏节点一直被重试。`smart` 按真实连接质量（首字节延迟 + 丢包惩罚）动态选，失败自动重试下一个候选。固定 5 分钟重测，`interval` 无效。

**三个硬约束**：

| 约束 | 后果 |
| --- | --- |
| 只接受 proxy 策略 | 嵌套组和 `DIRECT` 被**静默忽略**（无报错） |
| 不能作为 `subnet` 的成员 | 必须加一层中间组 |
| 不能当 `url-test`/`load-balance` 的子策略 | 用 `include-other-group` 复制成员 |

### 最终结构

```ini
[Proxy Group]
PROXY-HOME = subnet, default = PROXY-HOME-SMART, SSID:LearningCenter = DIRECT
# 中间层必需：smart 不能直接放进 subnet
PROXY-HOME-SMART = smart, DEVICE:XIAOKEN, 🇨🇳http-home-mac
```

`subnet` 判断在哪 → `smart` 选哪个代理 → 具体策略落地。

## 二、很多 app 已经自带 agent skill

Surge.app 里就带了一份完整的，但**不在 agent 的 skill 搜索路径里**，所以 agent 完全不知道它存在：

```
/Applications/Surge.app/Contents/Resources/Skills/surge/
├── SKILL.md                    # 用法与命令选型
├── agents/openai.yaml          # 给 Codex/ChatGPT 的接入声明
└── references/command-reference.md   # 696 行完整命令目录
```

发现与安装：

```bash
find /Applications/<App>.app -iname "*skill*" -o -iname "SKILL.md" 2>/dev/null
ln -s /Applications/Surge.app/Contents/Resources/Skills/surge ~/.agents/skills/surge
```

软链而非拷贝：app 升级时自动跟着更新。`agents/` 里有 `openai.yaml` / `claude.yaml` 说明厂商是专门为 agent 接入准备的。

### 装了立刻有用的命令

```bash
SC=/Applications/Surge.app/Contents/Applications/surge-cli
$SC --check xiaopei.conf      # 校验配置，不 reload
$SC rule match github.com      # 这个域名会走哪条规则
$SC dump summary               # 被动健康快照（先跑这个）
$SC dump rule-usage            # 哪些规则从没命中过 → 找死规则
$SC profile diff               # original vs effective（modules 改了什么）
```

**最重要：调试用临时规则，别改 profile 文件。** 立即生效、优先级最高、Surge 停止即消失、无需清理：

```bash
surge-cli rule temp add "DOMAIN-SUFFIX,example.com,Proxy"
surge-cli rule temp flush
```

skill 开头第一句就是「Prefer surge-cli over GUI instructions or profile file edits」，我偏改了 profile 做实验，把链路搞坏了。

### 测试方法不对会得出错误结论

```bash
# ❌ 假阴性：https 类型代理是 TLS 包住的 HTTP 代理，明文打 TLS 端口当然失败
curl -x http://host:8388 http://ipinfo.io/ip          # Empty reply from server

# ✅ 用 Surge 自己的协议栈
surge-cli http probe http://www.gstatic.com/generate_204 "<policy>"   # Status: 204
```

```bash
surge-cli test-policy "<policy>"              # 只握手，端口活着就绿（假阳性）
surge-cli http probe <url> "<policy>"         # 真正发请求，才是端到端验证
surge-cli test-policy-external-ip "<policy>"  # 查真实出口 IP
```

**动手前先找有没有现成的 skill/CLI 工具，比自创测法可靠得多。**
