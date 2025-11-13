# 部署指南

## 已完成的步骤

✅ 代码已推送到 GitHub: https://github.com/sunyuzheng/english-editor
✅ Dockerfile 已创建并配置
✅ 应用已更新以支持 PORT 环境变量
✅ 部署脚本已创建

## 部署步骤

### 1. 设置 API Token

创建 `.env` 文件并添加你的 AI_BUILDER_TOKEN:

```bash
echo "AI_BUILDER_TOKEN=your_actual_token_here" > .env
```

或者导出环境变量:

```bash
export AI_BUILDER_TOKEN=your_actual_token_here
```

### 2. 运行部署脚本

```bash
source venv/bin/activate
python deploy.py
```

### 3. 等待部署完成

部署需要 5-10 分钟。完成后，你的应用将在以下地址可用:

**https://english-editor.ai-builders.space**

### 4. 检查部署状态

你可以通过以下方式检查部署状态:

- 访问部署 API: `https://www.ai-builders.com/resources/students-backend/v1/deployments/english-editor`
- 或使用部署脚本检查状态（可以扩展 deploy.py 添加状态检查功能）

## 部署信息

- **GitHub 仓库**: https://github.com/sunyuzheng/english-editor
- **服务名称**: english-editor
- **分支**: main
- **端口**: 8000 (由 Koyeb 通过 PORT 环境变量设置)

## 注意事项

1. `AI_BUILDER_TOKEN` 会在部署时自动注入，不需要在代码中硬编码
2. 部署使用 Docker 容器，限制为 256 MB RAM
3. 免费托管期为 12 个月
4. 如果需要删除服务或延长托管，请联系讲师

