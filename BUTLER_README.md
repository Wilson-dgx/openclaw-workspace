# 🤖 管家智能体

使用 LM Studio 本地部署的 MiniMax M2.5 模型

## 配置信息

| 项目 | 值 |
|------|-----|
| **名称** | 管家 (butler) |
| **模型** | minimax/minimax-m2.5 |
| **API** | LM Studio OpenAI 兼容接口 |
| **地址** | http://127.0.0.1:1234/v1 |
| **类型** | 本地部署 |

## 使用方法

### 1. 启动 LM Studio
- 打开 LM Studio 应用
- 加载 minimax-m2.5 模型
- 开启本地服务器（端口 1234）

### 2. 启动管家智能体

```bash
# 方式1：使用启动脚本
~/.openclaw/workspace/start_butler.sh

# 方式2：直接启动
openclaw session --agent butler --model lmstudio:minimax-m2.5
```

### 3. 在对话中使用

也可以直接在对话中切换到管家：

```
@butler 你好
```

或使用命令：

```bash
openclaw session --switch butler
```

## 文件位置

- 配置目录：`~/.openclaw/agents/butler/`
- 模型配置：`~/.openclaw/agents/butler/agent/models.json`
- 启动脚本：`~/.openclaw/workspace/start_butler.sh`

## 注意事项

1. 必须先启动 LM Studio 才能使用管家智能体
2. 确保 LM Studio 的本地服务器端口为 1234
3. 如果端口冲突，需要修改 `models.json` 中的 `baseUrl`

## 故障排查

如果连接失败：
```bash
# 检查 LM Studio 是否运行
curl http://127.0.0.1:1234/v1/models

# 检查端口是否被占用
lsof -i :1234
```