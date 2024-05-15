import streamlit as st # (1)
from langchain.schema import HumanMessage
from langchain.schema import AIMessage
from langchain.chat_models import ChatOpenAI # (1)
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
import logging
import sys
from dotenv import load_dotenv

load_dotenv() # (2)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, force=True) # (3)

try: # (4)
    memory = st.session_state["memory"]
except:
    memory = ConversationBufferMemory(return_messages=True)

llm = ChatOpenAI(model_name="gpt-3.5-turbo")
chain = ConversationChain(llm=llm, memory=memory, verbose=True) # (5)

st.title("🐟チャットの単純な実装🐟") # (2)
c = st.container()
prompt = st.text_input("メッセージを入力してください。")
history = [
    AIMessage(content="こんにちは。お手伝いできることはありますか？", additional_kwargs={}, example=False)
]

if prompt: # (6)
    chain(prompt) # (7)
    st.session_state["memory"] = memory # (8)
    try:
        history = memory.load_memory_variables({})["history"] # (9)
    except Exception as e:
        st.error(e)

for index, chat_message in enumerate(history): # (4)
    if type(chat_message) == HumanMessage: # (5)
        with c.chat_message("user", avatar="🧑"):
            st.write(chat_message.content)
    elif type(chat_message) == AIMessage: # (6)
        with c.chat_message("agent", avatar="🤖"):
            st.write(chat_message.content)