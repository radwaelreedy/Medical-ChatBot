from flask import Flask, render_template, jsonify, request, session
from src.helper import download_hugging_face_embeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from dotenv import load_dotenv
import os
import uuid
from src.prompt import *


load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "change-this-secret-key")


OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY')
os.environ["OPENROUTER_API_KEY"] = OPENROUTER_API_KEY


embeddings = download_hugging_face_embeddings()


docsearch = FAISS.load_local(
    "faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)


retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 3})


llm = ChatOpenAI(
    model="meta-llama/llama-3.1-8b-instruct",
    temperature=0.4,
    max_tokens=500,
    openai_api_key=os.environ.get("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1"
)

# لاحظ إضافة MessagesPlaceholder("chat_history") هنا
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

# قاموس يخزن تاريخ المحادثة لكل مستخدم (session) لوحده
store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

conversational_rag_chain = RunnableWithMessageHistory(
    rag_chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
    output_messages_key="answer",
)


@app.route("/")
def index():
    # لو المستخدم مالوش session_id لسه، اعمله واحد جديد
    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())
    return render_template('chat.html')


@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    print(input)

    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())
    session_id = session["session_id"]

    response = conversational_rag_chain.invoke(
        {"input": msg},
        config={"configurable": {"session_id": session_id}}
    )
    print("Response : ", response["answer"])
    return str(response["answer"])


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
    