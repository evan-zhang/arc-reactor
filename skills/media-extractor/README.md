# Media Extractor (M4 Pro 白嫖特别版)

此组件专门针对搭载 Apple Silicon 芯片（特别是拥有强劲 UMA 内存体系的 M1/M2/M3/M4 系列）的 Mac 电脑研发！

## 第一步：底层硬核安装
确保您的 macOS 已经装好了 `ffmpeg`：
```bash
brew install ffmpeg
```

## 第二步：算法挂件安装
由于使用了 Apple 官方专门优化的机器语言框架 `mlx-whisper`，请在您的 OpenClaw 运行环境中执行：
```bash
pip install -r requirements.txt
```

*(备注：由于 `mlx-whisper` 首次运行大型语言模型时会需要自动下载几个 G 大小的权重包，因此您的第一次调用可能会需要几分钟时间的网络下行。请耐心等待，在此之后所有的提取行为将都是 100% 断网且全免费运行的秒级体验！)*
