import streamlit as st
import pandas as pd
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="회계 챗봇", page_icon="💼")
st.title("💼 회계 데이터 기반 GPT 챗봇")

try:
    df = pd.read_excel("finance_data.xlsx")
    st.write("finance_data.xlsx 데이터 미리보기:")
    st.dataframe(df)
except FileNotFoundError:
    st.error("finance_data.xlsx 파일을 찾을 수 없습니다. 파일이 존재하는지 확인하세요.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "너는 업로드된 회계 데이터를 잘 분석해주는 분석가야."}]

user_input = st.text_input("질문을 입력하세요:", key="user_input")

if user_input:
    data_snippet = df.head(900).to_markdown(index=False)
    prompt = (
        "다음은 회계 데이터 일부야:\n\n"
        f"{data_snippet}\n\n"
        "위 데이터를 참고해서 사용자 질문에 답변해줘.\n"
        f"질문: {user_input}"
    )

    st.session_state.messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.messages
    )

    assistant_reply = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

# 대화 내용은 여기서만 출력
for msg in st.session_state.messages[1:]:
    if msg["role"] == "user" and "회계 데이터" not in msg["content"]:
        st.markdown(f"**👤 질문:** {msg['content']}")
    elif msg["role"] == "assistant":
        st.markdown(f"**🤖 GPT:** {msg['content']}")
