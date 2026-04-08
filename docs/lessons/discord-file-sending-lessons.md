# Discord 文件发送经验

## 问题描述

在 Discord 中通过 OpenClaw message 工具发送文件时遇到两个问题：

1. **Unknown Channel 错误**：使用 `channel=discord` + `target=USER_ID` 时
2. **附件不显示**：使用 `buffer/base64` 方式时，Discord 客户端不显示可下载的附件入口

## 根本原因

### 问题 1：Unknown Channel

**错误代码**：
```javascript
{ "error": "Unknown Channel" }
```

**原因**：Discord message 工具的 target 参数格式错误

**错误用法**：
```javascript
message({
  channel: "discord",
  target: "1453011761983655936",  // ❌ 错误
  message: "测试",
})
```

**正确用法**：
```javascript
message({
  target: "user:1453011761983655936",  // ✅ 正确
  message: "测试",
})
```

### 问题 2：附件不显示

**原因**：使用 `buffer` 参数发送 base64 编码的文件，Discord 客户端可能不会显示为可下载附件

## ✅ 解决方案

### 正确的文件发送流程

#### 步骤 1：准备文件

将文件复制到 OpenClaw 媒体目录：
```bash
# 创建目录（如果不存在）
mkdir -p ~/.openclaw/media/outbound

# 复制文件
cp /path/to/file.md ~/.openclaw/media/outbound/
```

#### 步骤 2：使用 message 工具发送

**参数格式**：
```javascript
message({
  action: "send",
  target: "user:USER_ID",  // 使用 user: 前缀
  message: "文件说明",
  media: "/Users/evan/.openclaw/media/outbound/file.md"  // 使用 media 参数
})
```

**完整示例**：
```javascript
message({
  action: "send",
  target: "user:1453011761983655936",
  message: "模型容灾系统文档 - MODEL_MANAGER.md",
  media: "/Users/evan/.openclaw/media/outbound/MODEL_MANAGER.md"
})
```

### 对比表

| 方面 | 错误做法 | 正确做法 |
|------|---------|---------|
| **target 格式** | `target: "USER_ID"` | `target: "user:USER_ID"` |
| **文件位置** | 任意位置 | `~/.openclaw/media/outbound/` |
| **文件参数** | `buffer: "base64..."` | `media: "/path/to/file"` |
| **channel 参数** | `channel: "discord"` | 不需要（使用 target 自动识别） |

## 📁 文件管理

### 推荐的文件目录结构

```
~/.openclaw/media/outbound/
├── docs/              # 文档文件
├── images/            # 图片文件
├── code/              # 代码文件
└── temp/              # 临时文件
```

### 批量发送文件脚本

```javascript
// 批量发送多个文件
const files = [
  "MODEL_MANAGER.md",
  "README-MODEL-SYSTEM.md",
  "INTEGRATION-GUIDE.md"
]

for (const file of files) {
  message({
    action: "send",
    target: "user:USER_ID",
    message: `文档 - ${file}`,
    media: `/Users/evan/.openclaw/media/outbound/${file}`
  })
}
```

## 🚨 注意事项

### 1. 目标 ID 格式

- **DM（私聊）**：`target: "user:USER_ID"`
- **频道消息**：`target: "CHANNEL_ID"` 或使用 `channel: "discord" + target`
- **群组**：确保有发送权限

### 2. 文件路径

- 必须是绝对路径
- 必须存在且可读
- 文件大小限制（Discord 通常 25MB 以内）

### 3. 文件类型

支持的文件类型：
- 文档：`.md`, `.txt`, `.pdf`, `.docx`
- 图片：`.png`, `.jpg`, `.gif`, `.webp`
- 代码：`.js`, `.py`, `.json`, `.yaml`
- 压缩包：`.zip`, `.tar.gz`

## 📊 测试结果

### 成功案例

**2026-02-20 模型容灾系统文档发送**：
- 文件数：5 个
- 总大小：约 42KB
- 所有文件：成功发送 ✅
- Discord 显示：可下载附件 ✅

### 失败案例

| 错误 | 原因 | 解决 |
|------|------|------|
| Unknown Channel | target 格式错误 | 改为 `user:USER_ID` |
| 附件不显示 | 使用 buffer 参数 | 改用 `media` 参数 |
| Local media path not under an allowed directory | 文件位置不对 | 复制到 `~/.openclaw/media/outbound/` |

## 🎯 最佳实践总结

### 发送文件前检查清单

- [ ] 文件已复制到 `~/.openclaw/media/outbound/`
- [ ] target 格式为 `user:USER_ID`（DM）或 `CHANNEL_ID`（频道）
- [ ] 使用 `media` 参数（不是 `buffer`）
- [ ] 不需要 `channel` 参数（使用 target 自动识别）
- [ ] 文件大小在 25MB 以内
- [ ] 文件类型受支持

### 常用命令模板

```bash
# 准备文件
cp /path/to/file.md ~/.openclaw/media/outbound/

# 验证文件存在
ls -lh ~/.openclaw/media/outbound/

# 批量复制
cp *.md ~/.openclaw/media/outbound/
```

```javascript
// 发送单个文件
message({
  action: "send",
  target: "user:USER_ID",
  message: "文件说明",
  media: "/Users/evan/.openclaw/media/outbound/file.md"
})

// 发送多个文件
const files = ["file1.md", "file2.md", "file3.md"]
files.forEach(file => {
  message({
    action: "send",
    target: "user:USER_ID",
    message: `文档 - ${file}`,
    media: `/Users/evan/.openclaw/media/outbound/${file}`
  })
})
```

## 📝 记录日期

- **首次发现问题**: 2026-02-20
- **找到解决方案**: 2026-02-20
- **验证成功**: 2026-02-20
- **文档创建**: 2026-02-20

## 🔗 相关资源

- OpenClaw 文档: https://docs.openclaw.ai
- Discord API 文档: https://discord.com/developers/docs/reference
- OpenClaw 源码: `/opt/homebrew/lib/node_modules/openclaw/dist/`

---

*经验文档 - 仅供内部参考*
*作者: Nova (✨)*
*最后更新: 2026-02-20*
