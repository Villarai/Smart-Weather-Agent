# 智能天气助手

这是一个基于文心一言API和WeatherAPI的智能天气助手，可以回答用户关于天气的各种问题，并提供相应的建议。

## 功能特点

- 支持多个中国主要城市的天气查询
- 可以查询今天、明天和后天的天气
- 智能分析用户意图，提供个性化的天气建议
- 支持自然语言交互

## 安装说明

1. 克隆仓库：
```bash
git clone https://github.com/Villarai/Smart-Weather-Agent.git
cd weather_agent
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 配置环境变量：
   - 复制 `.env.example` 文件为 `.env`
   - 在 `.env` 文件中填入你的API密钥：
     - WeatherAPI密钥：从 [WeatherAPI](https://www.weatherapi.com/) 获取
     - 文心一言API配置：从 [文心一言开放平台](https://cloud.baidu.com/product/wenxinworkshop) 获取

## 使用方法

运行程序：
```bash
python weather_agent.py
```

示例查询：
- "明天上海适合约会吗？"
- "北京今天天气怎么样？"
- "广州后天会下雨吗？"

## 支持的城市

目前支持以下城市：
- 上海
- 北京
- 广州
- 深圳
- 杭州
- 南京
- 成都
- 武汉
- 西安
- 重庆
- 天津
- 苏州
- 厦门
- 青岛
- 大连

## 注意事项

- 请确保在使用前正确配置所有必要的API密钥
- 建议使用虚拟环境运行程序
- 如遇到API调用限制，请检查API密钥的有效性和使用配额

## 许可证

MIT License

## 贡献指南

欢迎提交Issue和Pull Request来帮助改进这个项目。

## 联系方式

如有问题或建议，请通过Issue与我们联系。 
