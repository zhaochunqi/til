---
tags: 
    - docker
    - docker compose
date: 2025-10-04
---
线上有个小服务，经常使用内存超标，想限制一下。我本来以为 docker compose 这些配置相关的都是跟 swarm 相关的，没想到其实是可以使用的。

在 docker compose 中添加 deploy 相关限制即可：

```yaml
deploy:
    resources:
    limits:
        memory: 300M
```

参考链接：https://docs.docker.com/reference/compose-file/deploy/#resources