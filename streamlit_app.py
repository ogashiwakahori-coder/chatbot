import streamlit as st
import google.generativeai as genai

# Show title and description.
st.title("💬 Chatbot")
st.write(
    "This is a simple chatbot that uses Google's Gemini model to generate responses. "
    "To use this app, you need to provide a Gemini API key, which you can get [here](https://aistudio.google.com/app/apikey). "
)

gemini_api_key = st.text_input("Gemini API Key", type="password")
if not gemini_api_key:
    st.info("Please add your Gemini API key to continue.", icon="🗝️")
else:
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel("gemini-2.5-pro")

    # チャット履歴をセッションに保存
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "chat" not in st.session_state:
        st.session_state.chat = model.start_chat(history=[])

    # 既存メッセージを表示
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 入力欄
    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Geminiでレスポンス生成（stream=Trueでストリーム）
        response_stream = st.session_state.chat.send_message(
            prompt,
            stream=True,
            generation_config={"max_output_tokens": 1024}
        )

        # ストリームを表示し、出力をすべて連結して保存
        full_response = ""
        with st.chat_message("assistant"):
            for chunk in st.write_stream(response_stream):
                full_response += chunk
        st.session_state.messages.append({"role": "assistant", "content": full_response})n session state.
        with st.chat_message("assistant"):
            output = st.write_stream(response)
        st.session_state.messages.append({"role": "assistant", "content": output})
