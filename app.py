import streamlit as st
import requests

st.set_page_config(page_title="AI 鉴定卫士", page_icon="🛡️")
st.title("🛡️ AI 内容鉴定专家")

# 这里填你自己的 Key
HIVE_KEY = "pag7kY+ІPLбxеМlуbXAgzA==" 

file = st.file_uploader("请上传图片", type=["jpg", "png", "jpeg"])

if file:
    st.image(file, use_container_width=True)
    if st.button("开始深度鉴定"):
        with st.spinner('调取云端大脑分析中...'):
            headers = {"Authorization": f"token {HIVE_KEY}"}
            res = requests.post("https://api.thehive.ai/v1/query", 
                               headers=headers, 
                               files={'media': file.getvalue()})
            if res.status_code == 200:
                score = res.json()['status'][0]['response']['output'][0]['score']
                st.divider()
                st.metric("AI 可能性", f"{score:.1%}")
                if score > 0.5:
                    st.error("检测结果：疑似 AI 生成内容")
                else:
                    st.success("检测结果：看起来是真实拍摄")
            else:
                st.warning("Key 可能输入有误，请检查。")
