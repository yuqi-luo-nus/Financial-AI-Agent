import streamlit as st
import os
import requests
import time
from io import BytesIO
from PyPDF2 import PdfReader
from openai import OpenAI
from tavily import TavilyClient
from dotenv import load_dotenv

# 加载配置
load_dotenv()

# --- 1. 核心初始化 ---
def get_keys():
    ds_key = os.getenv("DEEP_SEEK_KEY") or st.secrets.get("DEEP_SEEK_KEY")
    tv_key = os.getenv("TAVILY_API_KEY") or st.secrets.get("TAVILY_API_KEY")
    return ds_key, tv_key

DEEP_SEEK_KEY, TAVILY_KEY = get_keys()
client = OpenAI(api_key=DEEP_SEEK_KEY, base_url="https://api.deepseek.com")
tavily = TavilyClient(api_key=TAVILY_KEY)

# --- 2. 页面设置 ---
st.set_page_config(page_title="AI 权威财报助手", layout="wide")
st.title("📂 权威财报下载、解析与智能问答")

# 初始化 Session State (用于存储对话记录和 PDF 文本)
if "pdf_text" not in st.session_state: st.session_state.pdf_text = ""
if "messages" not in st.session_state: st.session_state.messages = []

# --- 3. 侧边栏：搜索与财报解析 ---
with st.sidebar:
    st.header("🔍 第一步：获取权威财报")
    company = st.text_input("公司名称", placeholder="例如: NVIDIA")
    year = st.selectbox("年份", ["2024", "2025"])
    
    if st.button("搜索并下载财报"):
        if company:
            with st.status(f"正在全网搜寻 {company} 官方 PDF...", expanded=True) as status:
                # 策略：强制搜索 PDF 文件
                query = f"{company} {year} annual report financial results official PDF"
                results = tavily.search(query=query, search_depth="advanced", max_results=5)
                
                # 寻找真实的 PDF 链接
                pdf_url = next((r['url'] for r in results['results'] if '.pdf' in r['url'].lower()), None)
                
                if pdf_url:
                    status.write(f"✅ 找到权威链接: {pdf_url}")
                    # 下载并解析 PDF
                    resp = requests.get(pdf_url)
                    pdf_file = BytesIO(resp.content)
                    reader = PdfReader(pdf_file)
                    
                    # 提取前 15 页（财报最核心的数据通常在前面）
                    full_text = ""
                    for i in range(min(15, len(reader.pages))):
                        full_text += reader.pages[i].extract_text()
                    
                    st.session_state.pdf_text = full_text
                    status.update(label="🚀 财报解析成功！可以开始对话了", state="complete")
                    st.success(f"[点击此处手动下载原始 PDF]({pdf_url})")
                else:
                    st.error("未能自动找到官方 PDF 链接，请尝试输入更准确的公司全称。")

# --- 4. 主界面：关键指标显示与 Chatbox ---
if st.session_state.pdf_text:
    # A. 关键财务指标提取 (利用 AI)
    with st.expander("📊 查看本报告核心财务指标提取", expanded=True):
        if st.button("点击提取关键数值"):
            with st.spinner("AI 正在扫描文档..."):
                extract_prompt = f"请根据以下财报文本，提取 营收(Revenue)、净利润(Net Income)、毛利率(Gross Margin) 和 EPS，并以 Markdown 表格显示：\n\n{st.session_state.pdf_text[:10000]}"
                res = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[{"role": "user", "content": extract_prompt}]
                )
                st.markdown(res.choices[0].message.content)

    # B. Chatbox 对话框
    st.divider()
    st.subheader("💬 针对该财报进行深度 Q&A")
    
    # 显示历史对话
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])
    
    if user_input := st.chat_input("您可以问：'本季度营收增长的主要动力是什么？'"):
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.chat_message("user").write(user_input)
        
        with st.chat_message("assistant"):
            # 将 PDF 文本作为 Context 传给 AI
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "你是一个资深财务分析师。请仅根据提供的财报内容回答。如果信息不足，请说明。"},
                    {"role": "user", "content": f"财报内容：{st.session_state.pdf_text[:15000]}\n\n问题：{user_input}"}
                ]
            )
            answer = response.choices[0].message.content
            st.write(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
else:
    st.info("👈 请在左侧输入公司名称并点击‘搜索并下载财报’开始项目。")