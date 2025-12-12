---
tags:
  - docker
  - linux
date: 2025-10-05
id: 01K6RD0QVGKHZ8N1BR8TCQXC9M
---

> vps 内存爆炸了，上来查原因，使用 bottom 查看之后发现是 `uwsgi` 进程占用高内存，但我印象中我是我没有部署类似的服务的，因为我基本都是使用 docker 来部署的。

## 通过 cgroup 信息定位问题

Linux 通过 cgroup 来管理容器资源，每个进程都会记录自己属于哪个 cgroup。我们可以利用这一点来找到它所属的容器。

1. **找到 `uwsgi` 进程的 PID (Process ID)**

    ```bash
    pidof uwsgi
    ```

    这个命令会返回一个或多个数字，就是 `uwsgi` 的进程 ID。我们假设返回的是 `12345`。

2. **查看该 PID 的 cgroup 信息**

    ```bash
    cat /proc/12345/cgroup
    ```

    在输出中，你会看到类似下面这样的行：

    ```bash
    11:perf_event:/docker/a1b2c3d4e5f6...
    10:cpuset:/docker/a1b2c3d4e5f6...
    ...
    1:name=systemd:/docker/a1b2c3d4e5f6...
    ```

    注意 `/docker/` 后面那串以 `a1b2c3d4e5f6` 开头的字符串，**这就是容器的完整 ID**。

3. **根据容器 ID 找到容器名**

    ```bash
    # 使用上一步找到的容器 ID 的前几位即可
    docker inspect a1b2c3d4e5f6 | grep "Name"
    ```

    或者更简单地，列出所有容器，手动找到这个 ID：

    ```bash
    docker ps
    ```

    在 `CONTAINER ID` 列中找到对应的 ID，它旁边的 `NAMES` 列就是你容器的名字，例如 `my-web-app`。

> **小技巧：** 你可以组合成一条命令，一步到位：
> `cat /proc/$(pidof uwsgi)/cgroup | grep -o '[0-9a-f]\{64\}' | xargs -I {} docker inspect {} | grep "Name"`
