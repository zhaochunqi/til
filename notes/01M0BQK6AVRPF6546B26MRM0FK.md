---
title: "kubectl create ingress 的 tls host 与 rule host 绑定"
display: true
tags:
  - ingress
  - kubectl
  - kubernetes
date: 2026-08-19
---

`kubectl create ingress` 的 `--rule` 语法里，`tls` 是挂在某条 rule 上的，它的 host 会直接复用该 rule 的 `host`，命令行层面**没有单独指定 tls hosts 的选项**。

```bash
kubectl create ingress snake-ingress -o snake \
  --rule="a.com/=snake:80,tls=snake" \
  --dry-run=client -o yaml
```

生成结果一定是：

```yaml
spec:
  rules:
  - host: a.com
    http:
      paths:
      - path: /
        pathType: Exact
        backend:
          service:
            name: snake
            port:
              number: 80
  tls:
  - hosts:
    - a.com
    secretName: snake
```

`rules[].host` 和 `tls[].hosts` 必然一致，无法让两者不同。

## 可行的两种办法

1. **手动改生成的 YAML（最直接）**：用 `--dry-run=client -o yaml` 生成后直接编辑 `spec.tls[0].hosts`，改成你想要的域名（如通配符证书 `*.a.com` 或额外域名），与 `rules[].host` 脱钩即可。

2. **用多条 `--rule` 聚合多个 host**：
   ```bash
   kubectl create ingress snake-ingress -o snake \
     --rule="a.com/=snake:80,tls=snake" \
     --rule="b.com/=snake:80,tls=snake" \
     --dry-run=client -o yaml
   ```
   这样 `tls[0].hosts` 会变成 `[a.com, b.com]`，但本质上只是各 rule host 的并集——**并不能**做到"某条 rule 的 host 不出现在 tls.hosts 里"这种脱钩效果。

如果你的目标是"http 规则匹配 `a.com`，但证书 SAN 是别的域名（如通配符证书）"，最干净的做法就是方案 1：生成模板后手工改 `tls.hosts` 再 `apply`。

