---
name: create-til
description: 添加新的 TIL 笔记
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: documentation
---

## 功能

`just new "标题"` 生成笔记入口（ULID 文件名 + front matter），然后按下述风格写正文。

## 风格

**一篇只装一个可复用的结论**：读者读完能直接抄走一条命令、一段配置、一个认知。装不下就另开一篇。

**开头先说清场景**：为什么需要它、要解决什么。一两句，别铺垫。

**主体是结论，不是过程**。结构随内容走，常见几种：

- 一句话能说清 → 就写一句话，附命令或配置
- 有坑或前置条件 → 先给结论，再补「为什么这样才行」
- 排查类问题 → 现象 → 原因 → 解法
- 步骤性内容 → 编号列表，或 `##` 小节分段
- 纯知识/原理 → 结论先行，再展开机制

`##` 标题可选，别为了对称硬凑；短篇直接连着写。

**不写**：排查过程、踩坑记录、主观取舍、结尾总结。客观约束要写（比如某写法会静默失败），那是事实不是取舍。唯一例外是**方法本身就是知识**时——像「用 cgroup 定位进程属于哪个容器」，排查方法可以是一篇笔记的全部内容。

**其他**：标题取单一主题，不要「以及…」并列；tags 用英文；正文中文，术语保留英文；代码真实可跑，域名/IP/凭据脱敏。

**跨笔记引用写成 `notes/<ULID>.md`**（从仓根数的路径，跟 README 索引一致）：站点构建时由 remark 插件改写成 `/<ulid>/`，所以从笔记页、tag 页到把整篇正文渲染出来的搜索页都能点。`scripts/check_note_links.py` 会拦下其他写法；代价是 GitHub 的 blob 视图解析不了它（会变成 `notes/notes/…`），属已知取舍。

## 模板

```markdown
---
title: "结论或主题"
display: true
tags:
  - tag1
  - tag2
date: YYYY-MM-DD
---

什么场景、要解决什么。

结论 / 配置 / 命令。

为什么这样才行（需要才写）。
```

## 收口

写完跑 `just maintain`（normalize front matter + 重排 README 索引）再提交。pre-commit 还会跑 autocorrect、索引生成和链接检查。
