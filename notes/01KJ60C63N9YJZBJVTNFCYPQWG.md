---
title: "Docker Compose 自定义卷名"
display: true
tags:
  - docker
  - docker-compose
date: 2026-02-24
---

Docker Compose 默认会给卷名加上项目前缀（目录名），使用 `name` 属性可自定义卷名。

```yaml
services:
  db:
    image: postgres
    volumes:
      - my_custom_volume:/var/lib/postgresql/data

volumes:
  my_custom_volume:
    name: "production_db_volume"
```

运行 `docker compose up` 后，`docker volume ls` 会显示 `production_db_volume`，而非 `my-app_my_custom_volume`。

**适用场景：**
- 多项目共享卷
- 固定名字便于脚本编写和迁移
