import time
from openai import OpenAI
import streamlit as st


assistant_id = 'asst_gSo5oyon5bH785Wcw59V2obe'
openai_api_key = st.secrets['OPENAPI_KEY']
client = OpenAI(api_key=openai_api_key)

st.title("KCC글라스 사내 챗봇")
st.caption("LLM-GPT-3.5-TURBO")

thread = client.beta.threads.create()
thread_id = thread.id

if "messages" not in st.session_state:
    st.session_state["messages"]=[{"role":"assistant","content":"How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Check your Open API Key")
        st.stop()

    if not thread_id:
        st.info("Check your Thread ID")
        st.stop()

    st.session_state.messages.append({"role":"user","content":prompt})
    st.chat_message("user").write(prompt)

    response = client.beta.threads.messages.create(
        thread_id,
        role="user",
        content=prompt,
    )
    print(response)

    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
    )
    run_id = run.id

    while True:
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run_id
        )

        if run.status == "completed":
            break
        else:
            time.sleep(20)
            break
        print(run)

    thread_messsage = client.beta.threads.messages.list(thread_id)
    msg = thread_messsage.data[0].content[0].text.value
    time.sleep(10)
    st.session_state.messages.append({"role": "assisant", "content": msg})
    st.chat_message("assistant").write(msg)



    # response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    # msg = response.choices[0].message.content
    # st.session_state.messages.append({"role":"user","content":msg})
    # st.chat_message("assistant").write(msg)
