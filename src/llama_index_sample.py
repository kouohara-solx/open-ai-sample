import streamlit as st
from langchain_openai import ChatOpenAI
from llama_index.core import Settings, VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage
import openai
import logging
import sys
import os
from dotenv import load_dotenv  # (1)

load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]  # (2)

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, force=True)  # (3)

Settings.llm = ChatOpenAI(model="gpt-3.5-turbo")  # (4)

dir_path = os.path.dirname(os.path.realpath(__file__))
documents = SimpleDirectoryReader(os.path.join(dir_path, "data")).load_data()
index = VectorStoreIndex.from_documents(documents)
index.storage_context.persist()  # (5)

storage_context = StorageContext.from_defaults(persist_dir="./storage")
index = load_index_from_storage(storage_context)
query_engine = index.as_query_engine()  # (6)

st.title("🐟LlamaIndexのサンプル🐟")
st.text("外部データを読み込んでいます。")
prompt = st.text_input("質問を入力してください。")  # (7)

if prompt:  # (8)
    try:
        response = query_engine.query(
            f"簡潔な日本語で答えてください。また文章に記載のない場合はその旨を教えてください。 ```{prompt}```"
        )  # (9)
    except Exception as e:
        print("error")
        response = str(e)
    # OpenAIの回答を表示
    st.write(response.response)
