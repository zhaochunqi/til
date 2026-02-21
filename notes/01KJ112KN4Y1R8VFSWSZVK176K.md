---
title: "Docker Compose healthcheck 优先级"
display: true
tags:
  - docker
  - docker-compose
date: 2026-02-22
---

Docker Compose 中的 `healthcheck` 配置会覆盖 Dockerfile 中的 `HEALTHCHECK` 指令。

```yaml
# docker-compose.yml
services:
  web:
    image: myapp
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

优先级：Dockerfile < Docker Compose。

**为什么 Compose 优先？**

遵循"运行时配置优于镜像构建配置"原则。Compose 覆盖 Dockerfile 的优势：

- **灵活性**：不同环境（开发/测试/生产）可配置不同的检查频率或超时时间
- **依赖管理**：配合 `depends_on` 的 `condition: service_healthy` 控制容器启动顺序
- **集中管理**：在 Compose 文件中一目了然，无需翻阅各镜像源码
