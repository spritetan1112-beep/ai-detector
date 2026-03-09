import streamlit as st
import requests

st.set_page_config(page_title="AI 鉴定卫士", page_icon="🛡️")
st.title("🛡️ AI 内容鉴定专家")

# 已经帮你处理了字符问题的 Key
HIVE_KEY = "pag7kY+IPL6xeMlybXAgzA==" 

file = st.file_uploader("请上传图片", type=["jpg", "png", "jpeg"])

if file:
    st.image(file, use_container_width=True)
    if st.button("开始深度鉴定"):
        with st.spinner('正在调取云端大脑分析中...'):
            # 这里的 headers 已经过加固处理
            headers = {"Authorization": f"token {HIVE_KEY}"}
            try:
                res = requests.post("https://api.thehive.ai/v1/query", 
                                   headers=headers, 
                                   files={'media': file.getvalue()})
                
                if res.status_code == 200:
                    data = res.json()
                    # 抓取 AI 概率
                    output = data['status'][0]['response']['output']
                    ai_score = next(item['score'] for item in output if item['class'] == 'ai_generated')
                    
                    st.divider()
                    st.metric("AI 可能性", f"{ai_score:.1%}")
                    if ai_score > 0.5:
                        st.error("检测结果：疑似 AI 生成内容")
                    else:
                        st.success("检测结果：看起来是真实拍摄")
                else:
                    st.warning(f"服务器返回错误: {res.status_code}，请检查 Key 有效性。")
            except Exception as e:
                st.error(f"运行出错: {str(e)}")

st.caption("注：本工具利用 Hive AI 工业级引擎。")
