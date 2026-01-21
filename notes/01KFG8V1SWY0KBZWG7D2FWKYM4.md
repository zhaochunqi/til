---
title: "测试覆盖率报告不应提交到 Git"
display: true
tags:
  - coverage
  - git
  - testing
date: 2026-01-21
---

测试覆盖率报告是构建产物，可以在本地或 CI 环境中随时重新生成，不应提交到 Git 仓库。

## 问题

提交测试覆盖率报告会导致：
- Git 仓库体积膨胀
- 每次测试运行产生大量变更记录
- 无意义的文件差异干扰代码审查

## 解决方案

将覆盖率报告目录添加到 `.gitignore`：

```gitignore
# 测试覆盖率报告
coverage/
*.lcov
.nyc_output/
```

## 最佳实践

1. **本地生成**：在需要查看覆盖率时本地运行命令
2. **CI 集成**：在 CI/CD 流程中生成并上传到专门的服务
3. **工具推荐**：
   - Codecov
   - Coveralls
   - GitHub 自带的覆盖率显示

这样既保持了仓库整洁，又能持续监控代码覆盖率。

