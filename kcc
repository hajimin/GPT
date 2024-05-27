import time
import openai
import requests
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
import urllib3
import os
import streamlit as st

# SSL 인증서 경고 무시
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class SSLAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = urllib3.util.create_urllib3_context()
        context.check_hostname = False
        context.verify_mode = urllib3.ssl.CERT_NONE
        kwargs['ssl_context'] = context
        return super(SSLAdapter, self).init_poolmanager(*args, **kwargs)

# 세션 생성
session = requests.Session()
session.mount('https://', SSLAdapter())

# 환경 변수에서 API 키 가져오기
api_key = os.getenv("OPENAI_API_KEY")
organization_id = 'org-iPpZEE3rIksM58FU6N4dOXoy'
assistant_id = 'asst_gSo5oyon5bH785Wcw59V2obe'

openai.api_key = api_key
openai.organization = organization_id

class OpenAIClient:
    def __init__(self, api_key, session):
        self.api_key = api_key
        self.session = session
        openai.api_key = api_key

    def post(self, url, **kwargs):
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'OpenAI-Organization': organization_id
        }
        kwargs['headers'] = headers
        return self.session.post(url, **kwargs)

client = OpenAIClient(api_key, session)
# Streamlit 인터페이스 설정
st.title("OpenAI Assistant Chat")

user_input = st.text_input("메시지를 입력하세요:", "KCC글라스 핸드폰 지원금 규정에 대해 알고 싶어요 (한국어로 답변)")
if st.button("전송"):
    with st.spinner("응답을 기다리는 중..."):
        try:
            # Existing Assistant 가져오기
            existing_assistant = openai.beta.assistants.retrieve(assistant_id=assistant_id)
            # st.write(f"This is the existing assistant object: {existing_assistant} \n")

            # Thread 생성
            my_thread = openai.beta.threads.create()
            # st.write(f"This is the thread object: {my_thread} \n")

            # Thread에 메시지 추가
            my_thread_message = openai.beta.threads.messages.create(
                thread_id=my_thread.id,
                role="user",
                content=user_input
            )
            # st.write(f"This is the message object: {my_thread_message} \n")

            # Assistant 실행
            my_run = openai.beta.threads.runs.create(
                thread_id=my_thread.id,
                assistant_id=assistant_id,
                instructions=existing_assistant.instructions
            )
            # st.write(f"This is the run object: {my_run} \n")

            # Run 상태 확인 및 완료될 때까지 대기
            while my_run.status in ["queued", "in_progress"]:
                keep_retrieving_run = openai.beta.threads.runs.retrieve(
                    thread_id=my_thread.id,
                    run_id=my_run.id
                )
                # st.write(f"Run status: {keep_retrieving_run.status}")

                if keep_retrieving_run.status == "completed":
                    st.write("\n")
                    all_messages = openai.beta.threads.messages.list(
                        thread_id=my_thread.id
                    )

                    st.write("------------------------------------------------------------ \n")
                    # st.write(f"User: {my_thread_message.content}")
                    st.write("KCC글라스 챗봇:")
                    st.info( f"{all_messages.data[0].content[0].text.value}")
                    # st.info( f"{all_messages.data[0].content[0].text.value}")

                    break

                elif keep_retrieving_run.status == "queued" or keep_retrieving_run.status == "in_progress":
                    time.sleep(1)
                else:
                    st.write(f"Run status: {keep_retrieving_run.status}")
                    break

        except Exception as e:
            st.error(f"오류 발생: {str(e)}")

# # Streamlit 앱 실행
# if __name__ == "__main__":
#     st._is_running_with_streamlit = True
#     st.run()
