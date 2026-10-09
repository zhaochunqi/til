---
title: "ULID 没有用完整的 26 个字母"
display: true
tags:
  - regex
  - ulid
date: 2026-10-09
---

ULID 用的是 Crockford Base32 的 32 字符表：10 个数字加 22 个字母，`I`、`L`、`O`、`U` 不在里面。所以校验它不能写 `[0-9A-Z]{26}`：

```regex
[0-9A-HJKMNP-TV-Z]{26}      # 宽松形态
[0-7][0-9A-HJKMNP-TV-Z]{25} # 严格形态，首字符只用 3 bit
```

```python
import re
ULID = re.compile(r"^[0-7][0-9A-HJKMNP-TV-Z]{25}$")
```

那个看着像乱码的字符类展开正好 32 个字符：

```
0123456789ABCDEFGHJKMNPQRSTVWXYZ
```

`I`/`L`/`O` 排除是为了不和 `1`/`0` 混淆，`U` 是 Crockford 为避免拼出脏话额外排除的。注意 `P-T` 是**范围**不是单个字符——`[0-9A-HJKMNP-TV-Z]` 读作 `0-9`、`A-H`、字面量 `J K M N`、范围 `P-T`（P、Q、R、S、T）、范围 `V-Z`，跳过 `U`。

严格形态首字符限 `0-7`：ULID 是 48 位毫秒时间戳加 80 位随机数，编成 26 个字符后时间戳占前 10 个（50 bit 里只用 48 bit），所以第一个字符只承载 3 bit。
