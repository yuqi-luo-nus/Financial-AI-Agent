# 📊 Autonomous Financial Analyst Agent (AFAA) 
### 基于 RAG 架构的自主金融财报调研体



## 🌟 项目简介 (Project Overview)
本项目是一款专为金融从业者设计的智能调研工具。它不仅仅是一个聊天机器人，而是一个能够闭环执行任务的 **AI Agent**。
它解决了传统大模型（LLM）的两大痛点：**信息滞后**（无法获取最新财报）和**幻觉问题**（回答不准确）。

通过集成 **DeepSeek-V3** 与 **Tavily AI**，该 Agent 能够实时从互联网检索官方权威 PDF 财报，并基于文档内容进行高精度的财务分析与问答。

## 🚀 核心功能 (Core Features)
* **权威数据定位**：自动过滤干扰信息，精准锁定公司官网或监管机构发布的 `.pdf` 原始财报。
* **RAG 智能问答**：采用 **RAG (Retrieval-Augmented Generation)** 技术，将解析出的 PDF 文本作为 AI 的实时知识库，确保回答每一个数字都有据可查。
* **关键指标自动提取**：一键扫描文档，自动生成包含营收、净利润、毛利率及 EPS 的财务摘要表格。
* **交互式对话**：支持针对财报细节（如：业务风险、研发投入、未来展望）进行追问。
* **本地化支持**：支持将分析报告一键导出为 Markdown 文件。

## 🛠️ 技术栈 (Tech Stack)
* **核心大脑**: [DeepSeek-V3](https://www.deepseek.com/) (通过 OpenAI SDK 兼容接入)
* **实时检索**: [Tavily AI](https://tavily.com/) (专业的 AI 搜索增强引擎)
* **Web 框架**: Streamlit (用于构建交互式金融看板)
* **解析引擎**: PyPDF2 (用于非结构化 PDF 数据的流式处理)
* **环境管理**: Python 3.10+ / Dotenv (环境变量解耦)


pip install -r requirements.txt
