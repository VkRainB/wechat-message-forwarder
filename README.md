# 微信消息实时推送工具

## 项目简介
Real-time WeChat message notifier using uiautomation to fetch messages without logging in.

本项目通过UI Automation技术获取微信窗口中的最新消息，并通过WebSocket实时推送给客户端。它可以帮助开发者快速搭建微信消息监控系统，适用于消息提醒、自动化处理等场景。

## 功能特点
- **实时消息获取**：通过UI Automation技术，精准提取微信窗口中的最新消息。
- **WebSocket推送**：使用WebSocket协议，实时将消息推送给客户端，低延迟、高效率。
- **消息过滤**：仅推送当前分钟内的消息，避免过多历史消息干扰。
- **简单易用**：基于Flask和Flask-Sock框架，易于部署和扩展。

## 技术栈
- **后端框架**：Flask
- **WebSocket**：Flask-Sock
- **UI Automation**：uiautomation

## 项目结构
```
project/
│
├── app.py               # 主程序，负责启动WebSocket服务和消息推送
├── get_msg.py           # 提取消息的核心模块，使用uiautomation获取微信窗口消息
├── README.md            # 项目说明文档
```

## 安装与运行

### 环境依赖
1. Python 3.9+（推荐）
2. Flask
3. Flask-Sock
4. uiautomation

### 安装步骤
1. 克隆项目：
   ```bash
   git clone https://github.com/your-username/your-project-name.git
   cd your-project-name
   ```
2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
3. 启动服务：
   ```bash
   python main.py
   ```
   服务默认运行在`127.0.0.1:8765`。
### 打包步骤
   ```bash
  pip install cx_Freeze
  python setup.py build
   ```

### 客户端连接
客户端可以通过WebSocket连接到`ws://127.0.0.1:8765/ws`，接收实时消息。

## 使用示例

### 后端运行
启动`app.py`后，程序会自动监听微信窗口的消息，并通过WebSocket推送。

### 客户端代码示例（JavaScript）
以下是一个简单的WebSocket客户端示例，用于接收推送的消息：
```javascript
const socket = new WebSocket('ws://127.0.0.1:8765/ws');

socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    if (data.code === 200) {
        console.log('收到新消息：', data.data);
    } else {
        console.error('WebSocket错误：', data.error);
    }
};

socket.onclose = function(event) {
    console.log('WebSocket连接已关闭');
};
```

## 注意事项
1. **窗口问题**：程序能获取最小化的微信窗口。完全关闭窗口是没办法获取到信息的，获取的信息只能是看到的列表项，看不到也就没有消息
2. **多开问题**：本程序默认只处理一个微信窗口。如果使用多开，请确保主窗口的`ClassName`为`WeChatMainWndForPC`。
3. **消息过滤**：程序仅推送当前分钟内的消息，以避免过多历史消息干扰。
4. **依赖版本**：请确保`uiautomation`版本与Python版本兼容。

## 贡献指南
欢迎贡献代码或提出改进建议！请遵循以下步骤：
1. Fork本项目。
2. 创建一个新的分支：`git checkout -b feature/your-feature-name`。
3. 提交你的更改：`git commit -m "Add some feature"`。
4. 推送到你的分支：`git push origin feature/your-feature-name`。
5. 提交Pull Request。

## 联系方式
- **作者**：[vkrain]
- **邮箱**：[1947967840@qq.com]
- **GitHub**：[GitHub](https://github.com/VkRainB)

---

希望这个README文件能清晰地介绍你的项目。如果有任何需要调整的地方，请随时告诉我！