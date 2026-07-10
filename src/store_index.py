from langchain_community.vectorstores import FAISS
from src.helper import load_pdf_file, text_split, download_hugging_face_embeddings
from dotenv import load_dotenv
import os


load_dotenv()

openai_api_key=os.environ.get("OPENROUTER_API_KEY")
openai_api_base="https://openrouter.ai/api/v1"




extracted_data=load_pdf_file(data='data/')
text_chunks=text_split(extracted_data)
embeddings = download_hugging_face_embeddings()


vectorstore = FAISS.from_documents(
    documents=text_chunks,
    embedding=embeddings
)

vectorstore.save_local("faiss_index")


docsearch = FAISS.load_local(
    "faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)
