# WeChat AI Assistant

一个用于学习 Python 桌面开发的微信聊天情绪分析小项目（V1.0.0）。

使用 **PySide6** 构建界面，结合 **mss / OpenCV** 截取聊天区域、**PaddleOCR** 识别文字，并通过 **DeepSeek API** 生成情绪分析和回复建议。

> 本项目为个人学习作品，与微信官方无关。AI 无法凭少量聊天文字确定他人的真实情绪，分析结果仅供参考。

## 已实现功能

- 点击「截取聊天」后倒计时 5 秒，再手动框选聊天截图区域
- 从截图中识别中文聊天内容，初步区分「我」与「对方」
- 过滤部分居中时间戳，尝试合并同一发送方的连续文字行
- 调用 DeepSeek API 分析聊天情绪并生成三条回复建议
- 在 PySide6 窗口中展示聊天文本与 AI 分析结果
- 使用 QThread 分别运行 OCR 和网络请求，减少界面等待期间的阻塞

## 项目文件

```text
WeChat-AI-Assistant/
├── gui.py             # 运行入口，GUI、OCR/AI 工作线程
├── main.ui            # Qt Designer 界面
├── screenshot.py      # 屏幕截图与手动区域选择
├── ocr.py             # PaddleOCR 识别与文字整理
├── ai.py              # DeepSeek API 调用
├── requirements.txt   # Python 依赖
├── README.md          # 本说明
└── .gitignore         # 排除本地配置与私人数据
```

## 环境与安装

开发和测试环境为 Windows + Python 3.11，建议使用虚拟环境。进入项目目录，在 PowerShell 中执行：

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

首次运行 PaddleOCR 时可能会下载模型文件，耗时取决于网络环境和电脑性能。安装 PaddlePaddle 时如果遇到平台兼容问题，请参考 PaddlePaddle 官方针对相应系统和 Python 版本的安装说明。

## 配置 DeepSeek API Key

**不要将 API Key 写在源代码里，更不要提交到 GitHub。**

在 PyCharm 的 `gui.py` 运行配置中，添加环境变量 `DEEPSEEK_API_KEY`；也可以在启动程序的 PowerShell 会话中临时设置：

```powershell
$env:DEEPSEEK_API_KEY = "在这里填写你自己的API_Key"
.\.venv\Scripts\python.exe gui.py
```

上述 PowerShell 环境变量只对当前会话及其子进程有效。

## 使用方法

1. 运行 `gui.py`。
2. 点击「截取聊天」，在倒计时内切换到微信聊天窗口。
3. 倒计时结束后，使用鼠标框选聊天区域并确认。
4. 点击「AI分析」，等待文字识别和 AI 回复建议。

## 已知限制与后续计划

- 发送方判断依赖聊天文字在截图中的左右位置，不能保证在所有聊天主题、分辨率和气泡布局下都准确
- 文字合并与时间过滤采用启发式规则，可能误识别或漏识别
- 连续重复点击可能引起工作线程生命周期或结果覆盖问题，计划在 V1.1 解决
- 当前截图框选使用 OpenCV 的 `selectROI`，框选期间 Qt 界面可能暂时不能响应
- 计划进一步优化 OCR 模型复用、界面交互及异常处理

## 隐私提醒

- **请确保有权处理聊天内容，并尊重聊天参与者的隐私。**
- OCR 提取的聊天文字会发送至第三方 DeepSeek API 进行分析，请避免输入敏感或未经允许分享的内容。
- `.gitignore` 排除了示例聊天记录、截图和常见密钥配置，但首次提交前仍应运行 `git status` 并人工确认没有敏感文件。

## 版本

`v1.0.0` — 首个可运行版本，完成截图、OCR、AI 分析与桌面 GUI 的基本工作流。
