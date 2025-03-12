from cx_Freeze import setup, Executable

# 创建可执行文件的配置
executableApp = Executable(
    script="main.py",
    target_name="WeChat Notifier",
    icon = "favicon.ico"
    # base=None  # 根据需要选择 "Win32GUI" 或 None，None 表示不隐藏窗口
)

# 构建选项
build_options = {
    "build_exe": {
        "includes": ["comtypes", "comtypes.stream", "comtypes.gen"],
        "include_files": [
            ("C:/Windows/System32/UIAutomationCore.dll", ".")
        ],
    }
}

# 设置包信息
setup(
    name="WebSocket WeChat Notifier",
    version="1.0.0",
    description="A WebSocket-based application for notifying WeChat messages",
    long_description="A simple application that uses UI Automation to fetch and notify WeChat messages without the need for login.",
    url="http://example.com/wechat-notifier",  # 替换为项目网址
    author="chen_bx",  # 替换为作者名字
    author_email="1947967840@qq.com",  # 替换为作者邮箱
    license="MIT",
    options=build_options,
    executables=[executableApp]
)